import psycopg2
import numpy as np
from matplotlib import dates,pyplot as plt
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import Qt
from PyQt5.QtGui import  QIcon, QFont

from PyQt5.QtWidgets import (

    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
)
import datetime


class AbsenceAnalyticsInterface(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
      
            # Connexion à la base de données "miniproject"
        self.conn = psycopg2.connect(
                host='localhost',
                user='docker',  # Nom d'utilisateur PostgreSQL
                password='docker',  # Mot de passe PostgreSQL
                database='miniproject'  # Nom de la base de données
            )

            # Création de tables si elles n'existent pas encore
         
        self.stacked_widget = stacked_widget

        # Création du layout principal avec marges pour entourer le contenu
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Section de titre et bouton Home
        title_section = QHBoxLayout()
        
        # Home button with icon
        home_btn = QPushButton("Home")
        home_btn.setIcon(QIcon("path_to_home_icon.png"))  # Replace with your home icon path
        home_btn.setStyleSheet("padding: 10px; font-size: 16px; border-radius: 8px; background-color: #90c695;")
        home_btn.setCursor(Qt.PointingHandCursor)
        title_section.addWidget(home_btn, alignment=Qt.AlignLeft)

        # Spacer to center the title
        title_section.addStretch(1)

        # Title label
        title_label = QLabel("Statiques Des Absences")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_section.addWidget(title_label, alignment=Qt.AlignCenter)

        # Spacer for centering
        title_section.addStretch(1)

        # Ajouter un autre espace flexible après le titre

        main_layout.addLayout(title_section)

        # Espace entre le titre et les boutons d'action

        # Création des boutons d'actions alignés sur une même ligne
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)
        button_style = "padding: 10px; background-color: #6dc9f2; border-radius: 12px; font-size: 14px;"
        

        par_filiere_btn = QPushButton("Statistiques par filière")
        par_filiere_btn.setStyleSheet(button_style)
        par_filiere_btn.setCursor(Qt.PointingHandCursor)
        par_filiere_btn.setObjectName("filiere")
        actions_layout.addWidget(par_filiere_btn)
         
        par_somaine_btn = QPushButton("Statistiques par Somaine")
        par_somaine_btn.setStyleSheet(button_style)
        par_somaine_btn.setCursor(Qt.PointingHandCursor)
        par_somaine_btn.setObjectName("somaine")
        actions_layout.addWidget(par_somaine_btn)

        par_temps_btn = QPushButton("Statistiques par temps")
        par_temps_btn.setStyleSheet(button_style)
        par_temps_btn.setCursor(Qt.PointingHandCursor)
        par_temps_btn.setObjectName("tempe")
        actions_layout.addWidget(par_temps_btn)

        main_layout.addLayout(actions_layout)

        # Espace entre les boutons d'action et le graphique
        main_layout.addSpacing(30)

        # Initialisation de la figure (graphique) et ajout au layout
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedHeight(int(self.height() * 1.5))  # Limite la taille du graphique à 80% de la fenêtre
        main_layout.addWidget(self.canvas)

        # Connecter les boutons aux méthodes
        par_filiere_btn.clicked.connect(self.show_absence)
        par_temps_btn.clicked.connect(self.show_absence_temp)
        par_somaine_btn.clicked.connect(self.show_par_somaine)
        home_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
    
    def show_absence_temp(self):
        cursor = self.conn.cursor()
        self.findChild(QPushButton,"tempe").setStyleSheet("border-bottom:1px solid black;padding: 10px; background-color: #6dc9c1; border-radius: 12px; font-size: 14px;")
        self.findChild(QPushButton,"filiere").setStyleSheet("padding: 10px; background-color: #6dc9f2; border-radius: 12px; font-size: 14px;")
        self.findChild(QPushButton,"somaine").setStyleSheet("padding: 10px; background-color: #6dc9f2; border-radius: 12px; font-size: 14px;")


        # Exécuter la requête pour récupérer les données d'absence par heure
        cursor.execute("""
            SELECT time, COUNT(time)
            FROM absence  
            GROUP BY time 
        """)

        list_time = []
        list_nb = []

        # Ajouter les données dans les listes
        for t, nb in cursor.fetchall():
            list_time.append(t)
            list_nb.append(nb)

        # Fermer le curseur
        cursor.close()

        # Effacer le contenu précédent de la figure
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Tracer le graphique en camembert
        wedges, texts, autotexts = ax.pie(
            list_nb, labels=list_time, autopct='%1.1f%%', startangle=90,
            textprops={'color': 'white', 'bbox': dict(facecolor='black', alpha=0.8, edgecolor='none')}
        )

        # Personnaliser les labels de pourcentage
        for autotext in autotexts:
            autotext.set_bbox(dict(facecolor='black', edgecolor='none', alpha=0.8))
            autotext.set_color('white')

        # Titre et légende
        ax.set_title("Temps d'absences", color='black')
        ax.legend(wedges, list_time, title="Temps", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        # Rafraîchir le canvas pour afficher le graphique
        self.canvas.draw()
    def show_absence(self):
        # Exécution d'une requête pour obtenir les données
        cursor = self.conn.cursor()
        self.findChild(QPushButton,"filiere").setStyleSheet("border-bottom:1px solid black;padding: 10px; background-color: #6dc9c1; border-radius: 12px; font-size: 14px;")
        self.findChild(QPushButton,"tempe").setStyleSheet("padding: 10px; background-color: #6dc9f2; border-radius: 12px; font-size: 14px;")
        self.findChild(QPushButton,"somaine").setStyleSheet("padding: 10px; background-color: #6dc9f2; border-radius: 12px; font-size: 14px;")
        cursor.execute("""
            SELECT filiere, COUNT(filiere)
            FROM users u JOIN absence a ON a.id = u.id
            GROUP BY filiere
        """)

        list_filiere = []
        list_nombre_absences = []
        for f, ab in cursor.fetchall():
            list_filiere.append(f)
            list_nombre_absences.append(ab)


        # Création et mise à jour du graphique
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        colors = plt.cm.viridis(np.linspace(0, 1, len(list_filiere)))
        bars = ax.bar(list_filiere, list_nombre_absences, color=colors)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom', fontsize=12)

        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_title("Absences par filière", color='black')
        ax.set_xlabel("Filière", fontsize=14, color='red')
        ax.set_ylabel("Total des Absences", fontsize=12, color='green')

        # Mise à jour de la figure sur le canvas
        self.canvas.draw()

    def show_par_somaine(self):
    
        cursor=self.conn.cursor()
        self.findChild(QPushButton,"somaine").setStyleSheet("border-bottom:1px solid black;padding: 10px; background-color: #6dc9c1; border-radius: 12px; font-size: 14px;")
        self.findChild(QPushButton,"filiere").setStyleSheet("padding: 10px; background-color: #6dc9f2; border-radius: 12px; font-size: 14px;")
        self.findChild(QPushButton,"tempe").setStyleSheet("padding: 10px; background-color: #6dc9f2; border-radius: 12px; font-size: 14px;")
        # Exécuter la requête pour récupérer les données d'absence
        cursor.execute("""
            SELECT date, COUNT(id) 
FROM absence  
WHERE date BETWEEN CURRENT_DATE - INTERVAL '7 days' AND CURRENT_DATE
GROUP BY date
ORDER BY date;

        """)

        today = datetime.datetime.now()
        seven_days_ago = (today - datetime.timedelta(days=7)).date()
        current_day = today.date()

        # Initialiser les listes pour les données d'absence et les dates
        list_absence = []
        list_date = []

        # Ajouter les données dans les listes
        for date, ab in cursor.fetchall():
            list_absence.append(ab)
            list_date.append(date)

        # Fermer la connexion à la base de données

        # Effacer le contenu précédent de la figure
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Tracer les données
        ax.plot(list_date, list_absence, marker='o', linestyle='-', color='black', label='Total d\'absences')

        # Ajouter des annotations pour chaque point avec la date et le total d'absences
        for date, ab in zip(list_date, list_absence):
            ax.annotate(f"{date.strftime('%Y-%m-%d')}: {ab}", (date, ab), 
                        textcoords="offset points", 
                        xytext=(0, 10), 
                        ha='center', fontsize=11, color='white',
                        bbox=dict(facecolor='black', alpha=0.9))  # Fond noir avec transparence

        # Formater l'axe des x pour afficher les dates de manière lisible
        ax.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(dates.DayLocator(interval=1))
        self.figure.autofmt_xdate()  # Rotation des dates

        # Ajustement dynamique de l'axe y
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # Permet des valeurs entières sur l'axe y

        # Ajouter un titre et des labels avec couleurs spécifiques
        ax.set_title(
            f"Absences au fil du temps Semaine : {seven_days_ago} => {current_day}",
            fontsize=17, color='black', bbox=dict(facecolor='red', alpha=0.1)
        )
        ax.set_xlabel("Date", fontsize=15, color='red', bbox=dict(facecolor='red', alpha=0.1))
        ax.set_ylabel("Total des Absences", fontsize=15, color='green', bbox=dict(facecolor='green', alpha=0.1))

        # Afficher la légende
        ax.legend()

        # Rafraîchir le canvas pour afficher le graphique
        self.canvas.draw()