FROM gorialis/discord.py

COPY src/ /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]
