-- Créer la base de données si elle n'existe pas
CREATE DATABASE IF NOT EXISTS miniproject;

-- Utiliser la base de données
USE miniproject;

-- Créer la table 'students' si elle n'existe pas
CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            filiere VARCHAR(255),
            image longblob,
            image_pure longblob,
            accepte INT
        );

CREATE TABLE IF NOT EXISTS absence (
    id_ab INT AUTO_INCREMENT PRIMARY KEY,
    id INT NOT NULL,
    time VARCHAR(255) NOT NULL,
     date varchar(255)
);