# 📋 ButterGolem Changelog

## Version 6.1.0 - Admin Command Visibility & Changelog Fix (04. Juli 2025)

### 🔒 Neue Features

#### **Admin Command Visibility Fix**
- ✅ Admin Commands sind jetzt für normale User unsichtbar
- ✅ Implementierung von `@app_commands.default_permissions(administrator=True)`
- ✅ Verbesserte User Experience - keine Verwirrung mehr durch sichtbare aber nicht ausführbare Commands
- ✅ Native Discord Permission System Integration

#### **Changelog System Wiederhergestellt**
- ✅ `/changelog [version]` Command funktioniert wieder
- ✅ Entfernung des redundanten `/lordupdate` Commands
- ✅ Vollständige Versionhistorie verfügbar
- ✅ Detaillierte Changelog-Ansicht für spezifische Versionen

#### **🐉 Drachigotchi - Das ultimative Tamagotchi-Spiel!**
- ✅ **Komplettes Tamagotchi-System** - Virtuelles Drachenlord-Haustier
- ✅ **Persistent Storage** - Fortschritt wird automatisch gespeichert
- ✅ **Level & Skill System** - Sammle Erfahrung und verbessere deine Fähigkeiten
- ✅ **Inventar & Equipment** - Sammle Items, Waffen und Ausrüstung
- ✅ **Reise-System** - Erkunde 10+ verschiedene Orte mit Dropdown-Menüs
- ✅ **Job-System** - Arbeite als Streamer, Mett-Verkäufer oder Schanze-Wächter
- ✅ **Quest-System** - Erfülle Aufgaben und sammle Belohnungen
- ✅ **Achievement-System** - Sammle Erfolge und werde zum ultimativen Drachenlord
- ✅ **Random Events** - Erlebe zufällige Ereignisse während des Spiels
- ✅ **Kampf-System** - Kämpfe gegen Hater und verdiene Ruhm
- ✅ **Stream-System** - Verdiene Geld und Ruhm durch Streaming
- ✅ **Craft-System** - Erstelle neue Items aus Materialien

### 🔧 Bug Fixes

#### **Permission & Visibility Issues**
- ✅ Admin Commands werden nicht mehr in der Slash Command Liste für normale User angezeigt
- ✅ Changelog Commands sind wieder funktional
- ✅ Command Registration Issues behoben
- ✅ Verbesserte Permission Handling für alle Admin-Funktionen

### ⚙️ Technische Änderungen

#### **Command System Updates**
- ✅ `@app_commands.default_permissions(administrator=True)` zu allen Admin Commands hinzugefügt
- ✅ `register_update_commands` in main.py wieder aktiviert
- ✅ `ChangelogCog` Registration in main.py hinzugefügt
- ✅ Redundanten `/lordupdate` Command aus updates.py entfernt
- ✅ Version Strings in slash_commands.py und main.py auf 6.1.0 aktualisiert

#### **Neue Drachigotchi Commands**
- `/gotchi start <name>` - Erstelle dein persönliches Drachigotchi
- `/gotchi status` - Zeige deinen aktuellen Status mit ASCII-Art
- `/gotchi hilfe` - Komplette Spielanleitung mit allen Commands
- `/gotchi essen` - Iss Essen aus deinem Inventar (Dropdown-Menü)
- `/gotchi kaufen` - Kaufe Items in lokalen Shops (Dropdown-Menü)
- `/gotchi reisen` - Reise zu verschiedenen Orten (Dropdown-Menü)
- `/gotchi erkunden` - Erkunde deinen aktuellen Ort für Belohnungen
- `/gotchi streamen` - Streame um Geld und Ruhm zu verdienen
- `/gotchi arbeiten` - Arbeite in deinem Job um Geld zu verdienen
- `/gotchi quests` - Zeige verfügbare und aktive Quests
- `/gotchi achievements` - Schaue deine Erfolge an
- `/gotchi craft` - Erstelle neue Items aus Materialien
- `/gotchi inventar` - Schaue in dein Inventar
- `/gotchi job` - Nimm Jobs an oder kündige
- `/gotchi ausrüsten` - Rüste Ausrüstung und Items aus
- `/gotchi freilassen` - Lass dein Drachigotchi frei (⚠️ permanent!)

#### **Betroffene Admin Commands**
- `/server` - Server-Liste & Statistiken (Admin)
- `/servercount` - Manuelles Servercounter-Update (Admin)
- `/antwort` - Admin-Antwort senden (Admin)
- `/debug_sounds` - Sound-System Debug (Admin)
- `/butteriq` - ButterIQ Management (Admin)
- `/global` - Globale Nachrichten (Admin)
- `/message` - Direkte Nachrichten (Admin)
- `/memory` - Memory-System Verwaltung (Admin)

---

## Version 6.0.0 - Das große Update (2025)

### 🚀 Neue Features

#### **Komplette Slash Command Migration**
- ✅ Alle `!` Prefix Commands entfernt
- ✅ 15+ neue Slash Commands implementiert
- ✅ Moderne Discord-Integration mit Auto-Complete
- ✅ Ephemeral Responses für bessere UX

#### **Intent-freie Architektur**
- ✅ Keine privilegierten Intents mehr benötigt
- ✅ Optimiert für 100+ Server
- ✅ Bessere Performance und Stabilität
- ✅ Reduzierter Ressourcenverbrauch

#### **Erweiterte KI-Features**
- ✅ Massiv erweiterte Drachenlord Lore (2024/2025)
- ✅ Intelligentere Chat-Antworten
- ✅ Kontextbewusste Konversationen
- ✅ Authentische Persönlichkeit

#### **Sound-System Upgrade**
- ✅ 500+ Soundclips organisiert und optimiert
- ✅ Intelligentes Sound-Caching
- ✅ Verbesserte Playback-Qualität
- ✅ `/sound` Command mit Auto-Complete

#### **Admin-Tools & Statistiken**
- ✅ Memory-System für persistente Daten
- ✅ Neofetch-Style animierte Statistiken
- ✅ Erweiterte Debug-Funktionen
- ✅ Global Messaging System
- ✅ Ban-Management für User und Server

#### **Community Features**
- ✅ Ko-fi Integration für Spenden
- ✅ Verbesserte Hilfe-Systeme
- ✅ Privacy Policy Integration
- ✅ Kontakt-Informationen

### 🔧 Technische Verbesserungen

#### **Code-Architektur**
- ✅ Modulare Struktur mit sauberer Trennung
- ✅ Admin-Module in eigenem Ordner
- ✅ KI-Daten strukturiert in JSON-Dateien
- ✅ Verbesserte Error-Behandlung

#### **Performance**
- ✅ Entfernung von Message Content Intent
- ✅ Effiziente Embed-Generierung
- ✅ Optimierte Datenbank-Zugriffe
- ✅ Reduzierte API-Calls

#### **Deployment**
- ✅ Docker-Container optimiert
- ✅ Environment Variables für Konfiguration
- ✅ Verbesserte Logging-Systeme
- ✅ Automatische Command-Synchronisation

### 💥 Breaking Changes

#### **Command Migration**
- ❌ Alle `!drache` Commands entfernt
- ✅ Neue Syntax: `/drache stats` statt `!drache stats`
- ✅ Alle Commands jetzt als Slash Commands verfügbar

#### **Bot Permissions**
- ❌ Message Content Intent nicht mehr benötigt
- ✅ Reduzierte Berechtigungsanforderungen
- ✅ Bessere Sicherheit durch weniger Intents

### 📊 Neue Slash Commands

#### **Nutzer Commands**
- `/drache stats` - Erweiterte Bot-Statistiken
- `/drache neofetch` - Animierte System-Informationen
- `/sound [name]` - Spezifischen Sound abspielen
- `/sounds` - Alle verfügbaren Sounds anzeigen
- `/lord` - Zufälligen Sound abspielen
- `/zitat` - Drachenlord Zitat
- `/mett` - Mett-Meme
- `/lordmeme` - Zufälliges Meme
- `/quiz` - Quiz starten
- `/ping` - Bot-Latenz prüfen
- `/hilfe` - Hilfe-System
- `/kontakt` - Kontakt-Informationen
- `/privacy` - Datenschutz-Informationen

#### **Admin Commands**
- `/memory [add/remove/list]` - Memory-System verwalten
- `/servercount` - Server-Anzahl anzeigen
- `/server [info/list]` - Server-Informationen
- `/antwort [message]` - Global Message senden
- `/debug_sounds` - Sound-System debuggen
- `/butteriq [user]` - User-Statistiken
- `/global [message]` - Globale Nachricht

### 🐛 Bug Fixes

- ✅ Voice Channel Verbindungsprobleme behoben
- ✅ Memory Leaks in Sound-System gefixt
- ✅ Rate Limiting verbessert
- ✅ Error Handling für alle Commands
- ✅ Embed-Formatierung korrigiert
- ✅ Unicode-Probleme in Texten behoben

### 📚 Dokumentation

- ✅ README.md komplett überarbeitet
- ✅ Alle neuen Commands dokumentiert
- ✅ Installation-Guide aktualisiert
- ✅ Migration-Guide für v5.x Nutzer
- ✅ Docker-Setup verbessert
- ✅ Entwickler-Dokumentation erweitert

### 🎯 Migration von v5.x

#### **Für Server-Admins:**
1. Bot neu einladen mit aktualisierten Permissions
2. Alte `!` Commands durch `/` Commands ersetzen
3. Admin-Commands testen und konfigurieren

#### **Für Nutzer:**
1. Neue Slash Commands verwenden
2. Auto-Complete für einfachere Bedienung
3. Ephemeral Responses für private Antworten

### 🔮 Ausblick v6.2.0

- 🔄 Web-Dashboard für Server-Einstellungen
- 🎮 Erweiterte Quiz-Modi
- 🎵 Custom Sound-Upload für Premium
- 🔗 Webhook-Integration
- 📊 Erweiterte Statistik-Dashboards

---

## Version 5.4.0 und früher

*Für ältere Versionen siehe Git-History*

---

**Support:** [Ko-fi](https://ko-fi.com/buttergolem) | **Issues:** [GitHub](https://github.com/ninjazan420/drachenlod-bot) | **Discord:** [Support Server](https://discord.gg/buttergolem)
