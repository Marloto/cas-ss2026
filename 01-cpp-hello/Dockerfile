# Wir nutzen ein einziges Basis-Image
FROM ubuntu:22.04

# 1. System-Updates und Tools installieren
# Wir fügen git und ca-certificates direkt hinzu
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 2. Arbeitsverzeichnis im Container erstellen
WORKDIR /app

# 3. Den gesamten Quellcode von deinem Rechner in den Container kopieren
COPY . .

# 4. Build-Ordner erstellen und Projekt kompilieren
RUN mkdir -p build && cd build && \
    cmake .. && \
    make

# 5. Den Startbefehl festlegen
# Hinweis: Pfad zum Binary anpassen, falls es in build/ liegt
CMD ["./build/server"]