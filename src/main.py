#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ===== 1. IMPORTS =====
# Standard library imports
import os
import json
import random
import asyncio
import datetime
import platform
from random import randint
import uuid
from collections import defaultdict
import time
import math

# Third party imports
import discord
from discord.ext import commands, tasks
from discord import Status
import requests
from bs4 import BeautifulSoup
import psutil
import servercounter
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont

# Local imports
from quiz import register_quiz_commands
# from hilfe import register_help_commands  # Jetzt in !drache integriert
from sounds import register_sound_commands, playsound, get_random_clipname, get_random_clipname_cringe, playsound_cringe
from slash_commands import register_slash_commands
from admins import register_admin_commands
from lordmeme import register_meme_commands, MemeGenerator
from lordstats import register_lordstats_commands
from updates import register_update_commands
from ki import register_ki_commands, handle_ki_message
# from butteriq import register_butteriq_commands  # Jetzt in !drache integriert
# from animated_stats import register_animated_stats_commands  # Jetzt in !drache integriert
from memory import register_memory_manager
from memory_commands import register_memory_commands
from mirror import setup_mirror
from changelog import ChangelogCog
# Premium-Funktionalität entfernt - ersetzt durch Ko-fi Spenden

# ===== 2. CONFIGURATION AND SETUP =====
# Environment variables
def get_blacklisted_guilds(guild_str):
    return guild_str.split(",") if guild_str != "" else None

token = str(os.environ['DISCORD_API_TOKEN'])
random_joins = str(os.environ['ENABLE_RANDOM_JOINS']).lower()
logging_channel = int(os.environ['LOGGING_CHANNEL'])
admin_user_id = int(os.environ['ADMIN_USER_ID'])
blacklisted_guilds = get_blacklisted_guilds(str(os.environ['BLACKLISTED_GUILDS']))

# Bot initialization - Ohne privileged intents für 100+ Server Support
intents = discord.Intents.default()
intents.message_content = False  # DEAKTIVIERT für 100+ Server Support
# intents.members = True  # Entfernt - privileged intent
# intents.presences = True  # Entfernt - privileged intent

message_history = defaultdict(dict)
user_cooldowns = {}

client = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description='Buttergolem Discord Bot Version: 5.4.0\nCreated by: ninjazan420',
    intents=intents
)
client.remove_command('help')

# Initialize StatsManager (moved from above)
from admins import StatsManager
client.stats_manager = StatsManager()

# Set start time for uptime calculation
import datetime
client.start_time = datetime.datetime.now()

# Shared variables
client.admin_user_id = admin_user_id
client.logging_channel = logging_channel
client.message_history = message_history
client.meme_generator = MemeGenerator()
client.server_id_map = {}

# Register all commands
# register_quiz_commands(client)  # Entfernt - nur !lord bleibt
# register_help_commands(client)  # Jetzt in !drache integriert
register_sound_commands(client)  # Nur für !lord befehl
register_slash_commands(client)
register_admin_commands(client)
# register_meme_commands(client)  # Entfernt - nur !lord bleibt
# register_update_commands(client)  # Entfernt - nur !lord bleibt
# register_lordstats_commands(client)  # Entfernt - nur !lord bleibt
register_ki_commands(client)
# register_butteriq_commands(client)  # Jetzt in !drache integriert
# register_animated_stats_commands(client)  # Jetzt in !drache integriert
register_memory_manager(client)
# register_memory_commands(client)  # Deaktiviert wegen Command-Konflikten
setup_mirror(client)
# Premium-Befehle entfernt - Ko-fi Spenden-Link in !hilfe verfügbar

# Changelog System laden
client.add_cog(ChangelogCog(client))

# ===== 3. HELPER FUNCTIONS =====
async def _log(message):
    channel = client.get_channel(logging_channel)
    await channel.send("```\n" + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S # ") + str(message) + "```\n")

def get_random_datetime(min, max):
    return datetime.datetime.now() + datetime.timedelta(minutes=randint(min, max))

async def get_biggest_vc(guild):
    """Gibt den ersten verfügbaren Voice Channel zurück (ohne members intent)"""
    if logging_channel:
        await _log(f"⤷ Voice Channel auswählen...\n    ⤷ 🏰 {guild.name} ({guild.id})")

    # Ohne members intent können wir nicht die Anzahl der Benutzer sehen
    # Daher nehmen wir einfach den ersten verfügbaren Voice Channel
    if guild.voice_channels:
        selected_channel = guild.voice_channels[0]
        if logging_channel:
            await _log(f"\n    ⤷ Verwende Voice Channel: {selected_channel.name}")
        return selected_channel
    else:
        # Fallback: Erstelle einen temporären Voice Channel falls keiner existiert
        if logging_channel:
            await _log("\n    ⤷ Kein Voice Channel gefunden, überspringe...")
        return None

# Rate Limiting Functions
def is_on_cooldown(user_id: int) -> bool:
    if user_id not in user_cooldowns:
        return False
    return time.time() - user_cooldowns[user_id] < 5

def update_cooldown(user_id: int):
    user_cooldowns[user_id] = time.time()

def cooldown_check():
    async def predicate(ctx):
        if is_on_cooldown(ctx.author.id):
            remaining = round(5 - (time.time() - user_cooldowns[ctx.author.id]), 1)
            await ctx.send(f"⏳ Nicht so schnell! Bitte warte noch {remaining} Sekunden.")
            return False
        update_cooldown(ctx.author.id)
        return True
    return commands.check(predicate)

# Globale Status-Nachrichten
STATUS_MESSAGES = [
        # "Meddl Loide! | /hilfe",
        # "Auf Schanzentour | /hilfe", 
        # "Buttergolem's Abenteuer | /hilfe",
        # "Haiderexperte | /hilfe",
        # "Mettbrötchen zubereiten | /hilfe",
        # "Drachenlord Simulator 2024 | /hilfe",
        # "Schanze bewachen | /hilfe",
        # "Kagghaider vertreiben | /hilfe",
        # "Buttergolem's Rückkehr | /hilfe",
        # "Altschauerberg Guide | /hilfe",
        # "Meddl-Meister | /hilfe",
        # "Drachengame Pro | /hilfe",
        # "Schanzenfestival 2024 | /hilfe",
        # "Buttergolem's Rache | /hilfe",
        # "Server-Lord | /hilfe",
        # "Discord-Drache | /hilfe",
         "Riesen update live | /hilfe",
]

@tasks.loop(minutes=10.0)
async def change_status():
    new_status = random.choice(STATUS_MESSAGES)
    await client.change_presence(activity=discord.Game(name=new_status))

@tasks.loop(minutes=5.0)
async def update_member_counter_task():
    """Background task für Member Counter Updates alle 5 Minuten"""
    await servercounter.update_counter_channels(client)

# ===== 4. BOT EVENTS =====
@client.event
async def on_ready():
    # Slash Commands automatisch synchronisieren
    try:
        synced = await client.tree.sync()
        if logging_channel:
            await _log(f"⚙️ {len(synced)} Slash Commands synchronisiert")
    except Exception as e:
        if logging_channel:
            await _log(f"❌ Fehler beim Synchronisieren der Commands: {e}")
    
    if logging_channel:
        await _log("🟢 Bot gestartet - Version 6.0.0")

    # Status-Task starten
    change_status.start()
    
    # Member Counter Task starten
    update_member_counter_task.start()
    
    # Start time für Uptime Counter setzen
    client.start_time = datetime.datetime.now()
    
    client.logging_channel = logging_channel

    if random_joins == "true":
        if logging_channel:
            await _log(f"📛 Blacklisted Server: {', '.join(blacklisted_guilds) if blacklisted_guilds else 'Keine'}")
            await _log("⏲ Timer wird initialisiert...")
        await create_random_timer(1, 1)

    await client.tree.sync()

@client.event
async def on_command_completion(ctx):
    # Administratoren nicht protokollieren
    if ctx.author.guild_permissions.administrator:
        return

    channel = client.get_channel(logging_channel)
    if not channel:
        return

    # Zeitstempel für das Embed
    timestamp = discord.utils.utcnow()

    # Server-Informationen
    if ctx.guild:
        server_name = ctx.guild.name
        server_id = ctx.guild.id
        server_icon = ctx.guild.icon.url if ctx.guild.icon else None
    else:
        server_name = "Direktnachricht"
        server_id = "DM"
        server_icon = None

    # Embed erstellen
    embed = discord.Embed(
        title="🔧 Befehl ausgeführt",
        description=f"**Befehl:** `{ctx.command}`\n**Parameter:** `{ctx.message.content}`",
        color=0x3498db,  # Blau
        timestamp=timestamp
    )

    # Benutzerinformationen hinzufügen
    embed.set_author(
        name=f"{ctx.author.display_name} ({ctx.author.id})",
        icon_url=ctx.author.display_avatar.url
    )

    # Server-Informationen hinzufügen
    embed.add_field(name="Server", value=f"{server_name} ({server_id})", inline=True)
    embed.add_field(name="Kanal", value=f"#{ctx.channel.name} ({ctx.channel.id})", inline=True)

    # Server-Icon als Thumbnail hinzufügen, falls vorhanden
    if server_icon:
        embed.set_thumbnail(url=server_icon)

    # Footer mit Zeitstempel
    embed.set_footer(text=f"Befehl • {timestamp.strftime('%d.%m.%Y %H:%M:%S')}")

    # Embed senden
    await channel.send(embed=embed)

@client.event
async def on_guild_join(guild):
    channel = client.get_channel(logging_channel)

    # Prüfe, ob der Server in der statischen Blacklist ist
    if str(guild.id) in blacklisted_guilds:
        if channel:
            await channel.send(f"⚠️ Der Bot wurde zu einem geblacklisteten Server hinzugefügt und verlässt diesen wieder: {guild.name} (ID: {guild.id})")
        await guild.leave()
        return

    # Prüfe, ob der Server in der dynamischen Ban-Liste ist
    if hasattr(client, 'ban_manager') and client.ban_manager.is_banned(guild.id):
        ban = next((b for b in client.ban_manager.get_all_bans() if b["server_id"] == str(guild.id)), None)
        ban_info = f" (Ban-ID: {ban['ban_id']}, Grund: {ban['reason']})" if ban else ""

        if channel:
            await channel.send(f"⚠️ Der Bot wurde zu einem gebannten Server hinzugefügt und verlässt diesen wieder: {guild.name} (ID: {guild.id}){ban_info}")
        await guild.leave()
        return

    # Servercounter automatisch aktualisieren
    await servercounter.single_update(client)
    
    # Server-Join Statistik erhöhen
    if hasattr(client, 'stats_manager'):
        client.stats_manager.increment_servers_joined()

    if channel:
        embed = discord.Embed(
            title="🎉 Neuer Server beigetreten!",
            description=f"Der Bot wurde zu einem neuen Server hinzugefügt.",
            color=0x2ecc71,
            timestamp=datetime.datetime.now(datetime.UTC)
        )

        embed.add_field(name="Server Name", value=guild.name, inline=True)
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Besitzer", value=str(guild.owner), inline=True)
        embed.add_field(name="Mitglieder", value=str(guild.member_count), inline=True)
        embed.add_field(name="Text Channels", value=str(len(guild.text_channels)), inline=True)
        embed.add_field(name="Voice Channels", value=str(len(guild.voice_channels)), inline=True)

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.set_footer(text=f"Jetzt auf {len(client.guilds)} Servern!")
        await channel.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    # Bestimmte Fehler ignorieren
    if isinstance(error, commands.CheckFailure) or isinstance(error, commands.CommandNotFound):
        return

    # Logging-Channel abrufen
    channel = client.get_channel(logging_channel)
    if not channel:
        return

    # Zeitstempel für das Embed
    timestamp = discord.utils.utcnow()

    # Server-Informationen
    if ctx.guild:
        server_name = ctx.guild.name
        server_id = ctx.guild.id
    else:
        server_name = "Direktnachricht"
        server_id = "DM"

    # Fehlertyp und Nachricht
    error_type = type(error).__name__
    error_message = str(error)

    # Befehlsinformationen
    command_name = ctx.command.name if ctx.command else "Unbekannt"
    command_content = ctx.message.content if ctx.message else "Unbekannt"

    # Embed erstellen
    embed = discord.Embed(
        title="⚠️ Befehlsfehler",
        description=f"**Befehl:** `{command_name}`\n**Eingabe:** `{command_content}`\n\n**Fehlertyp:** `{error_type}`\n**Fehlermeldung:** ```{error_message}```",
        color=0xe74c3c,  # Rot
        timestamp=timestamp
    )

    # Benutzerinformationen hinzufügen
    embed.set_author(
        name=f"{ctx.author.display_name} ({ctx.author.id})",
        icon_url=ctx.author.display_avatar.url
    )

    # Server- und Kanalinformationen hinzufügen
    embed.add_field(name="Server", value=f"{server_name} ({server_id})", inline=True)
    if hasattr(ctx.channel, 'name'):
        embed.add_field(name="Kanal", value=f"#{ctx.channel.name} ({ctx.channel.id})", inline=True)

    # Footer mit Zeitstempel
    embed.set_footer(text=f"Fehler • {timestamp.strftime('%d.%m.%Y %H:%M:%S')}")

    # Embed senden
    await channel.send(embed=embed)

@client.event
async def on_message(message):
    # Ignoriere Nachrichten vom Bot selbst
    if message.author.bot:
        return

    if hasattr(client, 'stats_manager'):
        client.stats_manager.add_unique_user(message.author.id)

    # Prüfe, ob es sich um eine KI-Anfrage handelt (Erwähnung oder DM)
    # Wenn ja, verarbeite sie mit der KI-Funktion aus ki.py

    # Versuche, die Nachricht als KI-Anfrage zu verarbeiten
    try:
        ki_handled = await handle_ki_message(client, message)
        # Wenn die Nachricht als KI-Anfrage verarbeitet wurde, keine weiteren Befehle verarbeiten
        if ki_handled:
            return
    except Exception as e:
        # Bei Fehlern in der KI-Verarbeitung loggen und normal fortfahren
        logging_channel = client.get_channel(client.logging_channel)
        if logging_channel:
            await logging_channel.send(f"```\nFehler bei der KI-Verarbeitung: {str(e)}```")

    # Verarbeite Befehle normal weiter
    await client.process_commands(message)

@client.event
async def on_command_completion(ctx):
    """Wird aufgerufen, wenn ein Befehl erfolgreich ausgeführt wurde"""
    if hasattr(client, 'stats_manager'):
        client.stats_manager.increment_commands()

@client.event
async def on_application_command_error(interaction, error):
    try:
        # Benutzerfreundliche Fehlermeldungen für verschiedene Fehlertypen
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(
                "❌ Ich habe nicht die nötigen Berechtigungen für diesen Befehl! "
                "Stelle sicher, dass ich die entsprechenden Rechte habe.",
                ephemeral=True
            )
        elif isinstance(error, discord.Forbidden):
            await interaction.response.send_message(
                "❌ Ich kann diesen Befehl nicht ausführen! "
                "Mir fehlen die notwendigen Berechtigungen.",
                ephemeral=True
            )
        elif isinstance(error, discord.HTTPException):
            await interaction.response.send_message(
                "❌ Bei der Ausführung des Befehls ist ein Fehler aufgetreten. "
                "Versuche es später erneut.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Ein unerwarteter Fehler ist aufgetreten. Bitte versuche es erneut oder "
                "kontaktiere den Bot-Entwickler mit `!kontakt`.",
                ephemeral=True
            )

        # Fehler im Logging-Channel protokollieren
        channel = client.get_channel(logging_channel)
        if channel:
            # Zeitstempel für das Embed
            timestamp = discord.utils.utcnow()

            # Server-Informationen
            if interaction.guild:
                server_name = interaction.guild.name
                server_id = interaction.guild.id
                server_icon = interaction.guild.icon.url if interaction.guild.icon else None
            else:
                server_name = "Direktnachricht"
                server_id = "DM"
                server_icon = None

            # Fehlertyp und Nachricht
            error_type = type(error).__name__
            error_message = str(error)

            # Befehlsinformationen
            command_name = interaction.command.name if interaction.command else "Unbekannt"

            # Embed erstellen
            embed = discord.Embed(
                title="⚠️ Slash-Befehlsfehler",
                description=f"**Befehl:** `{command_name}`\n\n**Fehlertyp:** `{error_type}`\n**Fehlermeldung:** ```{error_message}```",
                color=0xe74c3c,  # Rot
                timestamp=timestamp
            )

            # Benutzerinformationen hinzufügen
            embed.set_author(
                name=f"{interaction.user.display_name} ({interaction.user.id})",
                icon_url=interaction.user.display_avatar.url
            )

            # Server- und Kanalinformationen hinzufügen
            embed.add_field(name="Server", value=f"{server_name} ({server_id})", inline=True)
            if hasattr(interaction.channel, 'name'):
                embed.add_field(name="Kanal", value=f"#{interaction.channel.name} ({interaction.channel.id})", inline=True)

            # Server-Icon als Thumbnail hinzufügen, falls vorhanden
            if server_icon:
                embed.set_thumbnail(url=server_icon)

            # Footer mit Zeitstempel
            embed.set_footer(text=f"Slash-Fehler • {timestamp.strftime('%d.%m.%Y %H:%M:%S')}")

            # Embed senden
            await channel.send(embed=embed)

    except Exception as e:
        # Falls die Interaktion bereits beantwortet wurde oder ein anderer Fehler auftritt
        channel = client.get_channel(logging_channel)
        if channel:
            # Einfacheres Fehler-Embed für Fehler bei der Fehlerbehandlung
            embed = discord.Embed(
                title="⚠️ Fehler bei der Fehlerbehandlung",
                description=f"**Ursprünglicher Fehler:** `{str(error)}`\n**Zusätzlicher Fehler:** `{str(e)}`",
                color=0xe74c3c,  # Rot
                timestamp=discord.utils.utcnow()
            )

            # Benutzerinformationen hinzufügen, falls verfügbar
            if hasattr(interaction, 'user') and interaction.user:
                embed.add_field(name="Benutzer", value=f"{interaction.user.display_name} ({interaction.user.id})", inline=True)

            # Befehlsinformationen hinzufügen, falls verfügbar
            if hasattr(interaction, 'command') and interaction.command:
                embed.add_field(name="Befehl", value=interaction.command.name, inline=True)

            await channel.send(embed=embed)

# ===== 5. PREFIX COMMAND REDIRECTS =====
# Alle Prefix-Commands wurden zu Slash-Commands migriert
# Diese Redirects wurden entfernt, da sie Konflikte mit den registrierten Commands verursachten
# Die ursprünglichen Commands in den jeweiligen Modulen zeigen bereits Deprecation-Warnungen an

@client.command(pass_context=True)
async def id(ctx):
    await ctx.message.channel.send(f'Aktuelle Server ID: {ctx.message.guild.id}')
    await ctx.message.channel.send(f'Aktuelle Textchannel ID: {ctx.message.channel.id}')
    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await ctx.message.channel.send(f'Aktuelle Voicekanal ID: {voice_channel.id}')

# ===== 6. TIMER FUNCTIONS =====
async def create_random_timer(min, max):
    minutes = randint(min, max)
    if logging_channel:
        endtime = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
        await _log(f"⤷ Timer gesetzt! Nächster Drachenlordbesuch: {endtime.strftime('%d-%m-%Y %H:%M:%S')}")

    await asyncio.sleep(minutes * 60)
    await on_reminder()

async def on_reminder():
    if logging_channel:
        await _log("🟠 TIMER! Sound wird abgespielt...")

    for guild in client.guilds:
        # Prüfe, ob der Server in der statischen Blacklist ist
        if str(guild.id) in blacklisted_guilds:
            await _log(f"📛 {guild.name} ({guild.id}) wurde in BLACKLISTED_GUILDS geblacklistet. Überspringe...")
            continue

        # Prüfe, ob der Server in der dynamischen Ban-Liste ist
        if hasattr(client, 'ban_manager') and client.ban_manager.is_banned(guild.id):
            await _log(f"🚫 {guild.name} ({guild.id}) wurde über !drache leave gebannt. Überspringe...")
            continue

        # Hole Voice Channel und prüfe ob verfügbar
        voice_channel = await get_biggest_vc(guild)
        if voice_channel:
            await playsound(voice_channel, get_random_clipname(), client)
            await playsound_cringe(voice_channel, get_random_clipname_cringe(), client)
        else:
            if logging_channel:
                await _log(f"⚠️ Kein Voice Channel in {guild.name} verfügbar, überspringe Sound-Wiedergabe")

    if logging_channel:
        await _log("⤷ ⏲ Neuer Timer wird gesetzt...")
    await create_random_timer(30, 120)

# ===== 7. BOT START =====
# Add sound functions to bot instance
client.playsound = playsound
client.get_random_clipname = get_random_clipname
client.playsound_cringe = playsound_cringe
client.get_random_clipname_cringe = get_random_clipname_cringe

# Set bot owner_id to admin_user_id for proper admin recognition
client.owner_id = admin_user_id

# Start the bot
async def main():
    async with client:
        await client.start(token)

if __name__ == "__main__":
    asyncio.run(main())

