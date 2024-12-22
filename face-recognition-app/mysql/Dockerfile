# Utiliser l'image officielle MySQL la plus récente
FROM mysql:latest

# Copier le script SQL pour initialiser la base de données
COPY ./databse_students.sql /docker-entrypoint-initdb.d/
