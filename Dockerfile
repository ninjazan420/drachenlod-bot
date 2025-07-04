FROM gorialis/discord.py

# Install Pillow dependencies and Impact font
RUN apt-get update && apt-get install -y \
    python3-pil \
    fonts-liberation \ 
    git \
    && \
    rm -rf /var/lib/apt/lists/*

# Accept EULA for MS fonts
RUN echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections

COPY src/ /app
# Erstelle den data Ordner statt ihn zu kopieren
RUN mkdir -p /app/data
WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]
