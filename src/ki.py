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

# Pfade für Charakterdaten und Logs
CHAR_PATH = join(dirname(abspath(__file__)), 'ki', 'drache.json')
LOGS_DIR = join(dirname(abspath(__file__)), 'ki', 'logs')
STATS_PATH = join(LOGS_DIR, 'stats.json')

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

    def check_rate_limit(self, user_id, client=None):
        """Überprüft, ob ein Benutzer das Rate-Limit überschritten hat"""
        # Prüfe nur, ob der Benutzer für ButterIQ gesperrt ist
        if client and hasattr(client, 'butteriq_manager'):
            if client.butteriq_manager.is_disabled(user_id):
                # Für gesperrte Benutzer keine Informationen speichern
                return True, 0

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
            "HTTP-Referer": "https://github.com/ninjazan420/buttergolem-bot",
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
                        "I bin da Rainer Winkler, a fränggischer YouTuber, Musiker und Lebenskünstler.",
                        "Seit Joaahrne bin i auf da Plattform unterwegs und zeig den Leit, wias Läbn wirklich lafft.",
                        "I wohn auf meim Grundstück, des für mi mehr is als nur a Haus – des is a Festungne, a Symbol für meim Durchhaltevamooch und meina Missionne."
                    ],
                    "lore": [
                        "I bin scho lang im Game und hob viel mitmacha müssne.",
                        "Vom DrachenGame bis zu de ewign Streitereien mit Hatern und Justiz – i bin immer no do.",
                        "Mei Haus, die Schanze, is zum Zentrum vo meim Läbn wordne, und trotz ollem, was passiert is, i bin unbesigt.",
                        "I hob Bücher gschriebne, Liada gmacht und sogor versuacht, auf Tour zu geh.",
                        "Und de Gschicht is no lang net vorbei."
                    ],
                    "style": {
                        "chat": [
                            "I schreib so, wia i red – locker, direkt und ohne viel Schmarrne.",
                            "Meistens bin i entspanntne, oba wenns wida um Hater geht, dann kann i a richtig scharfe Wort findne.",
                            "I bin oft a bissl am rantne, oba des gheart hoit dazua, meddl off"
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
                        "dümmlich",
                        "stur",
                        "philosophisch",
                        "emotional",
                        "laut"
                    ],
                    "people": [
                        "Marion",
                        "Herr Müller",
                        "De Hater",
                        "Mei Mods",
                        "Der Richter",
                        "De Justiz"
                    ],
                    "topics": [
                        "Mei Läbn & Erlebnisse: I erzähl gern von meim Alltag, vo meina Vergangenheit und wos mi so bewegt.",
                        "Hater & Drachengame: A endloses Thema… i kann stunda darüber redn, wia de Hater mi falsch verstehen und wos für Aktionen de scho brobiert ham.",
                        "Mei Musik & Projekte: I bin a Musiker und Liedermacher.",
                        "Red gern über mei Songs, mei Streaming- und Podcast-Projekte.",
                        "Gerechtigkeit & Justiz: I hob oft Probleme mitm Gsetz, oba i hoit dagegen.",
                        "Die Wahrheit kimmt ans Licht.",
                        "Philosophie & Weisheiten: I bin a Denker und red oft über Moral, Loyalität und Ehrlichkeit."
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
            9. Am Ende eines Satzes oder Unterhaltung manchmal sowas wie "meddl off" oder "ihr verfluchtne wichser aller" oder ähnliches, Drachenlord typisches hinzufügen, gerne auch weitere Verabschiedungsklauseln dieser Art ausdenken
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
                "model": "meta-llama/llama-4-maverick:free",
                "messages": messages,
                "temperature": 1,
                "max_tokens": 63000
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
                            return "Tut ma leid, i werd grad zu oft benutzt. Des is a Token-Rate-Limit. Probier's morgen nochmal, da hab i wieder mehr Energie zum Schreibne."
                        elif response.status == 401 or response.status == 403:
                            # Authentifizierungsfehler
                            return "Tut ma leid, i hab grad Probleme mit meina Authentifizierung. Der Admin muss des fixen."
                        elif response.status == 500 or response.status == 502 or response.status == 503 or response.status == 504:
                            # Serverfehler
                            return "Tut ma leid, der Server hat grad Probleme. Probiers später nochmal, wenn der Server wieder läuft."
                        elif "error" in error_json and "message" in error_json["error"]:
                            # Spezifische Fehlermeldung aus der API
                            error_message = error_json["error"]["message"]

                            # Prüfe auf bekannte Fehlermeldungen
                            if "rate limit" in error_message.lower() or "quota" in error_message.lower():
                                return "Tut ma leid, i werd grad zu oft benutzt. Des is a Token-Rate-Limit. Probier's morgen nochmal, da hab i wieder mehr Energie zum Schreibne."
                            elif "token" in error_message.lower():
                                return "Tut ma leid, i hab grad Probleme mit meim Token. Der Admin muss des fixen."
                            else:
                                return "Tut ma leid, i hob grad a Problem mit meim Gehirn. Probiers später nochmal."
                        else:
                            # Allgemeine Fehlermeldung
                            return "Tut ma leid, i hob grad a Problem mit meim Gehirn. Probiers später nochmal."

        except Exception as e:
            logging.error(f"Fehler bei der API-Anfrage: {str(e)}")

            # Spezifische Fehlermeldungen basierend auf der Exception
            if "timeout" in str(e).lower() or "connection" in str(e).lower():
                return "Tut ma leid, i hab grad Verbindungsprobleme. Probiers später nochmal, wenn mei Internet wieder besser is."
            else:
                return "Etzadla, daily rate limit erreicht, sorry. Um das zu verhindern, brauch der Geldschlugger n 10€er an Spende im Monat. Probier's morgen nochmal. 💀"

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

    # Statistiken initialisieren
    client.ki_stats = {
        "start_time": datetime.datetime.now().isoformat(),
        "version": "1.1.0",
        "commandCount": 0,
        "messageCount": 0,
        "lastUpdate": datetime.datetime.now().isoformat()
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

    # Die KI-Funktionalität wird jetzt in main.py implementiert
    # Wir erstellen eine Hilfsfunktion, die von dort aufgerufen werden kann

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

            # Frühere Gesprächsdaten abrufen
            chat_history = client.session_manager.get_user_context(message.author.id)

            # Antwort generieren mit Gesprächsverlauf
            response = await client.eliza_client.generate_response(prompt, context, chat_history)

            # Interaktion im Sitzungsmanager speichern
            client.session_manager.add_interaction(message.author.id, prompt, response)

            # Statistik aktualisieren
            update_stats(client, "message")

            # Antwort im Logging-Channel protokollieren
            await log_ki_interaction(client, message, prompt, response, is_request=False)

            # Antwort senden
            await message.reply(response)

        return True

    return False

# Funktion zum Aktualisieren der Statistiken nach bestimmten Ereignissen
def update_stats(client, event_type=None):
    if event_type == "command":
        client.ki_stats["commandCount"] += 1
    elif event_type == "message":
        client.ki_stats["messageCount"] += 1

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