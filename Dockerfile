FROM gorialis/discord.py

# Install Pillow dependencies
RUN apt-get update && apt-get install -y \
    python3-pil \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

COPY src/ /app
COPY data/ /app/data
WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]
