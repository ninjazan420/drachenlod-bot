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

async def playsound(voice_channel, soundfile, bot=None):
    print(f"playsound aufgerufen mit: {voice_channel}, {soundfile}")
    try:
        vc = await voice_channel.connect()
        print(f"Mit Voice-Channel verbunden, spiele Datei ab: /app/data/clips/{soundfile}")
        vc.play(discord.FFmpegPCMAudio(f'/app/data/clips/{soundfile}'),
                after=lambda e: print('erledigt', e))
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()
        print("Wiedergabe abgeschlossen und Voice-Channel getrennt")

        # Statistiken aktualisieren
        if bot and hasattr(bot, 'stats_manager'):
            bot.stats_manager.increment_sounds_played()
    except Exception as e:
        print(f"Fehler in playsound: {e}")
        raise  # Fehler weitergeben, damit er in der aufrufenden Funktion gefangen wird

async def playsound_cringe(voice_channel, soundfile, bot=None):
    try:
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(f'/app/data/clips/cringe/{soundfile}'),
                after=lambda e: print('erledigt', e))
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()

        # Statistiken aktualisieren
        if bot and hasattr(bot, 'stats_manager'):
            bot.stats_manager.increment_sounds_played()
    except Exception as e:
        print(f"Fehler in playsound_cringe: {e}")
        raise

def register_sound_commands(bot):
    # Create global sound browser instance
    sound_browser = SoundBrowser()

    # Der !lord Befehl wurde zu !drache lord verschoben

    @bot.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)  # Nutze discord.py's eingebautes Cooldown-System
    async def cringe(ctx):
        """Spielt einen zufälligen Cringe-Sound ab"""
        if not ctx.author.voice:
            await ctx.send('Das funktioniert nur in Voice-Channels du scheiß HAIDER')
            return

        voice_channel = ctx.author.voice.channel
        await playsound_cringe(voice_channel, get_random_clipname_cringe(), bot)

    @bot.command(name='lord')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lord_command(ctx):
        """Spielt einen zufälligen Drachenlord Sound ab (!lord Befehl)"""
        if not ctx.author.voice:
            await ctx.send('Das funktioniert nur in Voice-Channels du scheiß HAIDER')
            return

        voice_channel = ctx.author.voice.channel
        await playsound(voice_channel, get_random_clipname(), bot)

    # !sounds befehl entfernt - nur !lord bleibt bestehen

    @bot.tree.command(name="sounds", description="Zeigt eine Liste aller verfügbaren Sounds")
    async def sounds_slash(interaction: discord.Interaction):
        """Zeigt eine durchblätterbare Liste aller verfügbaren Sounds (Slash-Befehl)"""
        embed = await sound_browser.create_embed(1)
        await interaction.response.send_message(embed=embed)

        message = await interaction.original_response()

        # Keine Reaktionen in DMs hinzufügen
        if not isinstance(interaction.channel, discord.DMChannel):
            await message.add_reaction("⬅️")
            await message.add_reaction("➡️")

            def check(reaction, user):
                return user == interaction.user and str(reaction.emoji) in ["⬅️", "➡️"] and reaction.message.id == message.id

            current_page = 1
            while True:
                try:
                    reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)

                    if str(reaction.emoji) == "➡️" and current_page < sound_browser.total_pages:
                        current_page += 1
                    elif str(reaction.emoji) == "⬅️" and current_page > 1:
                        current_page -= 1

                    await message.edit(embed=await sound_browser.create_embed(current_page))

                    # Nur Reaktionen entfernen, wenn wir in einem Gildenkanal sind
                    try:
                        await message.remove_reaction(reaction, user)
                    except discord.errors.Forbidden:
                        pass  # Ignorieren, wenn wir keine Berechtigung haben

                except (asyncio.TimeoutError, discord.errors.Forbidden):
                    break
                except Exception as e:
                    # Keine zweite Antwort versuchen bei Fehlern
                    print(f"Fehler bei der Bearbeitung des sounds-Befehls: {e}")
                    break

    # !sound befehl entfernt - nur !lord bleibt bestehen

    # !debug_sounds befehl entfernt - nur !lord bleibt bestehen

def setup(bot):
    register_sound_commands(bot)
