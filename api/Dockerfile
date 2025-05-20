# Utilise une image legere de python 3.12 comme base
FROM python:3.12-slim

# Definit le repertoire de travail dans le conteneur
WORKDIR /app

# Copie les dependances dans le conteneur
COPY requirements.txt .

# Install les dependances Python sans mise en cache
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copie tous les fichier .py et .db de mon projet dans le conteneur
COPY . .

# Lance le serveur uvicorn pour executer l'API FastAPI
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" ]