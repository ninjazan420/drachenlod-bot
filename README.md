![draaaaa](https://github.com/user-attachments/assets/8c0f4ec0-e1ab-42be-a0aa-a2c08841a916)

# [Aktueller invitelink](https://discord.com/oauth2/authorize?client_id=1329104199794954240)

# Drachenlord Discord Bot v5.2.0

## Meddl Loidde!

Dieser Bot scheißt dir zufällige Zitate vom Arschgebirge aus der Schimmelschanze direkt in deinen Discord-Server.

## Features

  ✅ mehr als 500 Soundclips

  ✅ mehr als 100 Zitate

  ❓ Bist du ein Drachi oder ein echter Haider? Teste es im Quiz mit über 150 Fragen!

  🎉 Überraschung alle 30-60 Minuten

# Befehle

## 📋 Basis-Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `!hilfe` | Zeigt diese Hilfe an |
| `!mett` | Zeigt den aktuellen Mett-Level mit Mett-Meter an 🥓 |
| `!zitat` | Der Quallemann antwortet dir mit einem zufälligen Zitat |
| `!lordmeme <text>` | Erstellt ein Drachenlord Meme (Nutze \| für oben/unten) |
| `!lordstats [@user]` | Zeigt lustige Drachenlord-Statistiken für einen Benutzer |
| `!lordupdate` | Zeigt die letzten Bot-Updates und Änderungen |
| `!kontakt` | Sende eine Nachricht an den Admin |

## 🤖 Drachenlord KI

| Befehl | Beschreibung |
|--------|--------------|
| `@username <nachricht>` | Chatte mit dem Bot im Channel |
| `DM` | Du kannst dem Drachenlord auch eine DM schreiben und privat chatten! |

> **Hinweis:** Die KI-Features sind für alle Nutzer kostenlos verfügbar. Admins können den Zugriff einzelner User mit `!butteriq disable/enable <user_id>` verwalten.

## 🔊 Sound-Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `!lord` | Zufälliges GESCHREI im Voice-Channel |
| `!cringe` | Zufälliger Cringe-Sound wenn's mal wieder zu viel wird |
| `!sounds` | Zeigt eine durchblätterbare Liste aller verfügbaren Sounds |
| `!sound <name>` | Spielt den angegebenen Sound ab |

## ❓ Quiz-Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `!lordquiz` | Zeigt Informationen zum Quiz |
| `!lordquiz start X` | Startet ein Quiz mit X Runden (1-20) |
| `!lordquiz stop` | Beendet das aktuelle Quiz im Channel |

## 🔀 Slash-Befehle

Viele Befehle sind auch als Slash-Commands verfügbar! Tippe einfach `/` in Discord und wähle den gewünschten Befehl aus:

| Slash-Befehl | Beschreibung |
|--------------|--------------|
| `/lordstats [@user]` | Zeigt lustige Drachenlord-Statistiken |
| `/lordupdate` | Zeigt die letzten Bot-Updates |

## ⚙️ Admin-Befehle

### Server-Verwaltung
| Befehl | Beschreibung |
|--------|--------------|
| `!drache server [page]` | Zeigt Server-Liste & Nutzerstatistiken mit fortlaufenden IDs |
| `!drache leave <server_id> [message_id] [grund...]` | Bot von einem Server entfernen |
| `!drache ban server <server_id> [grund...]` | Server bannen (ohne zu verlassen) |
| `!drache unban server <ban_id>` | Ban für einen Server aufheben |
| `!drache bans server` | Liste aller gebannten Server anzeigen |

### User-Verwaltung
| Befehl | Beschreibung |
|--------|--------------|
| `!drache ban user <user_id> [server_id] [grund...]` | User bannen (global oder serverspezifisch) |
| `!drache unban user <ban_id>` | Ban für einen User aufheben |
| `!drache bans user` | Liste aller gebannten User anzeigen |
| `!antwort <message_id> <text>` | Antwortet auf Kontaktnachrichten von Nutzern |
| `!butteriq disable/enable <user_id>` | KI-Zugriff für User verwalten |

### System-Befehle
| Befehl | Beschreibung |
|--------|--------------|
| `!buttergolem stats` | Bot-Statistiken mit Neofetch-Style anzeigen |
| `!ping` | Zeigt die Bot-Latenz an |
| `!servercount` | Manuelles Servercounter-Update durchführen |
| `!id` | Zeigt die IDs des aktuellen Text- & Voice-Channels |

## Installation & Selbst hosten

- [Im Discord Developer Portal Golem hinzufügen](https://discord.com/developers/)
- in der [docker-compose.yml](https://github.com/ninjazan420/drachenlord-bot/blob/master/docker-compose.yml) den Bot-Token, Log Channel ID und Admin ID hinzufügen
- Entscheiden, ob der Bot alle 30-60 Minuten zufällig dem größten Kanal beitreten soll (`ENABLE_RANDOM_JOINS: "False"/"True"`)
- `docker compose build`, gefolgt von `docker compose up -d`
- Logs können per `docker compose logs -f` abgerufen werden

### Modulare Struktur

Der Bot ist modular aufgebaut. Jede Hauptfunktion befindet sich in einer eigenen Datei im `src/` Ordner:

- `main.py` - Hauptdatei mit Bot-Setup und Basislogik
- `hilfe.py` - Hilfe-Kommandos und Dokumentation
- `sounds.py` - Sound-bezogene Befehle und Funktionen
- `quiz.py` - Quiz-System und Spiellogik
- `admins.py` - Admin-Befehle, Ban-System und Server-Verwaltung
- `lordmeme.py` - Meme-Generator und Befehle
- `lordstats.py` - Lustige Drachenlord-Statistiken für User
- `updates.py` - Update-Changelog und Versionsinformationen
- `ki.py` - KI-Integration und Chat-Funktionen
- `butteriq.py` - KI-Zugriffsverwaltung und Unterstützer-System
- `servercounter.py` - Server-Tracking und Statistiken

Um neue Funktionen hinzuzufügen:

1. Erstelle eine neue Datei `src/meine_funktion.py`
2. Implementiere deine Befehle in einer `register_commands()` Funktion
3. Importiere und registriere das Modul in `main.py`

Diese Struktur macht es einfach, den Bot zu erweitern ohne bestehenden Code ändern zu müssen.

> Der Bot muss die Berechtigung besitzen, in den Voice zu joinen!

<sup>*Wichtig: da GitHub die Sounddateien wegen DMCA runter genommen hat, sind diese nur über den Bot direkt verfügbar! Falls du den Bot selbst hosten willst und die Sounds brauchst, schreib mir eine nachricht im discord `ninjazan420`</sup>
