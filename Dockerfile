# Utiliser une image de base Python
FROM python:3.9-slim

# Installer les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    xvfb \
    libgl1-mesa-glx \
    libxrender1 \
    libsm6 \
    libxext6 \
    qt5-qmake \
    libqt5gui5 \
    libqt5widgets5 \
    libqt5opengl5-dev \
    cmake \
    build-essential \
    libatlas-base-dev \
    gfortran \
    python3-dev \
    && apt-get clean  # Installer CMake pour la compilation de dlib

# Créer un environnement virtuel
RUN python -m venv /env

# Copier et installer les dépendances Python
RUN /env/bin/pip install --upgrade pip && /env/bin/pip install --no-cache-dir \
    --timeout=120 \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    psycopg2-binary \
    numpy \
    opencv-python \
    face_recognition \
    pandas \
    fpdf \
    matplotlib \
    imapclient \
    PyQt5 \
    Pillow

# Copier les fichiers de l'application
COPY . /app/classes

# Définir le répertoire de travail
WORKDIR /app/classes

# Commande par défaut
CMD ["xvfb-run", "/env/bin/python", "Menu.py"]
