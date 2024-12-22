# Utiliser l'image officielle Python 3.9 slim
FROM python:3.9-slim

# Étape 1 : Installer les dépendances système nécessaires, y compris CMake, dlib et les outils de compilation
RUN apt-get update && apt-get install -y \
    qt5-qmake qtbase5-dev \
    x11-apps \
    build-essential \
    cmake \
    libssl-dev \
    libffi-dev \
    libjpeg-dev \
    libcurl4-openssl-dev \
    libsqlite3-dev \
    ffmpeg \
    tk \
    && rm -rf /var/lib/apt/lists/*

# Étape 2 : Installer dlib via pip (et CMake si nécessaire)
RUN pip install --no-cache-dir \
    dlib \
    PyQt5 \
    mysql-connector-python \
    opencv-python \
    Pillow \
    face_recognition\
    matplotlib\
    pandas\
    fpdf\
    IMAPClient

# Définir le répertoire de travail
WORKDIR /usr/app/src

# Copier le script Python dans le conteneur
COPY . .

# Commande à exécuter au démarrage
CMD ["sh", "-c", "sleep 10 && python Menu.py"]
