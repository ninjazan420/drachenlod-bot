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
    except Exception as e:
        print(f"Fehler in playsound: {e}")
        raise  # Fehler weitergeben, damit er in der aufrufenden Funktion gefangen wird

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
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def list_sounds(ctx):
        """Zeigt eine durchblätterbare Liste aller verfügbaren Sounds"""
        embed = await sound_browser.create_embed(1)
        message = await ctx.send(embed=embed)
        
        # Keine Reaktionen in DMs hinzufügen
        if not isinstance(ctx.channel, discord.DMChannel):
            await message.add_reaction("⬅️")
            await message.add_reaction("➡️")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"] and reaction.message.id == message.id

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

                except asyncio.TimeoutError:
                    break

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

    @bot.command(name='sound')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def play_sound(ctx, *, sound_name: str = None):
        """Spielt einen bestimmten Sound ab"""
        print(f"!sound Befehl wurde aufgerufen von {ctx.author} mit Argument: {sound_name}")
        
        if sound_name is None:
            await ctx.send("❌ Bitte gib einen Soundnamen an! Beispiel: `!sound adler`")
            return
            
        sound_name = sound_name.lower().strip()
        print(f"Sound-Befehl aufgerufen mit: '{sound_name}'")
        
        # Debug: Zeige alle verfügbaren Sounds
        print(f"Verfügbare Sounds: {[s['command'] for s in sound_browser.cached_sounds[:5]]}... (und {len(sound_browser.cached_sounds)-5} weitere)")
        
        sound_file = None
        for sound in sound_browser.cached_sounds:
            if sound['command'] == sound_name:
                sound_file = sound['file']
                print(f"Sound gefunden: {sound_file}")
                break
        
        if not sound_file:
            await ctx.send(f"❌ Sound '{sound_name}' nicht gefunden! Nutze `!sounds` um alle verfügbaren Sounds zu sehen.")
            return
            
        if not ctx.author.voice:
            await ctx.send('Das funktioniert nur in Voice-Channels du scheiß HAIDER')
            return
        
        try:    
            voice_channel = ctx.author.voice.channel
            print(f"Versuche Sound abzuspielen: {sound_file} in Kanal {voice_channel}")
            
            # Direkter Vergleich mit der lord-Funktion, die funktioniert
            # await playsound(voice_channel, get_random_clipname())  # Dies würde funktionieren (wie !lord)
            await playsound(voice_channel, sound_file)  # Dies scheint nicht zu funktionieren
            
            print(f"Sound wurde abgespielt: {sound_file}")
        except Exception as e:
            print(f"Fehler beim Abspielen des Sounds: {e}")
            await ctx.send(f"❌ Fehler beim Abspielen des Sounds: {e}")

    @bot.command(name='debug_sounds')
    @commands.is_owner()  # Nur für Bot-Besitzer
    async def debug_sounds(ctx):
        """Zeigt Debug-Informationen über Sound-System"""
        sound_dir = '/app/data/clips'
        try:
            files = os.listdir(sound_dir)
            sample_files = files[:10]  # Zeige nur 10 Beispieldateien
            
            sound_info = (
                f"Sound-Verzeichnis: {sound_dir}\n"
                f"Anzahl Dateien: {len(files)}\n"
                f"Beispieldateien: {', '.join(sample_files)}...\n"
                f"Anzahl Sounds im Cache: {len(sound_browser.cached_sounds)}\n"
                f"Sounds pro Seite: {sound_browser.sounds_per_page}\n"
                f"Gesamtseiten: {sound_browser.total_pages}"
            )
            
            await ctx.send(f"```\n{sound_info}\n```")
            
            # Versuche einen bekannten Sound zu finden
            test_sound = "adler"  # Ersetze durch einen Sound, der definitiv existieren sollte
            found = False
            for sound in sound_browser.cached_sounds:
                if sound['command'] == test_sound:
                    await ctx.send(f"Testsuche nach '{test_sound}': GEFUNDEN als {sound['file']}")
                    found = True
                    break
            
            if not found:
                await ctx.send(f"Testsuche nach '{test_sound}': NICHT GEFUNDEN!")
            
        except Exception as e:
            await ctx.send(f"Fehler bei Debug: {str(e)}")

def setup(bot):
    register_sound_commands(bot)
