
# Drachenlord Discord Bot

  

## Meddl Loide! 

  

Dieser Bot[^1] scheißt dir zufällige Zitate vom Arschgebirge aus der Schimmelschanze direkt in deinen Discord-Server.

  

Sobald der Suppengumbo auf deinem Server online ist, kannst du ihn mit `!lord` heraufbeschwören. Je nachdem welche API-Permissions du gesetzt hast, funktioniert das in allen Text- und Voice-Channels (mehr dazu unter [Installation](#installation)).


## TL;DR

#### [Support Server!](https://discord.gg/7J4mgSyB8n)



## Features

  ✅ mehr als 500 Soundclips

  ✅ mehr als 100 Zitate

  🎉 Überraschung alle 30-60 Minuten

![Drachenlord Chat](https://i.imgur.com/IGtD0VS.png)

  

# Befehle

| Befehl		| Beschreibung |
| ------------- | ------------- |
| `!lord`       | Der Kotmidas joint in deinen VoiceChannel und schreit irgendein wirres Zeug |
| `!zitat`      | Der Quallemann antwortet dir mit einem Zitat seinerseits |
| `!meddl`      | Na was wohl |
| `!cringe`      | Wenn dein mate mal wieder cringe war, schmeiß ihm einen random cringe sound entgegen |
| `!id`		    | Zeigt dir die ID deines Text- & VoiceChannels|

  

Für einige mp3s gibt es eigene commands :) Mit `!help` siehst du alle verfügbaren commands.

  

# Hinzufügen von Sounds / Namen / Zitaten / Befehlen

Die Namen und Zitate sind in [json-files](./src/data/) gespeichert - du kannst diese beliebig ändern (PRs welcome).

  

Alle mp3-Dateien, die in [./src/data/clips/](./src/data/clips/) liegen, werden automatisch in die Zufallswiedergabe aufgenommen. Du kannst dir auch commands für einzelne Dateien bauen, siehe [main.py#193](./src/main.py#193).

  

Der Docker-Container muss nach allen Änderungen neu gebaut werden.

# Installation

  

## Konfiguration

### API Token

Damit der Karamellkaiser deinem Discord-Server joint, musst du ein API-Token erstellen und ihn zu deinem Server einladen. Wie das funktioniert lernst du hier (5min):

  

https://discordpy.readthedocs.io/en/latest/discord.html

  

Nachdem du einen Discord-Bot erstellt hast und ihn auf deinen Server eingeladen hast, bekommst du mit "Click to reveal token" ein API-Token.

  

Dieses musst du jetzt in deiner [docker-compose.yml](./docker-compose.yml#L6) hinterlegen.

  

### Random Joins

Der Popcornpapst wird alle 30-60 Minuten (Zufallswert) auf dem VoiceChannel mit den derzeit meisten Membern einen zufälligen Spruch lassen.

  

Wenns dich nervt kannst du das in deiner [docker-compose.yml](./docker-compose.yml#L7) deaktivieren ;D

  

### TextChannel-Logging

Zum Debuggen kannst du in deiner [docker-compose.yml](./docker-compose.yml#L8) eine TextChannel ID angeben, in den dann einige Infos geloggt werden. Um die ID eines Channels herauszufinden, kannst du `!id` benutzen.

  

## Docker Container starten

As simple as: `docker-compose build && docker-compose up -d`

[^1]:Der Bot wurde [IQNeoXen](https://github.com/IQNeoXen/drachenlord-discord-bot) geschrieben, aber er scheint gestorben zu sein. Da das Projekt zu schade ist um fallen zu lassen, habe ich ihn geklaut und entwickle ihn weiter. @IQNeoXen, wenn du das siehst und dir passt es nicht (adde halt ne Lizenz du doofkopf), dann schreib mir ne mail. 
