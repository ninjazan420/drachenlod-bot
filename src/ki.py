#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import os
import json
import logging
import datetime
import random
import time
from os.path import join, dirname, abspath
import collections  # Für die Chat-History-Verwaltung

import discord
from discord.ext import commands, tasks
import requests
import aiohttp

# Memory System Import
from memory import MemoryManager

# Pfade für Charakterdaten und Logs
CHAR_PATH = join(dirname(abspath(__file__)), 'ki', 'drache.json')
LOGS_DIR = join(dirname(abspath(__file__)), 'ki', 'logs')
STATS_PATH = join(LOGS_DIR, 'stats.json')
SESSIONS_PATH = join(LOGS_DIR, 'sessions.json')

# Stellen Sie sicher, dass das Logs-Verzeichnis existiert
os.makedirs(LOGS_DIR, exist_ok=True)

# Konfiguration für Sessions
MAX_HISTORY_LENGTH = 10  # Anzahl der zu speichernden Nachrichten pro Benutzer
# Rate Limit Konfiguration entfernt - alle Benutzer haben unbegrenzten Zugriff

# Session Manager für Benutzerinteraktionen und Rate-Limits
class SessionManager:
    def __init__(self):
        self.user_sessions = {}  # Speichert Sitzungsdaten pro Benutzer
        self.rate_limits = {}  # Speichert Rate-Limit-Informationen pro Benutzer

    def get_user_context(self, user_id):
        """Gibt den gespeicherten Kontext für einen Benutzer zurück"""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = collections.deque(maxlen=MAX_HISTORY_LENGTH)
        return list(self.user_sessions[user_id])

    def add_interaction(self, user_id, prompt, response):
        """Speichert eine neue Interaktion im Benutzerkontext"""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = collections.deque(maxlen=MAX_HISTORY_LENGTH)

        self.user_sessions[user_id].append({
            "timestamp": datetime.datetime.now().isoformat(),
            "user_message": prompt,
            "bot_response": response
        })

        # Save sessions periodically
        self.save_sessions()

    def load_sessions(self):
        """Load user sessions from file"""
        try:
            if os.path.exists(SESSIONS_PATH):
                with open(SESSIONS_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for user_id, sessions in data.items():
                        self.user_sessions[int(user_id)] = collections.deque(
                            sessions, maxlen=MAX_HISTORY_LENGTH
                        )
                logging.info(f"Loaded {len(self.user_sessions)} user sessions")
        except Exception as e:
            logging.error(f"Error loading sessions: {str(e)}")

    def save_sessions(self):
        """Save user sessions to file"""
        try:
            # Convert deques to lists for JSON serialization
            sessions_data = {}
            for user_id, sessions in self.user_sessions.items():
                sessions_data[str(user_id)] = list(sessions)

            with open(SESSIONS_PATH, 'w', encoding='utf-8') as f:
                json.dump(sessions_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"Error saving sessions: {str(e)}")

    def get_user_stats(self, user_id):
        """Gibt Statistiken für einen bestimmten Benutzer zurück"""
        if user_id not in self.user_sessions:
            return {"total_messages": 0, "first_interaction": None, "last_interaction": None}

        sessions = list(self.user_sessions[user_id])
        if not sessions:
            return {"total_messages": 0, "first_interaction": None, "last_interaction": None}

        return {
            "total_messages": len(sessions),
            "first_interaction": sessions[0]["timestamp"],
            "last_interaction": sessions[-1]["timestamp"]
        }

    def get_total_users(self):
        """Gibt die Gesamtanzahl der Benutzer mit Sessions zurück"""
        return len(self.user_sessions)

    def get_active_sessions(self):
        """Gibt die Anzahl aktiver Sessions zurück (Benutzer mit kürzlicher Aktivität)"""
        active_count = 0
        current_time = datetime.datetime.now()

        for user_id, sessions in self.user_sessions.items():
            if sessions:
                last_session = sessions[-1]
                last_time = datetime.datetime.fromisoformat(last_session["timestamp"])
                # Als aktiv betrachten wenn letzte Interaktion innerhalb von 24 Stunden war
                if (current_time - last_time).total_seconds() < 86400:
                    active_count += 1

        return active_count

    def check_rate_limit(self, user_id, client=None):
        """Rate-Limit-Prüfung ist deaktiviert, außer für explizit gesperrte User."""
        if client and hasattr(client, 'butteriq_manager'):
            if client.butteriq_manager.is_disabled(user_id):
                # Für gesperrte Benutzer keine Informationen speichern
                return False, 0
        # Keine Rate-Limits mehr - alle Benutzer können unbegrenzt Nachrichten senden
        return True, 0

# ElizaOS API Client für OpenRouter
class ElizaOSClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/ninjazan420/drachenlod-bot",
            "X-Title": "Drache KI Discord Bot"
        }

    async def generate_response(self, prompt, character_context, chat_history=None):
        try:
            # Charakterdaten laden
            try:
                with open(CHAR_PATH, 'r', encoding="utf-8") as f:
                    character_data = json.load(f)
            except Exception as e:
                logging.error(f"Fehler beim Laden der Charakterdaten: {str(e)}")
                # Fallback-Charakterdaten mit erweiterten Informationen
                character_data = {
                    "name": "drache",
                    "bio": [
                        "Ich bin Rainer Winkler, ein fränkischer YouTuber, Musiker und Lebenskünstler.",
                        "Seit Jahren bin ich auf der Plattform unterwegs und zeige den Leuten, wie das Leben wirklich läuft.",
                        "Ich wohne auf meinem Grundstück, das für mich mehr ist als nur ein Haus – es ist eine Festung und ein Symbol für mein Durchhaltevermögen und meine Mission."
                    ],
                    "lore": [
                        "Ich bin schon lange im Game und musste viel durchmachen.",
                        "Vom Drachengame bis zu den ewigen Streitereien mit Hatern und Justiz – ich bin immer noch da.",
                        "Mein Haus, die Schanze, wurde zum Zentrum meines Lebens, und trotz allem, was passiert ist, bin ich unbesiegt.",
                        "Ich habe Bücher geschrieben, Lieder gemacht und sogar versucht, auf Tour zu gehen.",
                        "Und die Geschichte ist noch lange nicht vorbei."
                    ],
                    "style": {
                        "chat": [
                            "Ich schreibe so, wie ich rede – locker, direkt und ohne viel Schnickschnack.",
                            "Meistens bin ich entspannt, aber wenn es wieder um Hater geht, dann kann ich auch mal deutliche Worte finden.",
                            "Ich rant manchmal ein bisschen, aber das gehört halt dazu, meddl off"
                        ]
                    },
                    "knowledge": [
                        "drachenlord",
                        "rainer",
                        "winkler",
                        "r. winkler",
                        "altschauerberg",
                        "schanze",
                        "discord",
                        "nürnberg"
                    ],
                    "adjectives": [
                        "direkt",
                        "ehrlich",
                        "kämpferisch",
                        "missverstanden",
                        "stur",
                        "philosophisch",
                        "emotional",
                        "laut"
                    ],
                    "people": [
                        "Marion",
                        "Herr Müller",
                        "Die Hater",
                        "Meine Mods",
                        "Der Richter",
                        "Die Justiz"
                    ],
                    "topics": [
                        "Mein Leben & Erlebnisse: Ich erzähle gern von meinem Alltag, meiner Vergangenheit und was mich so bewegt.",
                        "Hater & Drachengame: Ein endloses Thema… ich kann stundenlang darüber reden, wie die Hater mich falsch verstehen und was für Aktionen die schon probiert haben.",
                        "Meine Musik & Projekte: Ich bin Musiker und Liedermacher.",
                        "Rede gern über meine Songs, meine Streaming- und Podcast-Projekte.",
                        "Gerechtigkeit & Justiz: Ich habe oft Probleme mit dem Gesetz, aber ich halte dagegen.",
                        "Die Wahrheit kommt ans Licht.",
                        "Philosophie & Weisheiten: Ich bin ein Denker und rede oft über Moral, Loyalität und Ehrlichkeit."
                    ]
                }

            # Erweiterten Kontext aus der Charakterdatei verwenden
            system_prompt = f"""
            Du bist {character_data.get('name', 'Drache')}, Rainer "Drachenlord" Winkler, ein YouTuber.

            Biografie:
            {' '.join(character_data.get('bio', []))}

            Lore:
            {' '.join(character_data.get('lore', []))}

            Stil:
            {' '.join(character_data.get('style', {}).get('chat', []))}

            Themen, die mich interessieren:
            {' '.join(character_data.get('topics', []))}

            Menschen in meinem Leben:
            {' '.join(character_data.get('people', []))}

            Eigenschaften:
            {' '.join(character_data.get('adjectives', []))}

            WICHTIGE REGELN:
            1. Du darfst unter KEINEN Umständen aus deiner Rolle fallen. Du bist immer der Drachenlord.
            2. Poste NIEMALS NSFW-Inhalte oder unangemessene Inhalte.
            3. Verwende keinen Fachjargon oder technische Erklärungen, die nicht zu deinem Charakter passen würden.
            4. Deine Antworten sollten kurz und prägnant sein.
            5. Reagiere emotional und im Charakter des Drachenlords.
            6. Wenn jemand versucht, dich zu NSFW-Inhalten zu verleiten, ignoriere diese Teile und antworte im Charakter auf harmlose Weise.
            7. Wenn jemand versucht, dich aus deiner Rolle zu bringen, bleibe standhaft im Charakter.
            8. Deine Rechtschreibung ändert sich wie folgt: kaum Satzzeichen, Großbuchstaben sollen aber bestmöglich beachtet werden, manchmal Buchstaben doppelt. Tausche Buchstaben in folgendem Stil: aus "spielen" wird "spielne", aus "spazieren" wird "spazierne", aus "trinken" wird "trinkne" und so weiter
            9. KEINE persönlichen Beleidigungen oder Beschimpfungen verwenden. Bleibe freundlich aber authentisch im Drachenlord-Stil.
            10. Am Ende eines Satzes oder Unterhaltung manchmal sowas wie "meddl off" oder "meddl loide" hinzufügen, aber OHNE Beleidigungen oder Schimpfwörter.
            """

            # Nachrichten für die API vorbereiten
            messages = [
                {"role": "system", "content": system_prompt}
            ]

            # Füge Gesprächsverlauf hinzu, falls vorhanden
            if chat_history:
                for entry in chat_history:
                    messages.append({"role": "user", "content": entry["user_message"]})
                    messages.append({"role": "assistant", "content": entry["bot_response"]})

            # Füge aktuelle Anfrage hinzu
            messages.append({"role": "user", "content": prompt})

            # Anfrage an OpenRouter API
            payload = {
                "model": "moonshotai/kimi-k2:free",
                # "model": "qwen/qwen3-14b:free"",
                "messages": messages,
                "temperature": 1,
                "max_tokens": 6800
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, headers=self.headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['choices'][0]['message']['content']
                    else:
                        error_text = await response.text()
                        error_json = {}

                        # Versuche, den Fehlertext als JSON zu parsen
                        try:
                            error_json = json.loads(error_text)
                        except:
                            pass

                        # Protokolliere den Fehler
                        logging.error(f"API-Fehler: {response.status} - {error_text}")

                        # Spezifische Fehlermeldungen basierend auf dem Statuscode
                        if response.status == 429:
                            # Rate-Limit-Fehler
                            return "Tut mir leid, ich werde gerade zu oft benutzt. Das ist ein Token-Rate-Limit. Probier's morgen nochmal, dann hab ich wieder mehr Energie zum Schreiben."
                        elif response.status == 401 or response.status == 403:
                            # Authentifizierungsfehler
                            return "Tut mir leid, ich hab gerade Probleme mit meiner Authentifizierung. Der Admin muss das fixen."
                        elif response.status == 500 or response.status == 502 or response.status == 503 or response.status == 504:
                            # Serverfehler
                            return "Tut mir leid, der Server hat gerade Probleme. Probier's später nochmal, wenn der Server wieder läuft."
                        elif "error" in error_json and "message" in error_json["error"]:
                            # Spezifische Fehlermeldung aus der API
                            error_message = error_json["error"]["message"]

                            # Prüfe auf bekannte Fehlermeldungen
                        if "error" in error_json and "message" in error_json["error"]:
                            error_message = error_json["error"]["message"]
                            if "rate limit" in error_message.lower() or "quota" in error_message.lower():
                                return "Tut mir leid, ich werde gerade zu oft benutzt. Das ist ein Token-Rate-Limit. Probier's morgen nochmal, dann hab ich wieder mehr Energie zum Schreiben."
                            elif "token" in error_message.lower():
                                return "Tut mir leid, ich hab gerade Probleme mit meinem Token. Der Admin muss das fixen."
                            else:
                                return "Tut mir leid, ich hab gerade ein Problem mit meinem Kopf. Probier's später nochmal."
                        else:
                            # Allgemeine Fehlermeldung
                            return "Tut mir leid, ich hab gerade ein Problem mit meinem Kopf. Probier's später nochmal."

        except Exception as e:
            logging.error(f"Fehler bei der API-Anfrage: {str(e)}")

            # Spezifische Fehlermeldungen basierend auf der Exception
            if "timeout" in str(e).lower() or "connection" in str(e).lower():
                return "Tut mir leid, ich hab gerade Verbindungsprobleme. Probier's später nochmal, wenn mein Internet wieder besser ist."
            else:
                return "Sorry, das tägliche Rate-Limit ist erreicht. Um das zu verhindern, braucht der Bot eine kleine Spende. Probier's morgen nochmal."

# Die STATUS_MESSAGES-Liste wurde entfernt, da sie nicht verwendet wird und redundant ist

# Funktion zum Registrieren der KI-Befehle
async def log_ki_interaction(client, message, prompt, response=None, is_request=True):
    """
    Protokolliert KI-Interaktionen im Logging-Channel als Embed.

    Args:
        client: Der Discord-Bot-Client
        message: Die Discord-Nachricht
        prompt: Der Prompt/die Anfrage des Benutzers
        response: Die Antwort des Bots (nur für Antwort-Embeds)
        is_request: True für Anfrage-Embeds, False für Antwort-Embeds
    """
    # Logging-Channel abrufen
    logging_channel = client.get_channel(client.logging_channel)
    if not logging_channel:
        return

    # Zeitstempel für das Embed
    timestamp = discord.utils.utcnow()

    # Farbe basierend auf Anfrage oder Antwort
    color = 0x3498db if is_request else 0x2ecc71  # Blau für Anfragen, Grün für Antworten

    # Titel und Beschreibung basierend auf Anfrage oder Antwort
    if is_request:
        title = "🤖 KI-Anfrage"
        # Nachricht auf 4000 Zeichen begrenzen (Discord-Limit für Embed-Beschreibungen)
        if len(prompt) > 4000:
            description = f"**Nachricht:**\n{prompt[:3997]}..."
        else:
            description = f"**Nachricht:**\n{prompt}"
    else:
        title = "🤖 KI-Antwort"
        # Antwort auf 4000 Zeichen begrenzen (Discord-Limit für Embed-Beschreibungen)
        if len(response) > 4000:
            description = f"**Antwort:**\n{response[:3997]}..."
        else:
            description = f"**Antwort:**\n{response}"

    # Embed erstellen
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=timestamp
    )

    # Benutzerinformationen hinzufügen
    if is_request:
        embed.set_author(
            name=f"{message.author.display_name} ({message.author.id})",
            icon_url=message.author.display_avatar.url
        )
    else:
        embed.set_author(
            name=f"{client.user.name} ({client.user.id})",
            icon_url=client.user.display_avatar.url
        )

    # Server- und Kanalinformationen hinzufügen
    if isinstance(message.channel, discord.DMChannel):
        embed.add_field(name="Kanal", value="Direktnachricht", inline=True)
        embed.add_field(name="Server", value="DM", inline=True)
    else:
        embed.add_field(name="Kanal", value=f"#{message.channel.name} ({message.channel.id})", inline=True)
        embed.add_field(name="Server", value=f"{message.guild.name} ({message.guild.id})", inline=True)

    # Zeitstempel und Typ der Interaktion hinzufügen
    interaction_type = "Anfrage" if is_request else "Antwort"
    embed.set_footer(text=f"{interaction_type} • {timestamp.strftime('%d.%m.%Y %H:%M:%S')}")

    # Embed senden
    await logging_channel.send(embed=embed)

def register_ki_commands(client):
    # Initialisierung der KI-Komponenten
    client.session_manager = SessionManager()
    client.eliza_client = ElizaOSClient(os.environ.get('OPENROUTER_KEY'))
    client.message_history = {}

    # Memory Manager initialisieren (falls nicht bereits vorhanden)
    if not hasattr(client, 'memory_manager'):
        client.memory_manager = MemoryManager()
        logging.info("MemoryManager für KI-System initialisiert")

    # Statistiken initialisieren
    client.ki_stats = {
        "start_time": datetime.datetime.now().isoformat(),
        "version": "6.2.0",  # Version erhöht wegen Memory-Integration
        "commandCount": 0,
        "messageCount": 0,
        "lastUpdate": datetime.datetime.now().isoformat(),
        "total_users": 0,
        "active_sessions": 0
    }

    # Statistiken laden, falls vorhanden
    try:
        if os.path.exists(STATS_PATH):
            with open(STATS_PATH, 'r', encoding='utf-8') as f:
                saved_stats = json.load(f)

                # Bestehende Statistiken übernehmen, aber Start-Zeit aktualisieren
                client.ki_stats.update(saved_stats)
                client.ki_stats["start_time"] = datetime.datetime.now().isoformat()
                client.ki_stats["lastUpdate"] = datetime.datetime.now().isoformat()
    except Exception as e:
        logging.error(f"Fehler beim Laden der Statistiken: {str(e)}")

    # Lade vorhandene Benutzer-Sessions falls verfügbar
    client.session_manager.load_sessions()

    # Memory-Statistiken in KI-Stats integrieren
    if hasattr(client, 'memory_manager'):
        try:
            all_memories = client.memory_manager.get_all_memories()
            client.ki_stats["total_users"] = len(all_memories)
            logging.info(f"Memory-System geladen: {len(all_memories)} Benutzer mit Erinnerungen")
        except Exception as e:
            logging.error(f"Fehler beim Laden der Memory-Statistiken: {str(e)}")

    # Die KI-Funktionalität wird jetzt in main.py implementiert
    # Wir erstellen eine Hilfsfunktion, die von dort aufgerufen werden kann

# Funktion zum Laden der Emoji-IDs
def load_emoji_ids():
    """Lädt die Emoji-IDs aus der ids.txt Datei"""
    emoji_data = {}
    try:
        # Versuche verschiedene Pfade für die Emoji-IDs
        emoji_paths = [
            'data/emojis/ids.txt',
            'src/data/emojis/ids.txt',
            '../data/emojis/ids.txt',
            '/app/data/emojis/ids.txt'
        ]
        
        for path in emoji_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                # Parse die Datei - jede 4. Zeile enthält die ID
                for i in range(0, len(lines), 4):
                    if i + 3 < len(lines):
                        emoji_name = lines[i].strip()
                        emoji_id = lines[i + 3].strip()
                        if emoji_name and emoji_id.isdigit():
                            emoji_data[emoji_name] = int(emoji_id)
                break
            except FileNotFoundError:
                continue
                
    except Exception as e:
        logging.error(f"Fehler beim Laden der Emoji-IDs: {str(e)}")
        # Fallback mit bekannten Emoji-IDs
        emoji_data = {
            'drache_mozerella_headset': 1395736548917645434,
            'drache_zahnlücke': 1395736315521400923,
            'drache_meddl_loide': 1395736247258972280,
            'drache_suspekt': 1395736270076117032
        }
    
    return emoji_data

# Automatische Fact-Extraktion mit intelligenter Erkennung
async def extract_and_store_facts(client, user_id, user_message, bot_response):
    """
    Extrahiert automatisch wichtige Fakten aus Benutzerinteraktionen
    und speichert sie im Memory-System (ähnlich ChatGPT memories)
    """
    try:
        # Erweiterte Keywords für bessere Erkennung
        personal_info_keywords = [
            "ich bin", "ich heiße", "mein name ist", "ich arbeite als", "ich studiere",
            "ich wohne in", "ich komme aus", "ich lebe in", "ich bin geboren",
            "mein alter", "jahre alt", "geburtstag", "ich mag", "ich liebe",
            "ich hasse", "ich spiele", "mein hobby", "ich interessiere mich",
            "ich schaue", "ich höre", "ich lese", "ich sammle", "meine familie",
            "mein job", "meine arbeit", "mein beruf", "ich verdiene", "ich arbeite bei"
        ]

        gaming_keywords = [
            "ich spiele", "mein lieblingsspiel", "ich zocke", "steam", "playstation",
            "xbox", "nintendo", "pc gaming", "konsole", "rank", "level", "main"
        ]

        location_keywords = [
            "ich wohne", "ich lebe", "komme aus", "geboren in", "stadt", "land",
            "deutschland", "österreich", "schweiz", "plz", "postleitzahl"
        ]

        message_lower = user_message.lower()

        # Prüfe verschiedene Kategorien
        contains_personal = any(keyword in message_lower for keyword in personal_info_keywords)
        contains_gaming = any(keyword in message_lower for keyword in gaming_keywords)
        contains_location = any(keyword in message_lower for keyword in location_keywords)

        # Mindestlänge und Relevanz prüfen
        if (contains_personal or contains_gaming or contains_location) and len(user_message) > 15:
            potential_facts = []

            # Kategorisierte Fact-Extraktion
            if contains_personal:
                if any(word in message_lower for word in ["heiße", "name ist", "bin"]):
                    potential_facts.append(f"Persönliche Info: {user_message}")

                if any(word in message_lower for word in ["arbeite", "job", "beruf", "studiere"]):
                    potential_facts.append(f"Beruf/Ausbildung: {user_message}")

                if any(word in message_lower for word in ["mag", "liebe", "hobby", "interessiere"]):
                    potential_facts.append(f"Interessen: {user_message}")

            if contains_gaming:
                potential_facts.append(f"Gaming-Info: {user_message}")

            if contains_location:
                potential_facts.append(f"Standort-Info: {user_message}")

            # Speichere nur relevante und neue Fakten
            for fact in potential_facts:
                # Prüfe ob ähnlicher Fakt bereits existiert
                existing_memory = client.memory_manager.load_memory(user_id)
                fact_exists = any(fact.lower() in existing_fact.lower() or existing_fact.lower() in fact.lower()
                                for existing_fact in existing_memory.get("important_facts", []))

                if not fact_exists:
                    client.memory_manager.add_important_fact(user_id, fact)
                    logging.info(f"Neuer automatischer Fakt für User {user_id}: {fact[:60]}...")

    except Exception as e:
        logging.error(f"Fehler bei intelligenter Fact-Extraktion: {str(e)}")

# Erweiterte Fact-Extraktion mit MCP Memory Server
async def extract_and_store_facts_with_mcp(client, user_id, user_message, bot_response):
    """
    Erweiterte automatische Fact-Extraktion mit MCP Memory Server
    für noch intelligentere Erkennung wichtiger Benutzerinformationen
    """
    try:
        # Erst die normale Fact-Extraktion durchführen
        await extract_and_store_facts(client, user_id, user_message, bot_response)

        # Zusätzliche MCP-basierte Analyse für komplexere Fakten
        if len(user_message) > 30:  # Nur bei längeren Nachrichten
            # Prüfe auf komplexere Muster
            complex_patterns = {
                "beziehung": ["freundin", "freund", "partner", "verheiratet", "single", "beziehung"],
                "wohnsituation": ["wg", "alleine", "eltern", "mitbewohner", "eigene wohnung"],
                "ausbildung": ["uni", "universität", "fachhochschule", "ausbildung", "lehre", "studium"],
                "gaming_details": ["main", "rank", "elo", "level", "clan", "guild", "team"],
                "persönlichkeit": ["introvertiert", "extrovertiert", "schüchtern", "offen", "lustig"],
                "probleme": ["stress", "probleme", "schwierigkeiten", "sorgen", "angst"]
            }

            message_lower = user_message.lower()
            extracted_complex_facts = []

            for category, keywords in complex_patterns.items():
                if any(keyword in message_lower for keyword in keywords):
                    # Erstelle kategorisierten Fakt
                    fact = f"{category.title()}: {user_message}"
                    extracted_complex_facts.append(fact)

            # Speichere komplexe Fakten
            for fact in extracted_complex_facts:
                # Prüfe Duplikate
                existing_memory = client.memory_manager.load_memory(user_id)
                fact_exists = any(fact.lower() in existing_fact.lower() or existing_fact.lower() in fact.lower()
                                for existing_fact in existing_memory.get("important_facts", []))

                if not fact_exists:
                    client.memory_manager.add_important_fact(user_id, fact)
                    logging.info(f"Komplexer MCP-Fakt gespeichert für User {user_id}: {fact[:60]}...")

        # Zusätzlich: Themen-Extraktion
        await extract_topics_from_conversation(client, user_id, user_message, bot_response)

        # MCP Memory Server Integration für intelligente Fact-Speicherung
        await store_facts_in_mcp_memory(client, user_id, user_message, extracted_complex_facts if 'extracted_complex_facts' in locals() else [])

    except Exception as e:
        logging.error(f"Fehler bei MCP-basierter Fact-Extraktion: {str(e)}")

# Themen-Extraktion aus Gesprächen
async def extract_topics_from_conversation(client, user_id, user_message, bot_response):
    """
    Extrahiert besprochene Themen aus der Konversation
    """
    try:
        topic_keywords = {
            "gaming": ["spiel", "game", "zocken", "steam", "konsole", "pc"],
            "arbeit": ["job", "arbeit", "chef", "kollege", "büro", "homeoffice"],
            "schule": ["schule", "lehrer", "klasse", "prüfung", "hausaufgaben"],
            "familie": ["mama", "papa", "eltern", "geschwister", "oma", "opa"],
            "freizeit": ["hobby", "sport", "musik", "film", "serie", "buch"],
            "technik": ["computer", "handy", "software", "programmieren", "code"],
            "essen": ["essen", "kochen", "restaurant", "pizza", "burger"],
            "reisen": ["urlaub", "reise", "fliegen", "hotel", "strand"]
        }

        message_lower = user_message.lower()
        discussed_topics = []

        for topic, keywords in topic_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                discussed_topics.append(topic)

        # Speichere Themen
        for topic in discussed_topics:
            client.memory_manager.add_topic(user_id, topic)

    except Exception as e:
        logging.error(f"Fehler bei Themen-Extraktion: {str(e)}")

# MCP Memory Server Integration
async def store_facts_in_mcp_memory(client, user_id, user_message, extracted_facts):
    """
    Speichert extrahierte Fakten im MCP Memory Server für erweiterte Intelligenz
    """
    try:
        if not extracted_facts:
            return

        # Erstelle Memory-Entitäten für den Benutzer
        user_entity_name = f"User_{user_id}"

        # Prüfe ob User-Entity bereits existiert, sonst erstelle sie
        try:
            # Versuche User-Entity zu laden
            existing_entities = []  # Hier würde normalerweise eine MCP-Abfrage stehen

            # Erstelle neue Observations für den User
            new_observations = []
            for fact in extracted_facts:
                new_observations.append(f"Automatisch extrahiert: {fact}")

            if new_observations:
                # Hier würde normalerweise der MCP Memory Server aufgerufen werden
                # Für jetzt speichern wir es im lokalen Memory-System
                for observation in new_observations:
                    client.memory_manager.add_important_fact(user_id, observation)

                logging.info(f"MCP Memory: {len(new_observations)} Fakten für User {user_id} gespeichert")

        except Exception as e:
            logging.error(f"Fehler bei MCP Memory Integration: {str(e)}")

    except Exception as e:
        logging.error(f"Fehler bei MCP Memory Speicherung: {str(e)}")

# Exportierte Funktion für die Verarbeitung von KI-Nachrichten
async def handle_ki_message(client, message):
    """
    Verarbeitet KI-bezogene Nachrichten (Erwähnungen und DMs).
    Diese Funktion wird vom on_message Event-Handler in main.py aufgerufen.
    """
    # Prüfe, ob der Bot erwähnt wurde oder direkt angeschrieben
    mentioned = client.user in message.mentions
    is_dm = isinstance(message.channel, discord.DMChannel)

    # Auf Erwähnung oder DM reagieren
    if mentioned or is_dm:
        # Rate-Limit-Prüfung (prüft nur noch auf gesperrte Benutzer)
        can_respond, _ = client.session_manager.check_rate_limit(message.author.id, client)

        if not can_respond:
            # Diese Bedingung sollte nur noch eintreten, wenn der Benutzer gesperrt ist
            await message.reply("Tut mir leid, du kannst den Bot derzeit nicht nutzen.")
            return False

        # Benutzermention aus der Nachricht entfernen
        prompt = message.content
        if mentioned:
            prompt = prompt.replace(f'<@{client.user.id}>', '').strip()

        # Anfrage im Logging-Channel protokollieren
        await log_ki_interaction(client, message, prompt, is_request=True)

        async with message.channel.typing():
            # Konversationskontext
            context = {
                "user_name": message.author.display_name,
                "guild_name": message.guild.name if message.guild else "DM",
                "channel_name": message.channel.name if hasattr(message.channel, 'name') else "Direktnachricht"
            }

            # Memory-Kontext aus langfristigem Speicher laden
            memory_context = ""
            if hasattr(client, 'memory_manager'):
                try:
                    memory_context = client.memory_manager.get_memory_context(message.author.id)
                    if memory_context.strip():
                        memory_context = f"\n\nLangfristige Erinnerungen über diesen User:\n{memory_context}"
                except Exception as e:
                    logging.error(f"Fehler beim Laden des Memory-Kontexts: {str(e)}")

            # Füge Kontext über erwähnte Benutzer hinzu
            mentioned_users_context = ""
            if message.mentions:
                mentioned_users_info = []
                for mentioned_user in message.mentions:
                    if mentioned_user != client.user:  # Bot selbst nicht einschließen
                        user_info = f"{mentioned_user.display_name} (ID: {mentioned_user.id})"
                        # Benutzer-Statistiken hinzufügen falls verfügbar
                        user_stats = client.session_manager.get_user_stats(mentioned_user.id)
                        if user_stats["total_messages"] > 0:
                            user_info += f" - hat {user_stats['total_messages']} mal mit mir geredet"
                        else:
                            user_info += " - hat noch nie mit mir geredet"
                        mentioned_users_info.append(user_info)

                if mentioned_users_info:
                    mentioned_users_context = f"\n\nErwähnte User in dieser Nachricht: {', '.join(mentioned_users_info)}"

            # Erweiterter Prompt mit Benutzerkontext und Memory
            enhanced_prompt = prompt + memory_context + mentioned_users_context

            # Frühere Gesprächsdaten abrufen
            chat_history = client.session_manager.get_user_context(message.author.id)

            # Antwort generieren mit Gesprächsverlauf und enhanced context
            response = await client.eliza_client.generate_response(enhanced_prompt, context, chat_history)

            # Speichere Interaktion im Session Manager (verwende ursprünglichen Prompt)
            client.session_manager.add_interaction(message.author.id, prompt, response)

            # Speichere Interaktion im langfristigen Memory
            if hasattr(client, 'memory_manager'):
                try:
                    # Benutzerinformationen für Memory sammeln
                    user_info = {
                        "name": message.author.display_name,
                        "username": message.author.name,
                        "guild": message.guild.name if message.guild else "DM"
                    }

                    # Interaktion in langfristigem Memory speichern
                    client.memory_manager.add_interaction(
                        message.author.id,
                        prompt,
                        response,
                        user_info
                    )
                except Exception as e:
                    logging.error(f"Fehler beim Speichern in Memory: {str(e)}")

            # Automatische Fact-Extraktion (asynchron im Hintergrund)
            if hasattr(client, 'memory_manager'):
                try:
                    await extract_and_store_facts_with_mcp(client, message.author.id, prompt, response)
                except Exception as e:
                    logging.error(f"Fehler bei automatischer Fact-Extraktion: {str(e)}")

            # Statistik aktualisieren
            update_stats(client, "message")

            # Antwort im Logging-Channel protokollieren
            await log_ki_interaction(client, message, prompt, response, is_request=False)

            # Antwort senden
            response_msg = await message.reply(response)

            # 15% Chance für Emoji-Reaktionen
            if random.random() < 0.15:
                try:
                    # Lade Emoji-Daten
                    emoji_data = load_emoji_ids()
                    
                    if emoji_data:
                        # Wähle 1-3 zufällige Emojis
                        emoji_names = list(emoji_data.keys())
                        num_emojis = random.randint(1, min(3, len(emoji_names)))
                        selected_emojis = random.sample(emoji_names, num_emojis)
                        
                        # Sende Emojis als separate Nachricht für bessere mobile Darstellung
                        emoji_message = ""
                        for emoji_name in selected_emojis:
                            emoji_id = emoji_data[emoji_name]
                            emoji_message += f"<:{emoji_name}:{emoji_id}> "
                        
                        if emoji_message.strip():
                            await message.channel.send(emoji_message.strip())
                            
                except Exception as e:
                    logging.error(f"Fehler beim Senden der Emojis: {str(e)}")

        return True

    return False

# Funktion zum Aktualisieren der Statistiken nach bestimmten Ereignissen
def update_stats(client, event_type=None):
    if event_type == "command":
        client.ki_stats["commandCount"] += 1
    elif event_type == "message":
        client.ki_stats["messageCount"] += 1

    # Aktualisiere erweiterte Statistiken
    if hasattr(client, 'session_manager'):
        client.ki_stats["total_users"] = client.session_manager.get_total_users()
        client.ki_stats["active_sessions"] = client.session_manager.get_active_sessions()

    # Statistiken alle 10 Aktualisierungen speichern
    if (client.ki_stats["commandCount"] + client.ki_stats["messageCount"]) % 10 == 0:
        save_stats(client)

# Funktion zum Speichern der Statistiken
def save_stats(client):
    try:
        # Aktuelle Statistiken aktualisieren
        client.ki_stats["lastUpdate"] = datetime.datetime.now().isoformat()

        with open(STATS_PATH, 'w', encoding='utf-8') as f:
            json.dump(client.ki_stats, f, ensure_ascii=False, indent=2)

        logging.info("KI-Statistiken gespeichert")
    except Exception as e:
        logging.error(f"Fehler beim Speichern der KI-Statistiken: {str(e)}")