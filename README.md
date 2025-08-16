# 🧈 Buttergolem - Der Drachenlord Discord Bot

[![Discord](https://img.shields.io/discord/1085838744176820244?color=black&label=Discord&logo=discord&logoColor=black)](https://discord.gg/buttergolem)
[![Python](https://img.shields.io/badge/Python-3.9%2B-black?logo=python&logoColor=black)](https://www.python.org/)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.3%2B-black?logo=discord&logoColor=black)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-GNU%20v3-black.svg)](https://opensource.org/licenses/GPL-3.0)
[![Version](https://img.shields.io/badge/Version-6.2.0-black.svg)](CHANGELOG.md)
[![Monero](https://img.shields.io/badge/Support-Monero-black?logo=monero&logoColor=black)](488jjkw5ZmcCgQdUKJ9AYUCqWhJtARpeHXFjHvjTeMt8VzqyKeFdLTYWhbcgUUfgxo2XJy43oRWwGCywJac8s2Jp6fRgYpH)

## 🚀 Was ist neu in v6.2.0?

### 🎮 Gaming Update - Hangman & Snake + AI Memory System
- **Hangman-Spiel** - Wortratespiel 
- **Snake-Spiel** - Klassisches Snake Ascii
- **AI Memory System** - KI kann sich jetzt an vorherige Gespräche erinnern
- **Performance-Optimierungen** - Stats-System deutlich verbessert und Memory-Leaks behoben
- **Gaming-Kategorie** - Neue Hilfe-Sektion mit allen verfügbaren Spielen
- **Persistente Speicherung** - Spielstände und Highscores werden dauerhaft gespeichert

## 🎯 Features

### 🎮 Slash Commands
Alle Commands sind als moderne Slash Commands verfügbar - keine Prefixe mehr nötig!

#### Nutzer Commands
- `/drache stats` - Detaillierte Bot-Statistiken
- `/drache neofetch` - Animierte System-Informationen im Terminal-Stil
- `/drache system` - System-Informationen anzeigen
- `/drache minimal` - Minimale Statistiken
- `/drache rainbow` - Regenbogen-farbene ASCII-Art
- `/drache drachenlord` - Drachenlord ASCII-Art
- `/drache shrek` - Shrek ASCII-Art
- `/drache butteriq` - ButterIQ Management (Admin)
- `/sound [name]` - Spezifischen Sound abspielen
- `/sounds` - Alle verfügbaren Sounds anzeigen
- `/lord` - Zufälligen Drachenlord Sound
- `/zitat` - Zufälliges Drachenlord Zitat
- `/mett` - Mett-Meme
- `/lordmeme [text] [position]` - Drachenlord Meme erstellen
- `/quiz [runden]` - Drachenlord Quiz starten (1-20 Runden)
- `/ping` - Bot-Latenz prüfen
- `/hangman` - Starte ein Hangman-Spiel
- `/hangman_ranking` - Starte ein Hangman-Spiel
- `/sl` - Drachenlord Donkey Kong Animation
- `/snake` - Drachenlord Snake Spiel
- `/gotchi hilfe` - Drachigotchi Spiel-Anleitung
- `/hilfe` - Komplette Hilfe mit allen Commands
- `/kontakt` - Kontakt-Informationen
- `/privacy` - Datenschutzerklärung

#### Admin Commands
- `/admin memory [action] [user_id] [data]` - Memory-System verwalten (list/show/add/delete)
- `/admin servercount` - Server-Anzahl anzeigen
- `/admin server [info/list]` - Server-Informationen
- `/admin ban [typ] [target_id] [reason]` - Server oder User bannen
- `/admin antwort [message]` - Global Message senden
- `/admin debug_sounds` - Sound-System debuggen
- `/admin butteriq [action] [user]` - ButterIQ Management (enable/disable/status)
- `/admin global [message]` - Globale Nachricht senden

### 🧠 KI-Chat Features
- **Erweiterte Drachenlord Lore** - Aktuelle Informationen bis 2024/2025
- **Kontextbewusste Antworten** - Versteht den Gesprächskontext
- **Authentische Persönlichkeit** - Echter Drachenlord-Style
- **Memory-System** - Merkt sich wichtige Informationen

### 🎵 Sound System
- **500+ Soundclips** - Organisiert und optimiert
- **Intelligentes Caching** - Schnelle Ladezeiten
- **Auto-Complete** - Einfaches Finden von Sounds
- **Hohe Qualität** - Optimierte Audio-Dateien

### 📊 Statistiken
- **Neofetch-Style** - Animierte System-Informationen
- **Real-time Updates** - Live-Statistiken
- **Server-Übersicht** - Alle verbundenen Server
- **Performance-Metriken** - Bot-Health Monitoring

## 🛠️ Installation

### Docker (Empfohlen)
```bash
git clone https://github.com/ninjazan420/buttergolem-bot.git
cd buttergolem-bot
cp docker-compose example.yml docker-compose.yml
# docker-compose.yml mit deinen Werten anpassen
docker-compose up -d
```

### Manuelle Installation
```bash
git clone https://github.com/ninjazan420/buttergolem-bot.git
cd buttergolem-bot
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows

pip install -r requirements.txt
cp .env.example .env
# .env mit deinen Werten anpassen

python src/main.py
```

## 🎯 Migration von v5.x

### Für Server-Admins
1. Bot mit aktualisierten Permissions neu einladen
2. Alte `!` Commands durch `/` Commands ersetzen
3. Admin-Commands testen und konfigurieren

### Für Nutzer
1. Neue Slash Commands verwenden
2. Auto-Complete für einfachere Bedienung nutzen
3. Ephemeral Responses für private Antworten

## 📋 Systemanforderungen

- **Python**: 3.9 oder höher
- **Discord.py**: 2.3 oder höher
- **Intents**: Keine privilegierten Intents nötig
- **Speicher**: Mindestens 2GB RAM
- **Speicherplatz**: 500MB für Sounds und Daten

## 🔧 Konfiguration

### Docker Compose
```yaml
services:
  buttergolem:
    build: .
    volumes:
      - ./data:/app/data # Persistent storage for game data

    environment:
      DISCORD_API_TOKEN: "Discord Token API" # Discord Bot-Token
      ENABLE_RANDOM_JOINS: "False" # Enables random joins on the biggest VC
      BLACKLISTED_GUILDS: "123456,654321" # Comma seperated

      ADMIN_USER_ID: "123123123" # CAREFUL also able to use Admin commands

      # Mongodb

      MONGODB_CONNECTION_STRING: "mongodb+srv://your:string@databasename.randomstring.mongodb.net/?retryWrites=true&w=majority&appName=YOURAPPNAME"
      MONGODB_DATABASE_NAME: "Your app Name"
      MONGODB_TIMEOUT: "5000"
      MONGODB_POOL_SIZE: "50"
      ENABLE_MONGODB: "false"  # Feature flag - Wenn deaktiviert wird alles in Json gerendert

      # Router Keys

      OPENROUTER_KEY: "Open Router Key"
      VOID_API_KEY: "Void.ai Key"

      # Channel spoecific

      LOGGING_CHANNEL: "Your Logging Channel ID" # Logging Channel ID
      CHAT_MIRROR_CHANNEL: "Chat Mirror Channel"
      MEMBER_COUNTER_SERVER: "Membercounter Voice Channel Server"

      # etc. 

      DISCORDS_KEY: "Discords server counter api key" # will work without
      TOPGG_KEY: "top.gg key" # will work without

      # Monero Wallet für Spenden
      
      MONERO_SPENDEN_ID: "Your Monero Wallet"

```

## 🎮 Verwendung

### Erste Schritte
1. Bot zu deinem Server einladen
2. `/hilfe` für die vollständige Command-Liste
3. `/lord` für einen zufälligen Sound
4. `/drache stats` für Bot-Statistiken

### Sound-System
- `/sounds` zeigt alle verfügbaren Sounds
- `/sound [name]` spielt einen spezifischen Sound
- Auto-Complete hilft beim Finden

### Admin-Funktionen
- Nur für Bot-Admins verfügbar
- Detaillierte Hilfe mit `/hilfe`
- Sichere Permission-Systeme

## 📱 Support

- **Discord**: [Support Server](https://discord.gg/8A9HHpnfW7)
- **GitHub**: [Issues & Feature Requests](https://github.com/ninjazan420/drachenlod-bot/issues)
- **Monero**: 488jjkw5ZmcCgQdUKJ9AYUCqWhJtARpeHXFjHvjTeMt8VzqyKeFdLTYWhbcgUUfgxo2XJy43oRWwGCywJac8s2Jp6fRgYpH 
- **Email**: drache@f0ck.org

## 🤝 Beitragen

1. Fork das Repository
2. Erstelle einen Feature Branch
3. Commit deine Änderungen
4. Push zum Branch
5. Erstelle einen Pull Request

## 📄 Lizenz

Dieses Projekt ist unter der GNU General Public License v3 lizenziert. Siehe [LICENSE](LICENSE) für Details.

## 🙏 Danksagung

- **Drachenlord** - Für die Inspiration
- **Discord.py Community** - Für die großartige Library
- **Alle Unterstützer** - Für die großzügigen Spenden
- **Community** - Für Feedback und Feature-Ideen

---

**Made with ❤️ by the Buttergolem Team**
