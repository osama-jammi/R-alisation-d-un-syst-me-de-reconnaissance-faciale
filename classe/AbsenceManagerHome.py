import psycopg2
from psycopg2.extras import DictCursor
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont,QColor
import pandas as pd  
from fpdf import FPDF
from PyQt5.QtWidgets import (
    QComboBox,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QGridLayout,
    QListWidget,
    QListWidgetItem,
    QCalendarWidget,
    QMessageBox,
    QDialog,
    QFileDialog,
    QGraphicsDropShadowEffect
)


class AbsenceManagerHome(QWidget):

    def __init__(self, stacked_widget, app_reference):
        
        super().__init__()
        self.conn = psycopg2.connect(
        host='localhost',
        user='docker',  # Nom d'utilisateur PostgreSQL
        password='docker',  # Mot de passe PostgreSQL
        database='miniproject'  # Nom de la base de données
    )
        self.stacked_widget = stacked_widget  
        self.app_reference = app_reference  
        self.conn = psycopg2.connect(
        host='localhost',
        user='docker',  # Nom d'utilisateur PostgreSQL
        password='docker',  # Mot de passe PostgreSQL
        database='miniproject'  # Nom de la base de données
    )


        common_stylesheet = """
        QListWidget {
            background-color: #f9f9f9; 
            border-radius: 12px; 
            padding: 5px; 
        }
        QListWidget::item {
            padding: 10px; 
            color: black;
            font-size: 14px;
            font-family: Arial;
            border: 1px solid transparent; 
            border-radius: 8px; 
        }
        QListWidget::item:hover {
            background-color: #a6e3a1; 
            border: 1px solid #6cc24a; 
        }
        """

        # Stylesheet pour le calendrier
        calendar_stylesheet = """
        QCalendarWidget {
            background-color: #f9f9f9; 
            border-radius: 10px;
            padding: 5px;
            font-size: 14px;
            font-family: Arial;
        }
        """
      
        main_layout = QVBoxLayout(self)

        
        nav_layout = QHBoxLayout()
        notif_btn = QPushButton("Notification")
        record_absence_btn = QPushButton("Record Absence")
        manage_users_btn = QPushButton("Manage Users")  
        absence_analysis_btn = QPushButton("Absence Analysis")


        button_stylesheet = """
        QPushButton {
            background-color: #a6e3a1; 
            padding: 10px; 
            font-size: 14px; 
            border-radius: 12px;
        }
        QPushButton:hover {
            background-color: #8bc68b;
        }
        """
        def apply_shadow(widget):
            shadow_effect = QGraphicsDropShadowEffect()
            shadow_effect.setBlurRadius(15)  # Flou de l'ombre
            shadow_effect.setColor(QColor(0, 0, 0, 100))  # Couleur noire avec transparence
            shadow_effect.setOffset(3, 3)  # Décalage de l'ombre
            widget.setGraphicsEffect(shadow_effect)

       
        





        notif_btn.setStyleSheet(button_stylesheet)
        notif_btn.setCursor(Qt.PointingHandCursor)
        record_absence_btn.setStyleSheet(button_stylesheet)
        record_absence_btn.setCursor(Qt.PointingHandCursor)
        manage_users_btn.setStyleSheet(button_stylesheet)
        manage_users_btn.setCursor(Qt.PointingHandCursor)
        absence_analysis_btn.setStyleSheet(button_stylesheet)
        absence_analysis_btn.setCursor(Qt.PointingHandCursor)

        nav_layout.addWidget(record_absence_btn)
        nav_layout.addWidget(manage_users_btn)
        nav_layout.addWidget(absence_analysis_btn)
        nav_layout.addWidget(notif_btn)
        main_layout.addLayout(nav_layout)


        export_button = QPushButton("Exporter les données")
        export_button.setStyleSheet("""
        background-color: #90caf9; 
        padding: 10px; 
        font-size: 14px; 
        border-radius: 10px;
        """)
        export_button.setCursor(Qt.PointingHandCursor)
        export_button.clicked.connect(self.show_export_dialog)

        
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch() 
      
        bottom_layout.addWidget(export_button, alignment=Qt.AlignRight) 
        
        main_layout.addLayout(bottom_layout)

       
        self.grid_layout = QGridLayout()
        main_layout.addLayout(self.grid_layout)

        self.calendar_widget = QCalendarWidget()
        self.calendar_widget.setStyleSheet(calendar_stylesheet)
        self.grid_layout.addWidget(self.calendar_widget, 0, 0, 2, 1)
        self.calendar_widget.clicked[QDate].connect(self.get_selected_date)
        apply_shadow(self.calendar_widget)

        # Autres sections comme Absences à venir, Notifications, etc.
        self.upcoming_absences_label = QLabel("Listes des  Absences")
        self.upcoming_absences_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 5px;")
        self.upcoming_absences_list = QListWidget()
        self.upcoming_absences_list.setStyleSheet(common_stylesheet)
        self.grid_layout.addWidget(self.upcoming_absences_label, 0, 1)
        self.grid_layout.addWidget(self.upcoming_absences_list, 1, 1)
        

       


        statistics_label = QLabel("Your Statistics")
        statistics_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 5px;")
        self.statistics_list = QListWidget()
        self.statistics_list.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")
        

        # Ajout au layout principal
 
        
        self.grid_layout.addWidget(statistics_label, 0, 2)
        self.grid_layout.addWidget(self.statistics_list, 1, 2)

        # Appliquer le style et l'ombre à la liste des absences
        self.upcoming_absences_list.setStyleSheet(common_stylesheet)
        apply_shadow(self.upcoming_absences_list)

        # Appliquer le style et l'ombre à la liste des statistiques
        self.statistics_list.setStyleSheet(common_stylesheet)
        apply_shadow(self.statistics_list)





        # Connecter le bouton "Record Absence" à la fonction du script
        record_absence_btn.clicked.connect(self.app_reference.run_record_absence_script)

        # Signal pour passer à l'interface de gestion des utilisateurs
        notif_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        manage_users_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        absence_analysis_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
    def get_selected_date(self, date):
        formatted_date = date.toString("yyyy/MM/dd")
        self.upcoming_absences_list.clear()

        cursor = self.conn.cursor()
        print(formatted_date)
        # Exécuter la requête pour récupérer les données d'absence par heure
        cursor.execute("""
           SELECT u.username,u.filiere,a.time
           FROM absence a
           JOIN users u ON a.id = u.id
           WHERE a.date = DATE(%s) order by u.filiere
           """,(formatted_date,))
        liste=cursor.fetchall()
        if liste==[]:

            item = QListWidgetItem("No Absences ...")
            self.upcoming_absences_list.addItem(item)
        else:
            for j,i,k in liste:
                item = QListWidgetItem(f"{j}--{i}--{k}")
                self.upcoming_absences_list.addItem(item)
            for i in range(len(self.upcoming_absences_list)):
               font = QFont()
               font.setBold(True)
               font.setPointSize(14)
               font.setCapitalization(QFont.Capitalize)
               self.upcoming_absences_list.item(i).setFont(font)
               self.upcoming_absences_list.item(i).setTextAlignment(Qt.AlignCenter)



        self.grid_layout.addWidget(self.upcoming_absences_label, 0, 1)
        self.grid_layout.addWidget(self.upcoming_absences_list, 1, 1) 
        self.statistics_list.clear()
        query = """
        SELECT users.filiere, COUNT(absence.id) AS total_absences
        FROM absence
        JOIN users ON absence.id = users.id
        where absence.date=%s
        GROUP BY users.filiere;
        """
        cursor = self.conn.cursor(cursor_factory=DictCursor)
        cursor.execute(query,(formatted_date,))
        statistics_data = cursor.fetchall()

        print("Data fetched from the database:", statistics_data)
        # Ajout des statistiques à la liste
        if statistics_data:
            for record in statistics_data:
                filiere = record['filiere']
                total_absences = record['total_absences']
                print(f"Filière: {filiere}, Total des absences: {total_absences}")
                formatted_item = f"Filière: {filiere} | Total des absences: {total_absences}"
                self.statistics_list.addItem(formatted_item)

        else:
            self.statistics_list.addItem(QListWidgetItem("No statistics available."))
    # Fonction pour récupérer le dernier e-mail et retourner un tuple (expéditeur, sujet, date sans heure)
  

    def show_export_dialog(self):
        # Étape 1 : Récupérer les filières disponibles depuis la base de données
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT filiere FROM users")
        filieres = [row[0] for row in cursor.fetchall()]

        if not filieres:
            QMessageBox.warning(self, "Erreur", "Aucune filière trouvée dans la base de données.")
            return

        # Étape 2 : Afficher une boîte de dialogue pour sélectionner une filière
        dialog = QDialog(self)
        dialog.setWindowTitle("Choisir une filière")
        dialog_layout = QVBoxLayout(dialog)

        filiere_label = QLabel("Sélectionnez une filière à exporter :")
        dialog_layout.addWidget(filiere_label)

        filiere_dropdown = QComboBox()
        filiere_dropdown.addItems(filieres)
        dialog_layout.addWidget(filiere_dropdown)

        confirm_button = QPushButton("Confirmer")
        confirm_button.clicked.connect(lambda: self.show_export_format(dialog, filiere_dropdown.currentText()))
        dialog_layout.addWidget(confirm_button)

        dialog.exec()

    def show_export_format(self, parent_dialog, filiere):
        # Étape 3 : Afficher les options de format d'exportation
        parent_dialog.accept()

        format_dialog = QDialog(self)
        format_dialog.setWindowTitle("Choisir le format d'exportation")
        dialog_layout = QVBoxLayout(format_dialog)

        format_label = QLabel("Choisissez un format :")
        dialog_layout.addWidget(format_label)

        format_dropdown = QComboBox()
        format_dropdown.addItems(["Excel", "PDF", "Texte"])
        dialog_layout.addWidget(format_dropdown)

        confirm_button = QPushButton("Exporter")
        confirm_button.clicked.connect(lambda: self.perform_export(filiere, format_dropdown.currentText()))
        dialog_layout.addWidget(confirm_button)

        format_dialog.exec()

    def perform_export(self, filiere, file_format):
        # Étape 4 : Récupérer les données de la base de données
        query = """
        SELECT u.username, u.filiere, a.date,a.time
        FROM users u
        JOIN absence a ON u.id = a.id
        WHERE u.filiere = %s
        """
        cursor = self.conn.cursor(cursor_factory=DictCursor)
        cursor.execute(query, (filiere,))
        data = cursor.fetchall()

        if not data:
            QMessageBox.warning(self, "Erreur", f"Aucune donnée trouvée pour la filière {filiere}.")
            return

        # Étape 5 : Exporter selon le format sélectionné
        if file_format == "Excel":
            self.export_to_excel(data, filiere)
        elif file_format == "PDF":
            self.export_to_pdf(data, filiere)
        elif file_format == "Texte":
            self.export_to_text(data, filiere)

    def export_to_excel(self, data, filiere):
        file_path, _ = QFileDialog.getSaveFileName(self, "Exporter en Excel", "", "Fichiers Excel (*.xlsx)")
        if file_path:
            df = pd.DataFrame(data)
            df = df.sort_values(by='date')
            df.to_excel(file_path, index=False , sheet_name=filiere)
            QMessageBox.information(self, "Succès", f"Les données de la filière {filiere} ont été exportées en Excel.")

    def export_to_pdf(self, data, filiere):
        file_path, _ = QFileDialog.getSaveFileName(self, "Exporter en PDF", "", "Fichiers PDF (*.pdf)")
        if file_path:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Données de la filière {filiere}", ln=True, align="C")
            pdf.ln(10)

            for record in data:
                pdf.cell(200, 10, txt=str(record), ln=True)

            pdf.output(file_path)
            QMessageBox.information(self, "Succès", f"Les données de la filière {filiere} ont été exportées en PDF.")

    def export_to_text(self, data, filiere):
        file_path, _ = QFileDialog.getSaveFileName(self, "Exporter en Texte", "", "Fichiers texte (*.txt)")
        if file_path:
            with open(file_path, "w") as f:
                f.write(f"Données de la filière {filiere}\n\n")
                for record in data:
                    f.write(str(record) + "\n")
            QMessageBox.information(self, "Succès", f"Les données de la filière {filiere} ont été exportées en texte.")


    
