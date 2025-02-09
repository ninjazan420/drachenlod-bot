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
import math  # Neu für Seitenberechnung

# Third party imports
import discord
from discord.ext import commands
from discord import Status
import requests
from bs4 import BeautifulSoup
import psutil  # Neuer Import für Systeminfos
import servercounter
from discord import app_commands  # Neuer Import für Slash-Befehle
from PIL import Image, ImageDraw, ImageFont  # Neu für Meme-Generator

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

# Initialize message history before bot creation
message_history = defaultdict(dict)

client = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description='Buttergolem Discord Bot Version: 4.2.0\nCreated by: ninjazan420',
    intents=intents
)
client.remove_command('help')

# Make shared variables available to bot
client.admin_user_id = admin_user_id
client.logging_channel = logging_channel
client.message_history = message_history

# Quiz-Modul importieren und Befehle registrieren
from quiz import register_quiz_commands
from hilfe import register_help_commands
from sounds import register_sound_commands
from admins import register_admin_commands

# Register commands after setting up shared variables
register_quiz_commands(client)
register_help_commands(client)
register_sound_commands(client)
register_admin_commands(client)

# Importiere Sound-Funktionen
from sounds import playsound, get_random_clipname, get_random_clipname_cringe, playsound_cringe

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
            await ctx.send(f"⏳ Nicht so schnell! Bitte warte noch {remaining} Sekunden.")
            return False
        update_cooldown(ctx.author.id)
        return True
    return commands.check(predicate)

# Add error handler for cooldown check failures
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        # Error already handled in cooldown_check
        pass
    else:
        # Log other errors
        if logging_channel:
            await _log(f"Error in {ctx.command}: {str(error)}")

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
    # Keine Logging-Nachricht senden, wenn der Benutzer ein Admin ist
    if ctx.author.id == admin_user_id:
        return
    
    channel = client.get_channel(logging_channel)
    server = ctx.guild.name if ctx.guild else "DM"
    await channel.send(f"```\n{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} # {ctx.author} used {ctx.command} in {server}```")

# --- Basic Commands ---
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
    try:
        if ctx.message.author == client.user:
            return

        with open('/app/data/quotes.json', mode="r", encoding="utf-8") as quotes_file:
            buttergolem_quotes = json.load(quotes_file)
        with open('/app/data/names.json', mode="r", encoding="utf-8") as names_file:
            buttergolem_names = json.load(names_file)

        name = random.choice(buttergolem_names)
        quote = random.choice(buttergolem_quotes)
        await ctx.message.channel.send(f"{name} sagt: {quote}")
    except Exception as e:
        if logging_channel:
            await _log(f"Error in zitat command: {str(e)}")
        await ctx.send("Ein Fehler ist aufgetreten beim Ausführen des Befehls.")

# --- Utility Commands ---
@client.command(pass_context=True)
async def id(ctx):
    await ctx.message.channel.send(f'Aktuelle Server ID: {ctx.message.guild.id}')
    await ctx.message.channel.send(f'Aktuelle Textchannel ID: {ctx.message.channel.id}')
    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await ctx.message.channel.send(f'Aktuelle Voicekanal ID: {voice_channel.id}')

# MemeGenerator Klasse hinzufügen
class MemeGenerator:
    def __init__(self):
        self.image_folder = "/app/data/imgs/drache"  
        self.font_path = "/app/data/fonts/impact.ttf" 
        self.output_folder = "/tmp"

        # Überprüfen der Pfade
        for path in [self.image_folder, self.font_path]:
            if not os.path.exists(path):
                raise RuntimeError(f"Datei/Ordner nicht gefunden: {path}")

    def wrap_text(self, text, font, max_width):
        """Bricht Text um, wenn er zu lang ist"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

    def calculate_font_size(self, text, max_width, max_height, initial_size, font_path):
        """Berechnet die optimale Schriftgröße für den gegebenen Text"""
        font_size = initial_size
        min_font_size = 20  # Minimale Schriftgröße
        
        while font_size > min_font_size:
            font = ImageFont.truetype(font_path, font_size)
            lines = self.wrap_text(text, font, max_width)
            
            # Berechne Gesamthöhe des Texts
            bbox = font.getbbox("Ag")
            line_height = bbox[3] - bbox[1] + 10
            total_height = line_height * len(lines)
            
            # Wenn der Text in den verfügbaren Platz passt, diese Größe verwenden
            if total_height <= max_height:
                break
                
            # Reduziere Schriftgröße
            font_size -= 2
            
        return font_size

    def generate_meme(self, text):
        """Erstellt ein Meme mit dem gegebenen Text"""
        # Wähle ein zufälliges Bild aus
        image_path = os.path.join(self.image_folder, random.choice(os.listdir(self.image_folder)))
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        # Initiale Schriftgröße (8% der Bildbreite)
        initial_font_size = int(image.width * 0.08)
        
        # Maximale Breite und Höhe für Text
        max_width = int(image.width * 0.9)
        max_height_top = int(image.height * 0.25)    # 25% der Bildhöhe für oberen Text
        max_height_bottom = int(image.height * 0.25)  # 25% der Bildhöhe für unteren Text

        # Text aufteilen und in Großbuchstaben umwandeln
        if "|" in text:
            top_text, bottom_text = text.split("|", 1)
            top_text = top_text.strip().upper()
            bottom_text = bottom_text.strip().upper()
        else:
            top_text = ""
            bottom_text = text.strip().upper()

        # Berechne optimale Schriftgrößen
        top_font_size = self.calculate_font_size(top_text, max_width, max_height_top, 
                                               initial_font_size, self.font_path) if top_text else initial_font_size
        bottom_font_size = self.calculate_font_size(bottom_text, max_width, max_height_bottom, 
                                                  initial_font_size, self.font_path)

        # Margins
        top_margin = int(image.height * 0.06)
        bottom_margin = int(image.height * 0.12)

        # Zeichne oberen Text
        if top_text:
            font = ImageFont.truetype(self.font_path, top_font_size)
            lines = self.wrap_text(top_text, font, max_width)
            bbox = font.getbbox("Ag")
            line_height = bbox[3] - bbox[1] + 10
            y = top_margin

            for line in lines:
                bbox = font.getbbox(line)
                text_width = bbox[2] - bbox[0]
                x = (image.width - text_width) / 2
                
                # Outline-Effekt
                for adj in range(-3, 4):
                    for adj2 in range(-3, 4):
                        draw.text((x+adj, y+adj2), line, font=font, fill="black")
                draw.text((x, y), line, font=font, fill="white")
                y += line_height

        # Zeichne unteren Text
        if bottom_text:
            font = ImageFont.truetype(self.font_path, bottom_font_size)
            lines = self.wrap_text(bottom_text, font, max_width)
            bbox = font.getbbox("Ag")
            line_height = bbox[3] - bbox[1] + 10
            total_height = line_height * len(lines)
            y = image.height - bottom_margin - total_height

            for line in lines:
                bbox = font.getbbox(line)
                text_width = bbox[2] - bbox[0]
                x = (image.width - text_width) / 2
                
                # Outline-Effekt
                for adj in range(-3, 4):
                    for adj2 in range(-3, 4):
                        draw.text((x+adj, y+adj2), line, font=font, fill="black")
                draw.text((x, y), line, font=font, fill="white")
                y += line_height

        # Bild speichern
        output_path = os.path.join(self.output_folder, f"meme_{uuid.uuid4().hex}.png")
        image.save(output_path)
        return output_path

# --- Meme Command ---
@client.command(name='lordmeme')
@cooldown_check()
async def create_meme(ctx, *, text: str):
    """Erstellt ein Drachenlord Meme"""
    try:
        # Generiere das Meme
        output_path = client.meme_generator.generate_meme(text)
        
        # Sende das Meme
        await ctx.send(file=discord.File(output_path))
        
        # Lösche die temporäre Datei
        os.remove(output_path)
    except Exception as e:
        if logging_channel:
            await _log(f"Error in meme command: {str(e)}")
        await ctx.send("Ein Fehler ist aufgetreten beim Erstellen des Memes.")

# Füge die Sound-Funktionen zum Bot hinzu damit sie von anderen Modulen verwendet werden können
client.playsound = playsound
client.get_random_clipname = get_random_clipname
client.playsound_cringe = playsound_cringe
client.get_random_clipname_cringe = get_random_clipname_cringe

# Bot starten
client.meme_generator = MemeGenerator()
client.run(token)

