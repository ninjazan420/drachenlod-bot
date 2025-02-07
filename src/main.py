#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard library imports
import os
import json
import random
import asyncio
import datetime
import platform
from random import randint
import uuid  # Neu für eindeutige IDs
from collections import defaultdict  # Neu für Nachrichten-Tracking
import time  # Neu für Rate-Limiting

# Third party imports
import discord
from discord.ext import commands
from discord import Status
import requests
from bs4 import BeautifulSoup
import psutil  # Neuer Import für Systeminfos
import servercounter
from discord import app_commands  # Neuer Import für Slash-Befehle

# --- Configuration and Setup ---
def get_blacklisted_guilds(guild_str):
    return guild_str.split(",") if guild_str != "" else None

# Environment variables
token = str(os.environ['DISCORD_API_TOKEN'])
random_joins = str(os.environ['ENABLE_RANDOM_JOINS']).lower()
logging_channel = int(os.environ['LOGGING_CHANNEL'])
admin_user_id = int(os.environ['ADMIN_USER_ID'])
blacklisted_guilds = get_blacklisted_guilds(str(os.environ['BLACKLISTED_GUILDS']))

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

client = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description='Buttergolem Discord Bot Version: 3.7.0\nCreated by: ninjazan420',
    intents=intents
)
client.remove_command('help')

# Quiz-Modul importieren und Befehle registrieren
from quiz import register_quiz_commands
register_quiz_commands(client)

message_history = defaultdict(dict)  # Speichert Nachrichten-IDs und zugehörige User

# Rate Limiting System
user_cooldowns = {}

def is_on_cooldown(user_id: int) -> bool:
    """Überprüft, ob ein Benutzer sich noch in der Cooldown-Phase befindet"""
    if user_id not in user_cooldowns:
        return False
    return time.time() - user_cooldowns[user_id] < 5

def update_cooldown(user_id: int):
    """Aktualisiert den Cooldown für einen Benutzer"""
    user_cooldowns[user_id] = time.time()

# Erstelle einen Check für Cooldowns
def cooldown_check():
    async def predicate(ctx):
        if is_on_cooldown(ctx.author.id):
            remaining = round(5 - (time.time() - user_cooldowns[ctx.author.id]), 1)
            await ctx.send(f"⏳ Nicht so schnell! Bitte warte noch {remaining} Sekunden.", delete_after=5)
            return False
        update_cooldown(ctx.author.id)
        return True
    return commands.check(predicate)

# --- Helper Functions ---
async def _log(message):
    channel = client.get_channel(logging_channel)
    await channel.send("```\n" + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S # ") + str(message) + "```\n")

def get_random_datetime(min, max):
    return datetime.datetime.now() + datetime.timedelta(minutes=randint(min, max))

async def get_biggest_vc(guild):
    if logging_channel:
        await _log(f"⤷ Grössten VC herausfinden...\n    ⤷ 🏰 {guild.name} ({guild.id})")

    voice_channel_with_most_users = guild.voice_channels[0]
    logtext = ""
    
    for voice_channel in guild.voice_channels:
        logtext += f"\n    ⤷ {len(voice_channel.members)} Benutzer in {voice_channel.name}"
        if len(voice_channel.members) > len(voice_channel_with_most_users.members):
            voice_channel_with_most_users = voice_channel

    if logging_channel:
        await _log(logtext)
    return voice_channel_with_most_users

# --- Sound Related Functions ---
def get_random_clipname():
    return str(random.choice(os.listdir('/app/data/clips')))

def get_random_clipname_cringe():
    return str(random.choice(os.listdir('/app/data/clips/cringe/')))

async def playsound(voice_channel, soundfile):
    vc = await voice_channel.connect()
    vc.play(discord.FFmpegPCMAudio(f'/app/data/clips/{soundfile}'), 
            after=lambda e: print('erledigt', e))
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()

async def playsound_cringe(voice_channel, soundfile):
    vc = await voice_channel.connect()
    vc.play(discord.FFmpegPCMAudio(f'/app/data/clips/cringe/{soundfile}'), 
            after=lambda e: print('erledigt', e))
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()

async def voice_quote(ctx, soundname):
    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await playsound(voice_channel, soundname)
    else:
        await ctx.message.channel.send('Das funktioniert nur in serverchannels du scheiß HAIDER')

# --- Timer Related Functions ---
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
        if str(guild.id) in blacklisted_guilds:
            await _log(f"📛 {guild.name} ({guild.id}) wurde geblacklistet. Überspringe...")
            continue
        await playsound(await get_biggest_vc(guild), get_random_clipname())
        await playsound_cringe(await get_biggest_vc(guild), get_random_clipname_cringe())

    if logging_channel:
        await _log("⤷ ⏲ Neuer Timer wird gesetzt...")
    await create_random_timer(30, 120)

# --- Bot Events ---
@client.event
async def on_ready():
    if logging_channel:
        await _log("🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢")
        await _log("⏳           Server beigetreten           ⏳")
        await _log("🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢")
        
    await client.change_presence(activity=discord.Game(name="/hilfe du kaschber"))
    
    # Set logging channel for servercounter
    client.logging_channel = logging_channel
    
    # Start server counter
    client.loop.create_task(servercounter.update_server_count(client))
    
    if random_joins == "true":
        await _log(f"📛 blacklisted Server: {''.join(str(e) + ',' for e in blacklisted_guilds)}")
        if logging_channel:
            await _log("⏲ Erster Timer wird gesetzt...")
        await create_random_timer(1, 1)
    
    await client.tree.sync()  # Synchronisiere Slash-Befehle

@client.event
async def on_command_completion(ctx):
    channel = client.get_channel(logging_channel)
    server = ctx.guild.name if ctx.guild else "DM"
    await channel.send(f"```\n{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} # {ctx.author} used {ctx.command} in {server}```")

# --- Basic Commands ---
async def create_help_embed(is_admin: bool) -> discord.Embed:
    """Erstellt das Help-Embed basierend auf den Berechtigungen"""
    embed = discord.Embed(
        title="🤖 Buttergolem Bot Hilfe",
        description="Dieser Bot scheißt dir zufällige Zitate vom Arschgebirge aus der Schimmelschanze direkt in deinen Discord-Server.\n\nVersion: 3.7.0 | Created by: ninjazan420",
        color=0xf1c40f
    )

    # Basis-Befehle
    embed.add_field(
        name="📋 Basis-Befehle",
        value="• `!hilfe` - Zeigt diese Hilfe an\n"
              "• `!mett` - Zeigt den aktuellen Mett-Level 🥓\n"
              "• `!zitat` - Zufälliges Zitat",
        inline=False
    )

    # Sound-Befehle
    embed.add_field(
        name="🔊 Sound-Befehle",
        value="• `!lord` - Zufälliges GESCHREI im Voice\n"
              "• `!cringe` - Oh no, cringe!\n"
              "• Weitere Sounds: `!warum`, `!frosch`, `!idiot`, `!meddl`, "
              "`!scheiße`, `!huso`, `!maul2` und mehr...",
        inline=False
    )

    # Quiz-Befehle
    embed.add_field(
        name="❓ Quiz-Befehle",
        value="• `!lordquiz` - Quiz-Informationen\n"
              "• `!lordquiz start <Anzahl Runden (1-20)>` - Startet Quiz\n"
              "• `!lordquiz stop` - Beende Quiz",
        inline=False
    )

    # Kontakt-Befehle
    embed.add_field(
        name="📧 Kontakt",
        value="• `!kontakt <Nachricht>` - Sende eine Nachricht an den Admin\n",
        inline=False
    )

    # Admin-Befehle nur anzeigen wenn Admin
    if is_admin:
        embed.add_field(
            name="⚙️ Admin-Befehle",
            value="• `!server` - Server-Liste\n"
                  "• `!user` - Nutzerstatistiken\n"
                  "• `!ping` - Bot-Latenz\n"
                  "• `!antwort <ID> <Text>` - Auf Kontaktnachrichten antworten",
            inline=False
        )

    embed.set_footer(text="Der Bot muss die Berechtigung besitzen, in den Voice zu joinen!")
    return embed

@client.command(name='hilfe')
async def hilfe_command(ctx):
    """Zeigt die Hilfe für den Buttergolem Bot"""
    is_admin = ctx.author.guild_permissions.administrator
    embed = await create_help_embed(is_admin)
    await ctx.send(embed=embed)

@client.tree.command(name="hilfe", description="Zeigt die Hilfe für den Buttergolem Bot")
async def hilfe_slash(interaction: discord.Interaction):
    """Zeigt die Hilfe für den Buttergolem Bot"""
    is_admin = interaction.user.guild_permissions.administrator
    embed = await create_help_embed(is_admin)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@client.command(name='mett')
@cooldown_check()
async def mett_level(ctx):
    """Zeigt den aktuellen Mett-Level an"""
    level = random.randint(1, 10)
    mett_meter = "🥓" * level + "⬜" * (10 - level)
    await ctx.send(f"Aktueller Mett-Level: {level}/10\n{mett_meter}")

# --- Quote Commands ---
@client.command(pass_context=True)
@cooldown_check()
async def zitat(ctx):
    if ctx.message.author == client.user:
        return

    with open('/app/data/quotes.json', mode="r", encoding="utf-8") as quotes_file:
        buttergolem_quotes = json.load(quotes_file)
    with open('/app/data/names.json', mode="r", encoding="utf-8") as names_file:
        buttergolem_names = json.load(names_file)

    name = random.choice(buttergolem_names)
    quote = random.choice(buttergolem_quotes)
    await ctx.message.channel.send(f"{name} sagt: {quote}")

# --- Utility Commands ---
@client.command(pass_context=True)
async def id(ctx):
    await ctx.message.channel.send(f'Aktuelle Server ID: {ctx.message.guild.id}')
    await ctx.message.channel.send(f'Aktuelle Textchannel ID: {ctx.message.channel.id}')
    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await ctx.message.channel.send(f'Aktuelle Voicekanal ID: {voice_channel.id}')

# --- Sound Commands ---
@client.command(pass_context=True)
@cooldown_check()
async def lord(ctx):
    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await playsound(voice_channel, get_random_clipname())
    else:
        await ctx.message.channel.send('Das funktioniert nur in serverchannels du scheiß HAIDER')

@client.command(pass_context=True)
@cooldown_check()
async def cringe(ctx):
    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await playsound_cringe(voice_channel, get_random_clipname_cringe())
    else:
        await ctx.message.channel.send('Das funktioniert nur in serverchannels du scheiß HAIDER')

# --- Individual Sound Commands ---
# Dictionary für Sound-Kommandos
SOUND_COMMANDS = {
    'warum': 'warum.mp3', 'frosch': 'frosch.mp3', 'furz': 'furz.mp3',
    'idiot': 'idiot.mp3', 'meddl': 'meddl.mp3', 'scheiße': 'scheiße.mp3',
    'durcheinander': 'Durcheinander.mp3', 'wiebitte': 'Wiebitte.mp3',
    'dick': 'Dick.mp3', 'vorbei': 'Vorbei.mp3', 'hahn': 'Hahn.mp3',
    'bla': 'Blablabla.mp3', 'maske': 'Maske.mp3', 'lockdown': 'Regeln.mp3',
    'regeln': 'Regeln2.mp3', 'csu': 'Seehofer.mp3', 'lol': 'LOL.mp3',
    'huso': 'Huso.mp3', 'bastard': 'Bastard.mp3', 'lappen': 'Lappen.mp3',
    'maul2': 'Maul2.mp3', 'wiwi': 'Wiwi.mp3', 'rumwichsen': 'Rumzuwichsen.mp3'
}

# Automatisch Kommandos für alle Sounds erstellen
for cmd_name, sound_file in SOUND_COMMANDS.items():
    @client.command(name=cmd_name)
    @cooldown_check()
    async def sound_cmd(ctx, sound_file=sound_file):
        await voice_quote(ctx, sound_file)

# --- Admin Commands ---
@client.command(pass_context=True)
async def server(ctx):
    if ctx.author.id != admin_user_id:
        await ctx.send("Du bist nicht berechtigt, diesen Befehl zu nutzen!")
        return
    
    server_list = "\n".join([f"• {guild.name} (ID: {guild.id})" for guild in client.guilds])
    await ctx.send(f"```Der Bot ist auf folgenden Servern aktiv:\n{server_list}```")
    if logging_channel:
        await _log(f"Admin-Befehl !server wurde von {ctx.author.name} ausgeführt")

@client.command(pass_context=True)
async def user(ctx):
    if ctx.author.id != admin_user_id:
        await ctx.send("Du bist nicht berechtigt, diesen Befehl zu nutzen!")
        return
    
    total_users = 0
    online_users = 0
    server_stats = []
    
    for guild in client.guilds:
        guild_total = guild.member_count
        guild_online = len([m for m in guild.members if m.status != Status.offline and not m.bot])
        total_users += guild_total
        online_users += guild_online
        server_stats.append(f"• {guild.name}: {guild_total} Nutzer ({guild_online} online)")
    
    stats_message = [
        "```Nutzerstatistiken:\n",
        f"Gesamt über alle Server: {total_users} Nutzer",
        f"Davon online: {online_users} Nutzer\n",
        "Details pro Server:",
        *server_stats,
        "```"
    ]
    
    await ctx.send("\n".join(stats_message))
    if logging_channel:
        await _log(f"Admin-Befehl !user wurde von {ctx.author.name} ausgeführt")


@client.command()
@commands.has_permissions(administrator=True)
async def ping(ctx):
    latency = round(client.latency * 1000)
    await ctx.send(f"🏓 Pong! Bot Latenz: {latency}ms")

@client.command()
@commands.has_permissions(administrator=True)
async def servercount(ctx):
    """Führt ein manuelles Servercounter-Update durch"""
    await ctx.send("🔄 Starte manuelles Servercounter Update...")
    success = await servercounter.single_update(client)
    if not success:
        await ctx.send("❌ Servercounter Update fehlgeschlagen! Überprüfe die Logs.")

@client.command(name='kontakt')
async def contact(ctx, *, message=None):
    """Sendet eine Nachricht an den Bot-Administrator"""
    if not message:
        await ctx.send("Bitte gib eine Nachricht an! Beispiel: `!kontakt Hallo, ich habe eine Frage`")
        return

    admin_user = await client.fetch_user(admin_user_id)
    if not admin_user:
        await ctx.send("❌ Fehler: Admin konnte nicht gefunden werden!")
        return

    message_id = str(uuid.uuid4())[:8]  # Erstelle kurze eindeutige ID
    message_history[message_id] = ctx.author.id

    embed = discord.Embed(
        title="📨 Neue Nachricht",
        description=message,
        color=0x3498db,
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="Absender", value=f"{ctx.author} (ID: {ctx.author.id})")
    embed.add_field(name="Server", value=ctx.guild.name if ctx.guild else "DM")
    embed.add_field(name="Nachrichten-ID", value=message_id, inline=False)
    embed.set_footer(text=f"Antworte mit: !antwort {message_id} <deine Antwort>")

    try:
        await admin_user.send(embed=embed)
        await ctx.send("✅ Deine Nachricht wurde erfolgreich an den Administrator gesendet!")
        if logging_channel:
            await _log(f"Kontaktnachricht von {ctx.author} (ID: {message_id})")
    except:
        await ctx.send("❌ Fehler beim Senden der Nachricht!")

@client.command(name='antwort')
async def reply(ctx, message_id=None, *, response=None):
    """Ermöglicht dem Admin, auf Kontaktnachrichten zu antworten"""
    if ctx.author.id != admin_user_id:
        await ctx.send("❌ Nur der Administrator kann diesen Befehl nutzen!")
        return

    if not message_id or not response:
        await ctx.send("❌ Syntax: `!antwort <message_id> <deine Antwort>`")
        return

    if message_id not in message_history:
        await ctx.send("❌ Diese Nachrichten-ID existiert nicht!")
        return

    user_id = message_history[message_id]
    try:
        user = await client.fetch_user(user_id)
        embed = discord.Embed(
            title="📩 Antwort vom Administrator",
            description=response,
            color=0x2ecc71,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Bezugnehmend auf ID", value=message_id)
        
        await user.send(embed=embed)
        await ctx.send("✅ Antwort wurde erfolgreich gesendet!")
        if logging_channel:
            await _log(f"Admin-Antwort an User {user.id} (ID: {message_id})")
    except:
        await ctx.send("❌ Fehler beim Senden der Antwort!")

# Bot starten
client.run(token)
