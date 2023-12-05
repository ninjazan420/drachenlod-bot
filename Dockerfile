FROM gorialis/discord.py:3.9.4-minimal

COPY src/ /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]
