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
from discord.ext import commands
from discord import Status
import requests
from bs4 import BeautifulSoup
import psutil
import servercounter
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont

# Local imports
from quiz import register_quiz_commands
from hilfe import register_help_commands
from sounds import register_sound_commands, playsound, get_random_clipname, get_random_clipname_cringe, playsound_cringe
from admins import register_admin_commands
from lordmeme import register_meme_commands, MemeGenerator
from lordstats import register_lordstats_commands
from updates import register_update_commands

# ===== 2. CONFIGURATION AND SETUP =====
# Environment variables
def get_blacklisted_guilds(guild_str):
    return guild_str.split(",") if guild_str != "" else None

token = str(os.environ['DISCORD_API_TOKEN'])
random_joins = str(os.environ['ENABLE_RANDOM_JOINS']).lower()
logging_channel = int(os.environ['LOGGING_CHANNEL'])
admin_user_id = int(os.environ['ADMIN_USER_ID'])
blacklisted_guilds = get_blacklisted_guilds(str(os.environ['BLACKLISTED_GUILDS']))

# Bot initialization
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

message_history = defaultdict(dict)
user_cooldowns = {}

client = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description='Buttergolem Discord Bot Version: 4.4.2\nCreated by: ninjazan420',
    intents=intents
)
client.remove_command('help')

# Initialize StatsManager (moved from above)
from admins import StatsManager
client.stats_manager = StatsManager()

# Shared variables
client.admin_user_id = admin_user_id
client.logging_channel = logging_channel
client.message_history = message_history
client.meme_generator = MemeGenerator()

# Register all commands
register_quiz_commands(client)
register_help_commands(client)
register_sound_commands(client)
register_admin_commands(client)
register_meme_commands(client)
register_update_commands(client)
register_lordstats_commands(client)

# ===== 3. HELPER FUNCTIONS =====
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

# ===== 4. BOT EVENTS =====
@client.event
async def on_ready():
    if logging_channel:
        await _log("🟢 Bot gestartet - Version 4.5.0")
    
    await client.change_presence(activity=discord.Game(name="!hilfe du kaschber"))
    client.logging_channel = logging_channel
    
    if random_joins == "true":
        if logging_channel:
            await _log(f"📛 Blacklisted Server: {', '.join(blacklisted_guilds) if blacklisted_guilds else 'Keine'}")
            await _log("⏲ Timer wird initialisiert...")
        await create_random_timer(1, 1)
    
    await client.tree.sync()

@client.event
async def on_command_completion(ctx):
    if ctx.author.guild_permissions.administrator:
        return
    
    channel = client.get_channel(logging_channel)
    server = ctx.guild.name if ctx.guild else "DM"
    await channel.send(f"```\n{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} # {ctx.author} used {ctx.command} in {server}```")

@client.event
async def on_guild_join(guild):
    channel = client.get_channel(logging_channel)
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
    if isinstance(error, commands.CheckFailure):
        pass
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        if logging_channel:
            await _log(f"Error in {ctx.command}: {str(error)}")

@client.event
async def on_message(message):
    if not message.author.bot:
        # Track unique users
        if hasattr(client, 'stats_manager'):
            client.stats_manager.stats['unique_users'].add(message.author.id)
            client.stats_manager._save_stats()
    await client.process_commands(message)

@client.event
async def on_application_command_error(interaction, error):
    try:
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
            
            if logging_channel:
                channel = client.get_channel(logging_channel)
                await channel.send(f"```\nFehler bei Slash-Befehl: {error}\nBenutzer: {interaction.user.name} ({interaction.user.id})\nBefehl: {interaction.command.name}```")
    except:
        # Falls die Interaktion bereits beantwortet wurde
        if logging_channel:
            channel = client.get_channel(logging_channel)
            await channel.send(f"```\nFehler bei der Fehlerbehandlung: {error}\nBenutzer: {interaction.user.name} ({interaction.user.id})```")

# ===== 5. BASIC COMMANDS =====
@client.command(name='mett')
@cooldown_check()
async def mett_level(ctx):
    level = random.randint(1, 10)
    mett_meter = "🥓" * level + "⬜" * (10 - level)
    await ctx.send(f"Aktueller Mett-Level: {level}/10\n{mett_meter}")

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
        if str(guild.id) in blacklisted_guilds:
            await _log(f"📛 {guild.name} ({guild.id}) wurde geblacklistet. Überspringe...")
            continue
        await playsound(await get_biggest_vc(guild), get_random_clipname())
        await playsound_cringe(await get_biggest_vc(guild), get_random_clipname_cringe())

    if logging_channel:
        await _log("⤷ ⏲ Neuer Timer wird gesetzt...")
    await create_random_timer(30, 120)

# ===== 7. BOT START =====
# Add sound functions to bot instance
client.playsound = playsound
client.get_random_clipname = get_random_clipname
client.playsound_cringe = playsound_cringe
client.get_random_clipname_cringe = get_random_clipname_cringe

# Start the bot
client.run(token)

