#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands, timers
import random
import requests
import json
import os
import asyncio
import datetime
from random import randint
from bs4 import BeautifulSoup


# config stuff
def get_blacklisted_guilds(guild_str):
    if guild_str != "":
        return guild_str.split(",")
    else:
        return None


token = str(os.environ['DISCORD_API_TOKEN'])
random_joins = str(os.environ['ENABLE_RANDOM_JOINS']).lower()
logging_channel = int(os.environ['LOGGING_CHANNEL'])
blacklisted_guilds = get_blacklisted_guilds(
    str(os.environ['BLACKLISTED_GUILDS']))
client = commands.Bot(command_prefix=commands.when_mentioned_or(
    "!"), description='Buttergolem Discord Bot Version: 1.1.0 \nCreated by: \nninja#1337 \n!help für Hilfe \n!lord für random GESCHREI \n!cringe oh no, cringe \n!porn Poste ein neues Bild von porns.to')
client.timer_manager = timers.TimerManager(client)

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
async def on_command(ctx):
    channel = client.get_channel(976866742200590427)
    server = ctx.guild.name
    user = ctx.author
    command = ctx.command
    await channel.send('{} used {} in {}'.format(user, command, server))


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
    # time has to be datetime.datetime object
    # get a random time in the next min-max minutes
    endtime = get_random_datetime(min, max)

    # start timer
    timers.Timer(client, "reminder", endtime).start()
    if logging_channel:
        await _log("⤷ Timer gesetzt! Nächster Drachenlordbesuch: " + endtime.strftime("%d-%m-%Y %H:%M:%S"))


# get random filename from /app/data/clips
def get_random_clipname():
    all_clips = os.listdir('/app/data/clips')
    return str(random.choice(all_clips))

# get random cringe from /data/clips/cringe
def get_random_clipname_cringe():
    all_clips = os.listdir('/app/data/clips/cringe/')
    return str(random.choice(all_clips))

# this will run when the last timer rings
@client.event
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
    
    # set new timer to ring in 30 to 60 minutes
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

# porns.to funktion

@client.command()
async def rnsfw(ctx):
    # Sende eine Anfrage an die URL und lade die HTML-Seite herunter
    response = requests.get("https://porns.to/?random")
    # Parse die HTML-Seite mit BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # Suche das Bild auf der Seite
    image_tag = soup.find('img')
    # Extrahiere die URL des Bildes aus dem img-Tag
    image_url = image_tag['src']
    # Sende das Bild an den Discord-Channel
    await ctx.send(image_url)

# finally run our bot ;)
client.run(token)

