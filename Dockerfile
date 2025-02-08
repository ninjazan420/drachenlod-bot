FROM gorialis/discord.py

# Install Pillow dependencies and Impact font
RUN apt-get update && apt-get install -y \
    python3-pil \
    fonts-liberation \ 
    && \
    rm -rf /var/lib/apt/lists/*

# Accept EULA for MS fonts
RUN echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections

COPY src/ /app
COPY data/ /app/data
WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]
