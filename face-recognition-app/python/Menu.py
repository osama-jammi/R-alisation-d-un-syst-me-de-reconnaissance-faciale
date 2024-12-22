import sys
import subprocess
import mysql.connector
import AbsenceAnalyticsInterface 
import AbsenceManagerHome
import NotifiInterface
import ManageUsersInterface
from PyQt5.QtWidgets import (
   
    QApplication,
   
    QMainWindow,
   
    QStackedWidget,
  
)



try:
    # Connexion par défaut pour créer la base de données si elle n'existe pas
    connection = mysql.connector.connect(
        user='root', password='root', host='mysql', port="3306"
    )
    connection.autocommit = True
    default_cursor = connection.cursor()

    # Vérifier si la base de données "miniproject" existe, sinon la créer
    default_cursor.execute("CREATE DATABASE IF NOT EXISTS  miniproject;")

    print("Base de données 'miniproject..' créée avec succès.")
    default_cursor.close()
    connection.close()

    # Connexion à la base de données "miniproject"
    conn = mysql.connector.connect(
        user='root', password='root', host='mysql', port="3306",database="miniproject"
    )

    # Création de tables si elles n'existent pas encore
    cursor = conn.cursor()

    # Création de la table 'users'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            filiere VARCHAR(255),
            image longblob,
            image_pure longblob,
            accepte INT
        );
    """)


    # Création de la table 'absence' avec la colonne 'date' corrigée
    cursor.execute("""
CREATE TABLE IF NOT EXISTS absence (
    id_ab INT AUTO_INCREMENT PRIMARY KEY,
    id INT NOT NULL,
    time VARCHAR(255) NOT NULL,
     date varchar(255)
);

    """)

    # Commit des modifications
    conn.commit()


except mysql.connector.Error as e:
    print(f"Erreur lors de la connexion ou de l'exécution SQL : {e}")
# Fonction pour afficher la filière choisie et fermer la fenêtre




class AbsenceManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.conn = mysql.connector.connect(
        user='root', password='root', host='mysql', port="3306", database='miniproject'
    )
        self.setWindowTitle("Absence Manager")
        self.setGeometry(100, 100, 1200, 800)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.home_interface = AbsenceManagerHome.AbsenceManagerHome(self.stacked_widget, self,self.conn)
        self.stacked_widget.addWidget(self.home_interface)
        self.notif = NotifiInterface.NotifiInterface(self.stacked_widget)
        self.stacked_widget.addWidget(self.notif)
        self.analytics = AbsenceAnalyticsInterface.AbsenceAnalyticsInterface(self.stacked_widget)
        self.stacked_widget.addWidget(self.analytics)

        self.manage_users_interface = ManageUsersInterface.ManageUsersInterface(self.stacked_widget)
        self.stacked_widget.addWidget(self.manage_users_interface)

    def run_record_absence_script(self):
        try:
            subprocess.run(['python', r'recorder.py'])
        except Exception as e:
            print(f"Error executing script: {e}")
    def closeEvent(self, event):
        """Fermer la connexion à la base de données quittant."""
        self.conn.close()
        event.accept()

app = QApplication(sys.argv)
window = AbsenceManagerApp()
window.show()
sys.exit(app.exec_())
