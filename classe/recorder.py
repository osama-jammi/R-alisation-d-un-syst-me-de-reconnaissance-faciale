import datetime
import cv2
import face_recognition
import mysql.connector
import numpy as np
import pickle
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter.simpledialog import askstring
from tkinter import messagebox
import psycopg2

# Connexion à la base de données PostgreSQL
try:
    # Connexion par défaut pour créer la base de données si elle n'existe pas
    default_conn = psycopg2.connect(
        host='localhost',
        user='docker',  # Nom d'utilisateur PostgreSQL
        password='docker',  # Mot de passe PostgreSQL
        database='postgres'  # Base par défaut pour les connexions
    )
    default_conn.autocommit = True
    default_cursor = default_conn.cursor()

    # Vérifier si la base de données "miniproject" existe, sinon la créer
    default_cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'miniproject';")
    if not default_cursor.fetchone():
        default_cursor.execute("CREATE DATABASE miniproject;")
        print("Base de données 'miniproject' créée avec succès.")
    default_cursor.close()
    default_conn.close()

    # Connexion à la base de données "miniproject"
    conn = psycopg2.connect(
        host='localhost',
        user='docker',  # Nom d'utilisateur PostgreSQL
        password='docker',  # Mot de passe PostgreSQL
        database='miniproject'  # Nom de la base de données
    )

    # Création de tables si elles n'existent pas encore
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    filiere VARCHAR(255),
    image BYTEA,
    image_pure BYTEA,
    accepte INT
);
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS absence (
            id_ab SERIAL PRIMARY KEY,
            id INT NOT NULL,
            time VARCHAR(255) NOT NULL,
            date DATE NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

    """)
    conn.commit()
except psycopg2.Error as e:
    print(f"Erreur lors de la connexion ou de l'exécution SQL : {e}")
# Fonction pour afficher la filière choisie et fermer la fenêtre
filiere = askstring("Donner filiere", "Veuillez entrer le filiere(MGSI,BDAISD,GL,SCITCN) :")
filieres=["MGSI","BDIASD","GL","SCITCN"]
while( filiere.upper() not in filieres):
    messagebox.showerror("Erreur", "filiere incorrect.")
    filiere = askstring("Donner filiere", "Veuillez entrer le filiere(MGSI,BDAISD,GL,SCITCN) :")
# Connexion à la base de données
try:
  
    cursor = conn.cursor()

    # Récupérer les encodages et les noms des visages depuis la base de données
    cursor.execute("SELECT id, username, image, filiere FROM users where filiere=%s",(filiere.upper(),))
    known_face_names = []
    known_face_encodings = []
    known_face_id = []
    known_face_filiere = []
     
    for id, username, encoding_blob, filiere in cursor.fetchall():
        encoding = pickle.loads(encoding_blob)
        known_face_encodings.append(encoding)
        known_face_names.append(username)
        known_face_filiere.append(filiere)
        known_face_id.append(id)
    print(known_face_filiere)
    print("Encodages chargés depuis la base de données avec succès.")
except mysql.connector.Error as err:
    print(f"Erreur de connexion à la base de données : {err}")
    exit(1)

# Initialiser la capture vidéo
cap = cv2.VideoCapture(0)
# Fonction pour mettre à jour le flux vidéo
confidence_percentage = 0.0  # Déclarez cette variable au début
cap.read()
def update_frame():
    global recognized_name, confidence_percentage
    ret, frame = cap.read()
    print(ret)

    if not ret:
        print("Erreur de capture vidéo.")
        return

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            recognized_name = known_face_names[best_match_index]
            filiere = known_face_filiere[best_match_index]
            confidence_percentage = 1 - face_distances[best_match_index]  # Confiance en pourcentage
            confidence_percentage = round(confidence_percentage * 100, 2)  # Arrondir à 2 décimales
            color = (10, 150, 10)  # Vert pour visage reconnu
        else:
            recognized_name = "Inconnu"
            filiere = ""
            confidence_percentage = 0.0  # Pas de confiance pour les inconnus
            color = (255, 0, 0)  # Rouge pour visage non reconnu

        # Dessiner un cadre plus large autour du visage (sans espace)
        border_thickness = 5  # Augmenter l'épaisseur du cadre
        cv2.rectangle(frame, (left - border_thickness, top - border_thickness),
                      (right + border_thickness, bottom + border_thickness), color, border_thickness)

        # Ajouter un fond aux informations (nom, filière et confiance)
        info_background_color = (0, 0, 255)  # Fond noir pour l'information
        text_display = f"{recognized_name} ({filiere}) {confidence_percentage}%"
        
        # Calculer la taille du texte et la position
        text_size = cv2.getTextSize(text_display, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        text_x = left + (right - left) // 2 - text_size[0] // 2
        text_y = bottom + 20

        # Dessiner un rectangle comme fond pour l'information
        cv2.rectangle(frame, (text_x - 10, text_y - 25), (text_x + text_size[0] + 10, text_y + 5), info_background_color, -1)
        
        # Afficher le texte par-dessus le fond
        cv2.putText(frame, text_display, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    if recognized_name != "Inconnu" and confidence_percentage >= 50:
        cursor.execute("UPDATE users SET accepte = 1 WHERE username = %s", (recognized_name,))
        conn.commit()
        print(f"{recognized_name} accepté(e).")
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    lbl.imgtk = imgtk
    lbl.configure(image=imgtk)
    lbl.after(10, update_frame)

# Fonction pour demander le code avant de quitter l'application
def on_close():
    code = askstring("Code de sécurité", "Veuillez entrer le code :")
    if code == "1234":
        current_hour = datetime.datetime.now().hour
        time_of_day_value = ""

        # Déterminer la période de la journée : Matin ou Soir
        if 8 <= current_hour <= 10:
            time_of_day_value = "08:30-10:15"
        elif 10 <= current_hour <= 13:
            time_of_day_value = "10:30-12:15"
        elif 14 <= current_hour <= 16:
            time_of_day_value = "14:30-16:15"
        elif 16 <= current_hour <= 19:
            time_of_day_value = "16:30-18:15"
        else:
            time_of_day_value = "P"

        cursor.execute("SELECT id FROM users WHERE accepte = 0 and filiere=%s",(filiere,))
        
        for (id,) in cursor.fetchall():
            cursor.execute("INSERT INTO absence (id, time) VALUES (%s, %s)", (id, time_of_day_value))
        conn.commit()
        cursor.execute("UPDATE users SET accepte = 0")
        conn.commit()

        cap.release()  # Libérer la capture vidéo
        root.destroy() # Fermer la fenêtre Tkinter
    else:
        messagebox.showerror("Erreur", "Code incorrect.")

# Interface Tkinter
root = tk.Tk()
root.title("Reconnaissance Faciale")
root.protocol("WM_DELETE_WINDOW", on_close)
root.configure(bg="#2E2E2E")  # Couleur de fond moderne

# Style du flux vidéo
lbl = tk.Label(root, borderwidth=2, relief="sunken", bg="#1E1E1E")
lbl.pack(padx=20, pady=20)

# Démarrer la mise à jour du flux vidéo
recognized_name = "Inconnu"
update_frame()

# Démarrer la boucle principale Tkinter
root.mainloop()
