#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import random
import requests
import json
import os
import asyncio
import datetime
from random import randint
from bs4 import BeautifulSoup
from discord import Status  # Neuer Import für Status


## config stuff
def get_blacklisted_guilds(guild_str):
    if guild_str != "":
        return guild_str.split(",")
    else:
        return None


token = str(os.environ['DISCORD_API_TOKEN'])
random_joins = str(os.environ['ENABLE_RANDOM_JOINS']).lower()
logging_channel = int(os.environ['LOGGING_CHANNEL'])
admin_user_id = int(os.environ['ADMIN_USER_ID'])
blacklisted_guilds = get_blacklisted_guilds(
    str(os.environ['BLACKLISTED_GUILDS']))
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Diese Zeile hinzufügen
intents.presences = True  # Diese Zeile hinzufügen
client = commands.Bot(command_prefix=commands.when_mentioned_or(
    "!"), description='Buttergolem Discord Bot Version: 1.5.0 \nCreated by: \nninjazan420 \n!help für Hilfe \n!lord für random GESCHREI \n!cringe oh no, cringe', intents=intents)

# Entferne die Standard-Hilfe und erstelle eine eigene
client.remove_command('help')

@client.command(name='help')
async def help(ctx):
    # Bot Beschreibung
    description = (
        "Buttergolem Discord Bot Version: 1.5.0\n"
        "Created by: ninjazan420\n"
        "!help für Hilfe\n"
        "!lord für random GESCHREI\n"
        "!cringe oh no, cringe\n"
        "\n"  # Leerzeile für bessere Lesbarkeit
    )
    
    # Sammle alle Command-Namen (außer hidden commands)
    commands_list = sorted([command.name for command in client.commands if not command.hidden])
    # Formatiere sie als kommagetrennte Liste
    commands_str = ', '.join(commands_list)
    
    # Sende beide Informationen
    await ctx.send(f'{description}Verfügbare Befehle: {commands_str}')

# simple log function
async def _log(message):
    channel = client.get_channel(logging_channel)
    await channel.send("```\n" + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S # ") + str(message) + "```\n")


# Do this on ready (when joining)
@client.event
async def on_ready():
    if logging_channel:
        await _log("🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢")
    if logging_channel:
        await _log("⏳           Server beigetreten           ⏳")
    if logging_channel:
        await _log("🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢")
        activity = discord.Game(name="Meddl", type=3)
        await client.change_presence(activity=discord.Game(name="!help du kaschber"))
    if random_joins == "true":
        # check blacklisted guilds
        await _log("📛 blacklisted Server: {s}".format(s=''.join(str(e) + "," for e in blacklisted_guilds)))
        # start first timer for random geschrei
        if logging_channel:
            await _log("⏲ Erster Timer wird gesetzt...")
        await create_random_timer(1, 1)


# select the voicechannel with the most members in it (atm)
async def get_biggest_vc(guild):
    if logging_channel:
        await _log("⤷ Grössten VC herausfinden...")

    if logging_channel:
        await _log(f"    ⤷ 🏰 {guild.name} ({guild.id})")

    # initialize with the first voice channel on the guild
    voice_channel_with_most_users = guild.voice_channels[0]

    # go through every voice channel in the guild
    logtext = ""
    for voice_channel in guild.voice_channels:
        # find the one with the most users
        logtext += "\n    ⤷ " + \
            str(len(voice_channel.members)) + " Benutzer in " + voice_channel.name
        if len(voice_channel.members) > len(voice_channel_with_most_users.members):
            voice_channel_with_most_users = voice_channel

    if logging_channel:
        await _log(logtext)
    if logging_channel:
        await _log("    ⤷ 🏁 Vollster VC Kanal: " + voice_channel_with_most_users.name)

    return voice_channel_with_most_users

# Log every command used by a server to a specific channel
@client.event
async def on_command_completion(ctx):
    channel = client.get_channel(logging_channel)  # Nutzt den gleichen Channel wie on_ready
    server = ctx.guild.name if ctx.guild else "DM"
    user = ctx.author
    command = ctx.command
    await channel.send(f"```\n{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} # {user} used {command} in {server}```")


# joins the voicechannel from ctx.message.author
# plays "soundfile.mp3" which should be /app/data/clips/soundfile.mp3
async def playsound(voice_channel, soundfile):
    # create StreamPlayer
    vc = await voice_channel.connect()
    vc.play(discord.FFmpegPCMAudio('/app/data/clips/' +
            str(soundfile)), after=lambda e: print('erledigt', e))
    while vc.is_playing():
        await asyncio.sleep(1)
    # disconnect after the player has finished
    await vc.disconnect()

# joins the voicechannel from ctx.message.author
# plays "soundfile.mp3" which should be /app/data/clips/soundfile.mp3
async def playsound_cringe(voice_channel, soundfile):
    # create StreamPlayer
    vc = await voice_channel.connect()
    vc.play(discord.FFmpegPCMAudio('/app/data/clips/cringe/' +
            str(soundfile)), after=lambda e: print('erledigt', e))
    while vc.is_playing():
        await asyncio.sleep(1)
    # disconnect after the player has finished
    await vc.disconnect()

# get a random datetime object between x (min) to y (max) minutes in the future
def get_random_datetime(min, max):
    randomdatetime = datetime.datetime.now(
    ) + datetime.timedelta(minutes=randint(min, max))
    return randomdatetime


# create timer
async def create_random_timer(min, max):
    minutes = randint(min, max)
    if logging_channel:
        endtime = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
        await _log("⤷ Timer gesetzt! Nächster Drachenlordbesuch: " + endtime.strftime("%d-%m-%Y %H:%M:%S"))
    
    # Wait for the specified minutes
    await asyncio.sleep(minutes * 60)
    # Call the callback directly
    await on_reminder()


# get random filename from /app/data/clips
def get_random_clipname():
    all_clips = os.listdir('app/data/clips')
    return str(random.choice(all_clips))

# get random cringe from /data/clips/cringe
def get_random_clipname_cringe():
    all_clips = os.listdir('/app/data/clips/cringe/')
    return str(random.choice(all_clips))

# this will run when the last timer rings
async def on_reminder():
    if logging_channel:
        await _log("🟠 TIMER! Sound wird abgespielt...")

    # play random sound in the most populated vc, for each guild
    for guild in client.guilds:
        if str(guild.id) in blacklisted_guilds:
            await _log(f"📛 {guild.name} ({guild.id}) wurde geblacklistet. Überspringe...")
        else:
            await playsound(await get_biggest_vc(guild), get_random_clipname())

    for guild in client.guilds:
        if str(guild.id) in blacklisted_guilds:
            await _log(f"📛 {guild.name} ({guild.id}) wurde geblacklistet. Überspringe...")
        else:
            await playsound_cringe(await get_biggest_vc(guild), get_random_clipname_cringe())

    # create next timer
    if logging_channel:
        await _log("⤷ ⏲ Neuer Timer wird gesetzt...")
    
    # set new timer to ring in 30 to 120 minutes
    await create_random_timer(30, 120)


# Quotes stuff
@client.command(pass_context=True)
async def zitat(ctx):
    quotes_jsonfile = open('/app/data/quotes.json', mode="r", encoding="utf-8")
    buttergolem_quotes = json.load(quotes_jsonfile)
    names_jsonfile = open('/app/data/names.json', mode="r", encoding="utf-8")
    buttergolem_names = json.load(names_jsonfile)

    if ctx.message.author == client.user:
        return

    name = random.choice(buttergolem_names)
    quote = random.choice(buttergolem_quotes)
    response = str(name) + " sagt: " + str(quote)

    await ctx.message.channel.send(response)


# some ids for you
@client.command(pass_context=True)
async def id(ctx):
    await ctx.message.channel.send('Aktuelle Server ID: ' + str(ctx.message.guild.id))
    await ctx.message.channel.send('Aktuelle Textchannel ID: ' + str(ctx.message.channel.id))
    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await ctx.message.channel.send('Aktuelle Voicekanal ID: ' + str(voice_channel.id))


# play a selected mp3 in the channel of the user of the provided message-context
async def voice_quote(ctx, soundname):
    # check if the user is in a voice-channel
    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await playsound(voice_channel, soundname)
    # if not, blame him
    else:
        await ctx.message.channel.send('Das funktioniert nur in serverchannels du scheiß HAIDER')


# play random sound in channel of sender
@client.command(pass_context=True)
async def lord(ctx):
    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await playsound(voice_channel, get_random_clipname())
    else:
        await ctx.message.channel.send('Das funktioniert nur in serverchannels du scheiß HAIDER')

# play random cringe in channel of sender
@client.command(pass_context=True)
async def cringe(ctx):
    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await playsound_cringe(voice_channel, get_random_clipname_cringe())
    else:
        await ctx.message.channel.send('Das funktioniert nur in serverchannels du scheiß HAIDER')

# Commands for different sounds
@client.command(pass_context=True)
async def warum(ctx):
    await voice_quote(ctx, "warum.mp3")


@client.command(pass_context=True)
async def frosch(ctx):
    await voice_quote(ctx, "frosch.mp3")


@client.command(pass_context=True)
async def furz(ctx):
    await voice_quote(ctx, "furz.mp3")


@client.command(pass_context=True)
async def idiot(ctx):
    await voice_quote(ctx, "idiot.mp3")


@client.command(pass_context=True)
async def meddl(ctx):
    await voice_quote(ctx, "meddl.mp3")


@client.command(pass_context=True)
async def scheiße(ctx):
    await voice_quote(ctx, "scheiße.mp3")


@client.command(pass_context=True)
async def durcheinander(ctx):
    await voice_quote(ctx, "Durcheinander.mp3")


@client.command(pass_context=True)
async def wiebitte(ctx):
    await voice_quote(ctx, "Wiebitte.mp3")


@client.command(pass_context=True)
async def dick(ctx):
    await voice_quote(ctx, "Dick.mp3")


@client.command(pass_context=True)
async def vorbei(ctx):
    await voice_quote(ctx, "Vorbei.mp3")


@client.command(pass_context=True)
async def hahn(ctx):
    await voice_quote(ctx, "Hahn.mp3")


@client.command(pass_context=True)
async def bla(ctx):
    await voice_quote(ctx, "Blablabla.mp3")


@client.command(pass_context=True)
async def maske(ctx):
    await voice_quote(ctx, "Maske.mp3")


@client.command(pass_context=True)
async def lockdown(ctx):
    await voice_quote(ctx, "Regeln.mp3")


@client.command(pass_context=True)
async def regeln(ctx):
    await voice_quote(ctx, "Regeln2.mp3")


@client.command(pass_context=True)
async def csu(ctx):
    await voice_quote(ctx, "Seehofer.mp3")


@client.command(pass_context=True)
async def lol(ctx):
    await voice_quote(ctx, "LOL.mp3")


@client.command(pass_context=True)
async def huso(ctx):
    await voice_quote(ctx, "Huso.mp3")


@client.command(pass_context=True)
async def bastard(ctx):
    await voice_quote(ctx, "Bastard.mp3")

@client.command(pass_context=True)
async def lappen(ctx):
    await voice_quote(ctx, "Lappen.mp3")

@client.command(pass_context=True)
async def maul2(ctx):
    await voice_quote(ctx, "Maul2.mp3")

@client.command(pass_context=True)
async def wiwi(ctx):
    await voice_quote(ctx, "Wiwi.mp3")

@client.command(pass_context=True)
async def rumwichsen(ctx):
    await voice_quote(ctx, "Rumzuwichsen.mp3")

# Neuer Befehl für Server-Liste (nur für Admin)
@client.command(pass_context=True)
async def server(ctx):
    if ctx.author.id != admin_user_id:
        await ctx.send("Du bist nicht berechtigt, diesen Befehl zu nutzen!")
        return
    
    server_list = "\n".join([f"• {guild.name} (ID: {guild.id})" for guild in client.guilds])
    message = f"```Der Bot ist auf folgenden Servern aktiv:\n{server_list}```"
    await ctx.send(message)
    if logging_channel:
        await _log(f"Admin-Befehl !server wurde von {ctx.author.name} ausgeführt")

# Neuer Befehl für Nutzer-Statistiken (nur für Admin)
@client.command(pass_context=True)
async def user(ctx):
    if ctx.author.id != admin_user_id:
        await ctx.send("Du bist nicht berechtigt, diesen Befehl zu nutzen!")
        return
    
    total_users = 0
    online_users = 0
    server_stats = []
    
    for guild in client.guilds:
        guild_total = len(guild.members)
        # Überprüfe alle Status-Arten, die als "online" gelten
        guild_online = len([m for m in guild.members if m.status in [Status.online, Status.idle, Status.dnd]])
        total_users += guild_total
        online_users += guild_online
        server_stats.append(f"• {guild.name}: {guild_total} Nutzer ({guild_online} online)")
    
    message = f"```Nutzerstatistiken:\n\n"
    message += f"Gesamt über alle Server: {total_users} Nutzer\n"
    message += f"Davon online: {online_users} Nutzer\n\n"
    message += "Details pro Server:\n"
    message += "\n".join(server_stats)
    message += "```"
    
    await ctx.send(message)
    if logging_channel:
        await _log(f"Admin-Befehl !user wurde von {ctx.author.name} ausgeführt")

# finally run our bot ;)
client.run(token)

