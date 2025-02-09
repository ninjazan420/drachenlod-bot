import os
import math
import random
import asyncio
import discord
from discord import app_commands
from discord.ext import commands

class SoundBrowser:
    def __init__(self, clips_dir='/app/data/clips'):
        self.clips_dir = clips_dir
        self.sounds_per_page = 50
        self.cached_sounds = []
        self.load_sounds()

    def load_sounds(self):
        sounds = []
        for file in os.listdir(self.clips_dir):
            if file.endswith('.mp3'):
                command_name = os.path.splitext(file)[0].lower()
                sounds.append({
                    'file': file,
                    'command': command_name
                })
        self.cached_sounds = sorted(sounds, key=lambda x: x['command'])
        self.total_pages = math.ceil(len(self.cached_sounds) / self.sounds_per_page)

    def get_page(self, page):
        start_idx = (page - 1) * self.sounds_per_page
        end_idx = start_idx + self.sounds_per_page
        return self.cached_sounds[start_idx:end_idx]

    async def create_embed(self, page):
        sounds = self.get_page(page)
        
        embed = discord.Embed(
            title="🎵 Verfügbare Sounds",
            description="Nutze `!sound <name>` um einen Sound abzuspielen",
            color=0x3498db
        )

        if sounds:
            columns = [[], [], []]
            col_size = len(sounds) // 3 + (1 if len(sounds) % 3 > 0 else 0)
            
            for i, sound in enumerate(sounds):
                col_index = i // col_size
                if col_index < 3:
                    columns[col_index].append(sound['command'])

            for i, column in enumerate(columns):
                if column:
                    col_text = '\n'.join(f'`{cmd:<20}`' for cmd in column)
                    embed.add_field(name='​', value=col_text, inline=True)

        embed.set_footer(text=f"Seite {page}/{self.total_pages} • Navigiere mit ⬅️ ➡️")
        return embed

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

def register_sound_commands(bot):
    # Create global sound browser instance
    sound_browser = SoundBrowser()

    @bot.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)  # Nutze discord.py's eingebautes Cooldown-System
    async def lord(ctx):
        """Spielt einen zufälligen Sound ab"""
        if not ctx.author.voice:
            await ctx.send('Das funktioniert nur in Voice-Channels du scheiß HAIDER')
            return
            
        voice_channel = ctx.author.voice.channel
        await playsound(voice_channel, get_random_clipname())

    @bot.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)  # Nutze discord.py's eingebautes Cooldown-System
    async def cringe(ctx):
        """Spielt einen zufälligen Cringe-Sound ab"""
        if not ctx.author.voice:
            await ctx.send('Das funktioniert nur in Voice-Channels du scheiß HAIDER')
            return
            
        voice_channel = ctx.author.voice.channel
        await playsound_cringe(voice_channel, get_random_clipname_cringe())

    @bot.command(name='sounds')
    @commands.cooldown(1, 5, commands.BucketType.user)  # Ersetze die alte Cooldown-Prüfung
    async def list_sounds(ctx):
        """Zeigt eine durchblätterbare Liste aller verfügbaren Sounds"""
        embed = await sound_browser.create_embed(1)
        message = await ctx.send(embed=embed)
        
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"]

        current_page = 1
        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)

                if str(reaction.emoji) == "➡️" and current_page < sound_browser.total_pages:
                    current_page += 1
                elif str(reaction.emoji) == "⬅️" and current_page > 1:
                    current_page -= 1
                
                await message.edit(embed=await sound_browser.create_embed(current_page))
                await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                break

    @bot.tree.command(name="sounds", description="Zeigt eine Liste aller verfügbaren Sounds")
    async def sounds_slash(interaction: discord.Interaction):
        embed = await sound_browser.create_embed(1)
        await interaction.response.send_message(embed=embed)
        
        message = await interaction.original_response()
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        def check(reaction, user):
            return user == interaction.user and str(reaction.emoji) in ["⬅️", "➡️"]

        current_page = 1
        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)

                if str(reaction.emoji) == "➡️" and current_page < sound_browser.total_pages:
                    current_page += 1
                elif str(reaction.emoji) == "⬅️" and current_page > 1:
                    current_page -= 1
                
                await message.edit(embed=await sound_browser.create_embed(current_page))
                await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                break

    @bot.command(name='sound')
    @commands.check(lambda ctx: hasattr(bot, 'cooldown_check') and bot.cooldown_check()(ctx))
    async def play_sound(ctx, sound_name: str):
        """Spielt einen bestimmten Sound ab"""
        sound_name = sound_name.lower()
        
        sound_file = None
        for sound in sound_browser.cached_sounds:
            if sound['command'] == sound_name:
                sound_file = sound['file']
                break
        
        if not sound_file:
            await ctx.send("❌ Sound nicht gefunden! Nutze `!sounds` um alle verfügbaren Sounds zu sehen.")
            return
            
        if hasattr(ctx.message.author, "voice"):
            voice_channel = ctx.message.author.voice.channel
            await playsound(voice_channel, sound_file)
        else:
            await ctx.send('Das funktioniert nur in Voice-Channels du scheiß HAIDER')

def setup(bot):
    register_sound_commands(bot)
