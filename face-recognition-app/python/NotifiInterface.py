
from imapclient import IMAPClient
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import  QIcon, QFont

from PyQt5.QtWidgets import (
    QHeaderView,
    QTextEdit,
    QTreeWidgetItem,
    QTreeWidget,

    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,

)

class NotifiInterface(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget  # Référence au QStackedWidget pour la navigation

        # Layout principal
        main_layout = QVBoxLayout(self)

        # Section titre avec bouton Home et titre centré
        title_section = QHBoxLayout()

        # Bouton Home avec icône
        home_btn = QPushButton("Home")
        home_btn.setIcon(QIcon("path_to_home_icon.png"))  # Remplace par le chemin vers ton icône
        home_btn.setStyleSheet(
            """
            QPushButton {
                padding: 10px; 
                font-size: 16px; 
                border-radius: 8px; 
                background-color: #90c695; 
                color: white;
            }
            QPushButton:hover {
                background-color: #77ab85;
            }
            """
        )
        home_btn.setCursor(Qt.PointingHandCursor)
        title_section.addWidget(home_btn, alignment=Qt.AlignLeft)

        # Spacer pour centrer le titre
        title_section.addStretch(1)

        # Label du titre
        title_label = QLabel("Votre Boîte Email")
        title_label.setFont(QFont("Helvetica", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_section.addWidget(title_label)

        # Spacer pour équilibrer le layout
        title_section.addStretch(1)

        # Ajouter le layout de titre au layout principal
        main_layout.addLayout(title_section)

        # Connecter le bouton Home pour naviguer
        home_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        # Section Liste des Emails
        email_section_layout = QVBoxLayout()
        email_label = QLabel("📬 Liste des Emails")
        email_label.setFont(QFont("Arial", 23 ,QFont.Bold))
        email_section_layout.addWidget(email_label)

        # Ajout du tableau pour les emails
        self.email_table = QTreeWidget(self)
        self.email_table.setColumnCount(3)
        self.email_table.setHeaderLabels(["📌 Sujet", "✉️ Expéditeur", "🗓️ Date d'envoi"])
        # Appliquer la feuille de style comme précédemment
        self.email_table.setStyleSheet(
    """
    QTreeWidget {
        background-color: #f7f7f7; 
        border: 1px solid #ccc; 
        font-size: 16px; 
        alternate-background-color: #f0f0f0; /* Couleur des lignes paires */
    }
    QTreeWidget::item {
        height: 40px;
        padding: 5px;
    }
    QTreeWidget::item:hover {
        background-color: #e8f5e9; /* Vert clair pour le survol */
    }
    QTreeWidget::item:selected {
        background-color: #c8e6c9; /* Vert pastel pour la sélection */
        color: black;
    }
    QHeaderView::section {
        background-color: #007bff; /* Bleu moderne */
        color: white; /* Texte blanc pour une meilleure visibilité */
        font-size: 18px;  /* Taille de la police ajustée */
        font-weight: bold; 
        padding: 10px 5px;  /* Espacement augmenté pour plus de lisibilité */
        border: none; /* Enlève la bordure */
        text-align: center;
    }
    """
)

# Rendre les colonnes de largeur égale
        header = self.email_table.header()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Colonne 0
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Colonne 1
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Colonne 2
# Ajoutez d'autres colonnes si nécessaire en ajustant les indices.



        email_section_layout.addWidget(self.email_table)

        self.host = "imap.gmail.com"  # Remplacez par le serveur IMAP de votre fournisseur
        self.email_user = "issam.mouhala@gmail.com"  # Votre e-mail
        self.email_pass = "rgiz lcpm isfb iydi"  # Votre mot de passe ou mot de passe d'application


        # Remplir le tableau avec les emails
        for subject, sender, content, date in self.fetch_last_10_emails( self.host,self.email_user, self.email_pass):
            item = QTreeWidgetItem(self.email_table, [subject, sender, date])
            item.setData(0, Qt.UserRole, (subject, sender, content, date))

        main_layout.addLayout(email_section_layout)

        # Zone Détails Email
        details_section_layout = QVBoxLayout()
        details_label = QLabel("Détails de l'Email")
        details_label.setFont(QFont("Arial", 21, QFont.Bold))
        details_section_layout.addWidget(details_label)

        self.details_text = QTextEdit(self)
        self.details_text.setReadOnly(True)
        self.details_text.setStyleSheet("background-color: #f9f9f1; font-size: 18px; padding: 10px;")
        details_section_layout.addWidget(self.details_text)

        main_layout.addLayout(details_section_layout)

        # Connecter l'affichage des détails
        self.email_table.itemClicked.connect(self.show_email_details)

    def show_email_details(self, item):
        """Affiche les détails de l'email sélectionné dans le QTextEdit"""
        subject, sender, content, date = item.data(0, Qt.UserRole)
        details = (
            f"Sujet : {subject}\n"
            f"Expéditeur : {sender}\n"
            f"Date d'envoi : {date}\n\n"
            f"Contenu :\n{content}"
        )
        self.details_text.setText(details)
    def decode_header_value(self,value):
      if value:
        decoded_parts = decode_header(value)
        decoded_string = ""
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                part = part.decode(encoding if encoding else "utf-8", errors="ignore")
            decoded_string += part
        return decoded_string
      return "Non disponible"


# Fonction pour récupérer le dernier e-mail (sujet, expéditeur, date, contenu)
    def fetch_last_10_emails(self,host, email_user, email_pass):
        try:
            with IMAPClient(host) as client:
                client.login(email_user, email_pass)
                client.select_folder("INBOX", readonly=True)  # Accès à la boîte de réception
                
                # Récupérer les ID des messages
                messages = client.search("ALL")
                if not messages:
                    return "Aucun e-mail trouvé."

                # Récupérer les 10 derniers messages (ou moins si moins de 10 messages)
                last_10_message_ids = messages[-10:]
                last_10_message_ids.reverse()
                emails = []

                for message_id in last_10_message_ids:
                    message_data = client.fetch(message_id, "RFC822")
                    msg = email.message_from_bytes(message_data[message_id][b"RFC822"])
                    
                    # Décoder le sujet, l'expéditeur et la date
                    subject = self.decode_header_value(msg.get("Subject"))
                    sender = self.decode_header_value(msg.get("From"))
                    if sender.count("@edu.uiz.ac.ma")==0:
                        break
                    date_sent = msg.get("Date")
                    date_sent_parsed = (
                        parsedate_to_datetime(date_sent).strftime("%Y-%m-%d")
                        if date_sent
                        else "Date non disponible"
                    )

                    # Extraire le contenu de l'e-mail
                    content = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                content = part.get_payload(decode=True).decode(errors="ignore")
                                break
                    else:
                        content = msg.get_payload(decode=True).decode(errors="ignore")
                    
                    content = content.replace("\r\n", "")
                    emails.append((subject, sender, content, date_sent_parsed))
                
                return emails
        except Exception as e:
            return [("Erreur", str(e), "", "")]

    # Fonction pour afficher les e-mails sous forme de tuple dans Tkinter

    # Paramètres de connexion
   