![draaaaa](https://github.com/user-attachments/assets/8c0f4ec0-e1ab-42be-a0aa-a2c08841a916)

# Drachenlord Discord Bot

## [Aktueller invitelink](https://discord.com/oauth2/authorize?client_id=1329104199794954240)

## Meddl Loidde! 

Dieser Bot scheißt dir zufällige Zitate vom Arschgebirge aus der Schimmelschanze direkt in deinen Discord-Server.

Sobald der Suppengumbo auf deinem Server online ist, kannst du ihn mit `!lord` heraufbeschwören. Funktioniert das in allen Text- und Voice-Channels.
Für ein Zufallszitat, einfach `!zitat` eingeben

## Features

  ✅ mehr als 500 Soundclips

  ✅ mehr als 100 Zitate

  🎉 Überraschung alle 30-60 Minuten

  # Befehle

| Befehl		| Beschreibung |
| ------------- | ------------- |
| `!lord`       | Der Kotmidas joint in deinen VoiceChannel und schreit irgendein wirres Zeug |
| `!zitat`      | Der Quallemann antwortet dir mit einem Zitat seinerseits |
| `!meddl`      | Na was wohl |
| `!cringe`      | Wenn dein mate mal wieder cringe war, schmeiß ihm einen random cringe sound entgegen |
| `!id`		    | Zeigt dir die ID deines Text- & VoiceChannels|
| `!help`		    | Der Hilfe-Command. Aktuelle Version, Kontaktinfos und mehr|
| `!server`		    | Admin: listet alle Server auf, auf dem der Golem vor sich hin schimmelt|
| `!user`		    | Admin: zählt alle user und online-user auf jedem Server auf dem sich deine Instanz befindet|

## Installation

- [Im Discord Developer Portal Golem hinzufügen](https://discord.com/developers/)
- in der [docker-compose.yml](https://github.com/ninjazan420/drachenlord-bot/blob/master/docker-compose.yml) den Bot-Token, Log Channel ID und Admin ID hinzufügen
- Entscheiden, ob der Bot alle 30-60 Minuten zufällig dem größten Kanal beitreten soll (`ENABLE_RANDOM_JOINS: "False"/"True"`)
- `docker compose build`, gefolgt von `docker compose up -d`
- Logs können per `docker compose logs -f` abgerufen werden

<sup>*Wichtig: da GitHub die Sounddateien wegen DMCA runter genommen hat, sind diese nur über den Bot direkt verfügbar! Falls du den Bot selbst hosten willst und die Sounds brauchst, schreib mir eine nachricht im discord `ninjazan420`</sup>
