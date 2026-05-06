FROM python:3.12-slim

# Anstatt python könnte man auch ein Basis-Linux nutzen, und die Dependencies
# selbst installieren
# FROM alpine:3.20
# RUN apk add python3

# Eine Art "Erstelle den Ordner falls er nicht existiert" und "cd /app" in diesen
WORKDIR /app

# Kopiert etwas vom Host (wo das Image gebaut wird) in das Image
# In diesem Fall requirements.txt in den aktuellen Ordner "."
# COPY Befehle werden nur neu ausgeführt, wenn die kopierten Dateien geändert sind
COPY requirements.txt .

# Führt einen beliebigen Shell-Befehl aus, hier ein pip install, also alle
# Pythonabhängigkeiten
# Befehl wird nur dann neu ausgeführt, wen die Teil hinter RUN sich ändert
RUN pip install --no-cache-dir -r requirements.txt

# Kopiert alles vom aktuellen Ordner in den aktuellen Ordner im Image
COPY . .

# Was ggf. für Ports genutzt werden
EXPOSE 8000

# Default-Start-Befehl, wenn aus dem Image ein Container erzeugt wird
CMD ["python", "app.py"]