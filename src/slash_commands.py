# -*- coding: utf-8 -*-
import discord
from discord import app_commands
from discord.ext import commands
import random
import json

def register_slash_commands(bot):
    """Registriert zusätzliche Slash Commands"""
    
    # Admin-Konfiguration aus Environment Variables
    import os
    admin_user_id = int(os.getenv('ADMIN_USER_ID'))
    logging_channel = int(os.getenv('LOGGING_CHANNEL'))
    
    async def _log(message):
        """Hilfsfunktion für Logging"""
        import datetime
        channel = bot.get_channel(logging_channel)
        if channel:
            await channel.send(f"```\n{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} # {message}```")
    
    # Entfernt: Doppelter drache-Befehl (siehe Zeile 681 für die vollständige Implementierung)
    
    # Helper function to get quotes
    def get_random_quote():
        """Lädt ein zufälliges Zitat"""
        try:
            import json
            import random
            
            # Versuche verschiedene Pfade für die JSON-Dateien
            data_paths = [
                'src/data/quotes.json',
                'data/quotes.json',
                '../data/quotes.json',
                '/app/data/quotes.json'
            ]
            
            for path in data_paths:
                try:
                    quotes_path = path
                    names_path = path.replace('quotes.json', 'names.json')
                    
                    with open(quotes_path, mode="r", encoding="utf-8") as f:
                        buttergolem_quotes = json.load(f)
                    with open(names_path, mode="r", encoding="utf-8") as f:
                        buttergolem_names = json.load(f)
                    
                    name = random.choice(buttergolem_names)
                    quote = random.choice(buttergolem_quotes)
                    return f"{name} sagt: {quote}"
                except FileNotFoundError:
                    continue
            
            return "Der Drachenlord sagt: Meddl Leude!"
        except Exception:
            return "Der Drachenlord sagt: Meddl Leude!"
    
    @bot.tree.command(name="mett", description="Zeigt den aktuellen Mett-Level")
    async def mett_slash(interaction: discord.Interaction):
        """Zeigt den aktuellen Mett-Level"""
        level = random.randint(1, 10)
        mett_meter = "🥓" * level + "⬜" * (10 - level)
        await interaction.response.send_message(
            f"Aktueller Mett-Level: {level}/10\n{mett_meter}", 
            ephemeral=True
        )
    
    @bot.tree.command(name="zitat", description="Zeigt ein zufälliges Zitat")
    async def zitat_slash(interaction: discord.Interaction):
        """Zeigt ein zufälliges Zitat"""
        quote = get_random_quote()
        await interaction.response.send_message(quote, ephemeral=True)
    
    @bot.tree.command(name="lordmeme", description="Erstellt ein Meme mit dem angegebenen Text")
    @app_commands.describe(
        text="Der Text für das Meme",
        position="Position des Textes (oben/unten/beide)"
    )
    @app_commands.choices(position=[
        app_commands.Choice(name="Oben", value="top"),
        app_commands.Choice(name="Unten", value="bottom"),
        app_commands.Choice(name="Oben und Unten (Text | Text)", value="both")
    ])
    async def lordmeme_slash(interaction: discord.Interaction, text: str, position: str = "top"):
        """Lordmeme Slash Command"""
        # Defer response to prevent timeout during meme generation
        await interaction.response.defer()
        
        try:
            import os
            import discord
            
            # Check if meme generator is available
            if not hasattr(bot, 'meme_generator'):
                await interaction.followup.send(
                    "❌ Meme-Generator ist nicht verfügbar!",
                    ephemeral=True
                )
                return
            
            # Generate meme with position parameter
            output_path = bot.meme_generator.generate_meme(text, position)
            
            # Send meme file
            await interaction.followup.send(
                "🎭 Dein Drachenlord Meme ist fertig!",
                file=discord.File(output_path)
            )
            
            # Clean up temporary file
            os.remove(output_path)
            
        except Exception as e:
            await interaction.followup.send(
                f"❌ Fehler beim Erstellen des Memes: {e}",
                ephemeral=True
            )
    
    # Admin Slash Commands Group
    admin_group = app_commands.Group(name="admin", description="Admin-Befehle für Moderation")
    
    @admin_group.command(name="ban", description="Bannt einen Server oder User")
    @app_commands.describe(
        typ="Server oder User bannen",
        target_id="ID des Servers oder Users",
        reason="Grund für den Ban"
    )
    async def admin_ban_slash(interaction: discord.Interaction, typ: str, target_id: str, reason: str = None):
        """Admin Ban Slash Command"""
        # Check if user is admin
        if interaction.user.id != bot.admin_user_id:
            await interaction.response.send_message("❌ Nur der Administrator kann diesen Befehl nutzen!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        if typ.lower() not in ['server', 'user']:
            await interaction.followup.send("❌ Typ muss 'server' oder 'user' sein!", ephemeral=True)
            return
        
        try:
            if typ.lower() == 'server':
                # Server ban logic
                if target_id.isdigit():
                    seq_id = int(target_id)
                    if seq_id in bot.server_id_map:
                        discord_id = bot.server_id_map[seq_id]
                    else:
                        discord_id = int(target_id)
                else:
                    await interaction.followup.send("❌ Ungültige Server-ID!", ephemeral=True)
                    return
                
                guild = bot.get_guild(discord_id)
                if guild:
                    ban_id = bot.ban_manager.add_ban(
                        server_id=guild.id,
                        server_name=guild.name,
                        reason=reason
                    )
                    await interaction.followup.send(f"🚫 Server `{guild.name}` wurde gebannt! Ban-ID: `{ban_id}`", ephemeral=True)
                else:
                    await interaction.followup.send(f"❌ Server mit ID {target_id} nicht gefunden!", ephemeral=True)
            
            elif typ.lower() == 'user':
                # User ban logic
                if not target_id.isdigit():
                    await interaction.followup.send("❌ Ungültige User-ID!", ephemeral=True)
                    return
                
                user_id = int(target_id)
                try:
                    user = await bot.fetch_user(user_id)
                    username = user.name
                except:
                    username = f"Unbekannter User ({user_id})"
                
                ban_id = bot.ban_manager.add_user_ban(
                    user_id=user_id,
                    username=username,
                    reason=reason
                )
                await interaction.followup.send(f"🚫 User `{username}` wurde gebannt! Ban-ID: `{ban_id}`", ephemeral=True)
        
        except Exception as e:
            await interaction.followup.send(f"❌ Fehler beim Bannen: {str(e)}", ephemeral=True)
    
    @admin_group.command(name="unban", description="Hebt einen Ban auf")
    @app_commands.describe(
        typ="Server oder User unbannen",
        ban_id="Ban-ID"
    )
    async def admin_unban_slash(interaction: discord.Interaction, typ: str, ban_id: str):
        """Admin Unban Slash Command"""
        # Check if user is admin
        if interaction.user.id != bot.admin_user_id:
            await interaction.response.send_message("❌ Nur der Administrator kann diesen Befehl nutzen!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        if typ.lower() not in ['server', 'user']:
            await interaction.followup.send("❌ Typ muss 'server' oder 'user' sein!", ephemeral=True)
            return
        
        try:
            if typ.lower() == 'server':
                ban = bot.ban_manager.get_ban_by_id(ban_id)
                if not ban:
                    await interaction.followup.send(f"❌ Server-Ban mit ID `{ban_id}` nicht gefunden!", ephemeral=True)
                    return
                
                success = bot.ban_manager.remove_ban(ban_id)
                if success:
                    await interaction.followup.send(f"✅ Ban für Server `{ban['server_name']}` wurde aufgehoben!", ephemeral=True)
                else:
                    await interaction.followup.send("❌ Fehler beim Aufheben des Bans!", ephemeral=True)
            
            elif typ.lower() == 'user':
                ban = bot.ban_manager.get_user_ban_by_id(ban_id)
                if not ban:
                    await interaction.followup.send(f"❌ User-Ban mit ID `{ban_id}` nicht gefunden!", ephemeral=True)
                    return
                
                success = bot.ban_manager.remove_user_ban(ban_id)
                if success:
                    await interaction.followup.send(f"✅ Ban für User `{ban['username']}` wurde aufgehoben!", ephemeral=True)
                else:
                    await interaction.followup.send("❌ Fehler beim Aufheben des Bans!", ephemeral=True)
        
        except Exception as e:
            await interaction.followup.send(f"❌ Fehler beim Aufheben des Bans: {str(e)}", ephemeral=True)
    
    @admin_group.command(name="leave", description="Verlässt einen Server")
    @app_commands.describe(
        server_id="Server-ID",
        reason="Grund für das Verlassen (optional, führt zu Ban)"
    )
    async def admin_leave_slash(interaction: discord.Interaction, server_id: str, reason: str = None):
        """Admin Leave Slash Command"""
        # Check if user is admin
        if interaction.user.id != bot.admin_user_id:
            await interaction.response.send_message("❌ Nur der Administrator kann diesen Befehl nutzen!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            if server_id.isdigit():
                seq_id = int(server_id)
                if seq_id in bot.server_id_map:
                    discord_id = bot.server_id_map[seq_id]
                else:
                    discord_id = int(server_id)
            else:
                await interaction.followup.send("❌ Ungültige Server-ID!", ephemeral=True)
                return
            
            guild = bot.get_guild(discord_id)
            if guild:
                await interaction.followup.send(f"🚪 Verlasse Server: {guild.name}...", ephemeral=True)
                await guild.leave()
                
                if reason:
                    ban_id = bot.ban_manager.add_ban(
                        server_id=guild.id,
                        server_name=guild.name,
                        reason=reason
                    )
                    await interaction.edit_original_response(content=f"🚪 Server verlassen und gebannt! Ban-ID: `{ban_id}`")
                else:
                    await interaction.edit_original_response(content="✅ Server erfolgreich verlassen!")
            else:
                await interaction.followup.send(f"❌ Server mit ID {server_id} nicht gefunden!", ephemeral=True)
        
        except Exception as e:
            await interaction.followup.send(f"❌ Fehler beim Verlassen des Servers: {str(e)}", ephemeral=True)
    
    # Add the admin group to the bot's command tree
    bot.tree.add_command(admin_group)
    
    # lordquiz befehl entfernt - nutze /quiz stattdessen
    
    @bot.tree.command(name="ping", description="Zeigt die Bot-Latenz und weitere Informationen")
    async def ping_slash(interaction: discord.Interaction):
        """Zeigt die Bot-Latenz und weitere Informationen öffentlich"""
        latency = round(bot.latency * 1000)
        
        # Zusätzliche Informationen sammeln
        guild_count = len(bot.guilds)
        user_count = sum(guild.member_count for guild in bot.guilds)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            color=0x00ff00
        )
        embed.add_field(name="Latenz", value=f"{latency}ms", inline=True)
        embed.add_field(name="Server", value=f"{guild_count}", inline=True)
        embed.add_field(name="Nutzer", value=f"{user_count:,}", inline=True)
        
        await interaction.response.send_message(embed=embed)
    
    @bot.tree.command(name="quiz", description="Startet ein Drachenlord Quiz")
    @app_commands.describe(rounds="Anzahl der Quiz-Runden (1-20)")
    async def quiz_slash(interaction: discord.Interaction, rounds: int = 5):
        """Startet ein Drachenlord Quiz"""
        if not 1 <= rounds <= 20:
            await interaction.response.send_message("Die Rundenzahl muss zwischen 1 und 20 liegen!", ephemeral=True)
            return
            
        # Importiere Quiz-Funktionen
        import sys
        import os
        sys.path.append(os.path.dirname(__file__))
        
        try:
            from quiz import QuizGame, collect_participants, ask_question, active_games
            
            channel_id = interaction.channel.id
            if channel_id in active_games:
                await interaction.response.send_message("Es läuft bereits ein Quiz in diesem Kanal!", ephemeral=True)
                return
            
            # Erstelle ein Mock-Context Objekt für die Quiz-Funktionen
            class MockContext:
                def __init__(self, interaction):
                    self.channel = interaction.channel
                    self.guild = interaction.guild
                    self.author = interaction.user
                    
                async def send(self, content=None, **kwargs):
                    return await self.channel.send(content, **kwargs)
            
            mock_ctx = MockContext(interaction)
            
            # Starte das Quiz direkt mit dem Benutzer der den Befehl ausgeführt hat
            game = QuizGame(rounds)
            
            # Füge den Benutzer als Teilnehmer hinzu
            from quiz import QuizParticipant
            game.participants[interaction.user.id] = QuizParticipant(interaction.user)
            
            active_games[channel_id] = game
            
            await interaction.response.send_message(
                f"🎮 **Quiz startet!**\n"
                f"Teilnehmer: {interaction.user.mention}\n"
                f"Anzahl Runden: {rounds}\n"
                "Beantworte die Fragen durch Klicken auf die Buttons."
            )
            
            # Starte erste Frage
            await ask_question(mock_ctx)
            
        except ImportError as e:
            await interaction.response.send_message(f"Fehler beim Laden der Quiz-Funktionen: {e}", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"Fehler beim Starten des Quiz: {e}", ephemeral=True)
    
    @bot.tree.command(name="kontakt", description="Sendet eine Nachricht an den Bot-Administrator")
    @app_commands.describe(nachricht="Die Nachricht an den Administrator")
    async def kontakt_slash(interaction: discord.Interaction, nachricht: str):
        """Kontakt-Slash-Command"""
        import uuid
        import datetime
        
        admin_user_id = bot.admin_user_id
        message_history = bot.message_history
        
        try:
            admin_user = await bot.fetch_user(admin_user_id)
            if not admin_user:
                await interaction.response.send_message(
                    "❌ Fehler: Admin konnte nicht gefunden werden!", 
                    ephemeral=True
                )
                return

            message_id = str(uuid.uuid4())[:8]
            message_history[message_id] = interaction.user.id

            embed = discord.Embed(
                title="📨 Neue Nachricht",
                description=nachricht,
                color=0x3498db,
                timestamp=datetime.datetime.now(datetime.UTC)
            )
            embed.add_field(name="Absender", value=f"{interaction.user} (ID: {interaction.user.id})")
            embed.add_field(name="Server", value=interaction.guild.name if interaction.guild else "DM")
            embed.add_field(name="Nachrichten-ID", value=message_id, inline=False)
            embed.set_footer(text=f"Antworte mit: !antwort {message_id} <deine Antwort>")

            await admin_user.send(embed=embed)
            await interaction.response.send_message(
                "✅ Deine Nachricht wurde erfolgreich an den Administrator gesendet!", 
                ephemeral=True
            )
            
            # Log to logging channel if available
            if hasattr(bot, 'logging_channel') and bot.logging_channel:
                try:
                    logging_channel = bot.get_channel(bot.logging_channel)
                    if logging_channel:
                        await logging_channel.send(f"📨 Kontaktnachricht von {interaction.user} (ID: {message_id})")
                except:
                    pass
                    
        except Exception as e:
            await interaction.response.send_message(
                "❌ Fehler beim Senden der Nachricht!", 
                ephemeral=True
            )
    
    @bot.tree.command(name="privacy", description="Zeigt die Datenschutzerklärung")
    async def privacy_slash(interaction: discord.Interaction):
        """Datenschutzerklärung als Slash Command"""
        embed = discord.Embed(
            title="🔐 Datenschutzerklärung",
            description="Informationen zum Datenschutz und zur Datenverarbeitung des Buttergolem Bots",
            color=0x3498db
        )
        
        embed.add_field(
            name="📊 Datensammlung",
            value="• Server-IDs und Kanal-IDs für Bot-Funktionalität\n"
                  "• Benutzer-IDs für Statistiken und Moderation\n"
                  "• Nachrichten-Inhalte nur temporär für KI-Funktionen\n"
                  "• Keine Speicherung persönlicher Daten",
            inline=False
        )
        
        embed.add_field(
            name="🛡️ Datenschutz-Garantien",
            value="• Keine Weitergabe an Dritte\n"
                  "• Automatische Löschung nach 30 Tagen\n"
                  "• Verschlüsselte Datenübertragung\n"
                  "• Minimale Datensammlung (Privacy by Design)",
            inline=False
        )
        
        embed.add_field(
            name="📄 Vollständige Datenschutzerklärung",
            value="[Hier findest du die vollständige Datenschutzerklärung](https://github.com/ninjazan420/drachenlod-bot/blob/master/privacy_policy.md)\n\n"
                  "Bei Fragen: drache@f0ck.org",
            inline=False
        )
        
        embed.set_footer(text="Durch die Nutzung des Bots stimmst du der Datenschutzerklärung zu.")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # ===== NEUE SLASH COMMANDS FÜR MIGRATION =====
    
    @bot.tree.command(name="drache", description="Zeigt Bot-Statistiken und Admin-Funktionen")
    @app_commands.describe(
        action="Die Aktion (stats/neofetch/drachenlord/shrek/butteriq)",
        farbe="Farbauswahl für ASCII-Art (nur bei neofetch/drachenlord/shrek)"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="stats", value="stats"),
        app_commands.Choice(name="neofetch", value="neofetch"),
        app_commands.Choice(name="drachenlord", value="drachenlord"),
        app_commands.Choice(name="shrek", value="shrek"),
        app_commands.Choice(name="butteriq", value="butteriq")
    ])
    @app_commands.choices(farbe=[
        app_commands.Choice(name="🔵 Blau (Standard)", value="blue"),
        app_commands.Choice(name="🔴 Rot", value="red"),
        app_commands.Choice(name="🟢 Grün", value="green"),
        app_commands.Choice(name="🟡 Gelb", value="yellow"),
        app_commands.Choice(name="🟣 Magenta", value="magenta"),
        app_commands.Choice(name="🔵 Cyan", value="cyan"),
        app_commands.Choice(name="⚪ Weiß", value="white"),
        app_commands.Choice(name="🌈 Zufällig", value="random"),
        app_commands.Choice(name="🎨 Gradient", value="gradient")
    ])
    async def drache_slash(interaction: discord.Interaction, action: str = "stats", farbe: str = "blue"):
        """Drache Slash Command"""
        if action == "stats":
            # Import der Stats-Funktionen
            from animated_stats import collect_bot_stats
            
            # Sammle Bot-Statistiken
            stats_text = collect_bot_stats(bot)
            
            embed = discord.Embed(
                title="📊 Bot Statistiken",
                description=stats_text,
                color=0x3498db
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        elif action in ["neofetch", "drachenlord", "shrek"]:
            # Nur für Bot-Owner
            if interaction.user.id != bot.owner_id:
                await interaction.response.send_message(
                    "❌ Nur der Bot-Owner kann diese Funktion nutzen!", 
                    ephemeral=True
                )
                return
            
            from animated_stats import collect_bot_stats, send_animated_stats_with_color
            
            # Sammle Statistiken
            stats_text = collect_bot_stats(bot)
            
            await interaction.response.send_message(
                f"🎨 Zeige Bot-Statistiken im {action}-Stil mit {farbe} Farbe...", 
                ephemeral=True
            )
            
            # Erstelle einen Mock-Context für send_animated_stats
            class MockContext:
                def __init__(self, channel):
                    self.channel = channel
                
                async def send(self, content, **kwargs):
                    return await self.channel.send(content, **kwargs)
            
            mock_ctx = MockContext(interaction.channel)
            await send_animated_stats_with_color(mock_ctx, bot, stats_text, action, farbe, show_quotes=(action == "drachenlord"))
            
        elif action == "butteriq":
            # Admin-only ButterIQ Funktion
            if interaction.user.id != bot.admin_user_id:
                await interaction.response.send_message(
                    "❌ Nur der Administrator kann diese Funktion nutzen!", 
                    ephemeral=True
                )
                return
            
            try:
                from butteriq import ButterIQManager
                
                # Initialisiere ButterIQ Manager falls nicht vorhanden
                if not hasattr(bot, 'butteriq_manager'):
                    bot.butteriq_manager = ButterIQManager()
                
                manager = bot.butteriq_manager
                disabled_count = len(manager.disabled_users)
                
                embed = discord.Embed(
                    title="📊 ButterIQ Status",
                    description=f"Gesperrte Benutzer: {disabled_count}",
                    color=0x3498db
                )
                
                if disabled_count > 0:
                    disabled_list = list(manager.disabled_users)[:10]  # Zeige nur erste 10
                    embed.add_field(
                        name="Gesperrte Benutzer (erste 10)",
                        value="\n".join([f"• <@{uid}>" for uid in disabled_list]),
                        inline=False
                    )
                
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
            except Exception as e:
                await interaction.response.send_message(
                    f"❌ Fehler beim ButterIQ Management: {e}", 
                    ephemeral=True
                )
            
        else:
            await interaction.response.send_message(
                f"❌ Unbekannte Aktion '{action}'. Verfügbare Aktionen: stats, neofetch, drachenlord, shrek, butteriq", 
                ephemeral=True
            )
    
    @bot.tree.command(name="sound", description="Spielt einen bestimmten Sound ab")
    @app_commands.describe(sound_name="Der Name des Sounds")
    async def sound_slash(interaction: discord.Interaction, sound_name: str):
        """Sound Slash Command"""
        if not interaction.user.voice:
            await interaction.response.send_message(
                "❌ Du musst in einem Voice-Channel sein, um Sounds abzuspielen!", 
                ephemeral=True
            )
            return
        
        # Import der Sound-Funktionen
        import os
        from sounds import playsound, SoundBrowser
        
        # Sound-Browser initialisieren
        sound_browser = SoundBrowser()
        sound_name = sound_name.lower().strip()
        
        # Sound suchen
        sound_file = None
        for sound in sound_browser.cached_sounds:
            if sound['command'] == sound_name:
                sound_file = sound['file']
                break
        
        if not sound_file:
            await interaction.response.send_message(
                f"❌ Sound '{sound_name}' nicht gefunden! Nutze `/sounds` um alle verfügbaren Sounds zu sehen.", 
                ephemeral=True
            )
            return
        
        try:
            voice_channel = interaction.user.voice.channel
            await interaction.response.send_message(
                f"🔊 Sound '{sound_name}' wird abgespielt...", 
                ephemeral=True
            )
            await playsound(voice_channel, sound_file, bot)
        except Exception as e:
            await interaction.followup.send(
                f"❌ Fehler beim Abspielen des Sounds: {e}", 
                ephemeral=True
            )
    
    @bot.tree.command(name="lord", description="Spielt einen zufälligen Drachenlord Sound ab")
    async def lord_slash(interaction: discord.Interaction):
        """Lord Slash Command - spielt zufällige Sounds ab"""
        # Prüfe ob User in Voice Channel ist
        if not interaction.user.voice:
            await interaction.response.send_message(
                "❌ Du musst in einem Voice-Channel sein um Sounds abzuspielen!", 
                ephemeral=True
            )
            return

        # Defer response to prevent timeout
        await interaction.response.defer(ephemeral=True)

        try:
            voice_channel = interaction.user.voice.channel
            
            # Import der Sound-Funktionen
            from sounds import playsound, get_random_clipname
            
            # Spiele zufälligen Sound ab
            await playsound(voice_channel, get_random_clipname(), bot)
            
            await interaction.followup.send(
                "🎵 Zufälliger Drachenlord Sound wurde abgespielt!", 
                ephemeral=True
            )
            
        except Exception as e:
            await interaction.followup.send(
                f"❌ Fehler beim Abspielen des Sounds: {e}", 
                ephemeral=True
            )
    # /sounds command ist bereits in sounds.py definiert - doppelte definition entfernt
    
    @bot.tree.command(name="hilfe", description="Zeigt alle verfügbaren Befehle")
    async def hilfe_slash(interaction: discord.Interaction):
        """Hilfe Slash Command - ersetzt den alten /help Befehl"""
        # Prüfe ob User Bot-Owner ist (nicht Server-Admin!)
        is_bot_owner = interaction.user.id == bot.owner_id
        
        embed = discord.Embed(
            title="🤖 Buttergolem Bot - Hilfe",
            description="Alle verfügbaren Slash-Commands im Überblick",
            color=0x3498db
        )
        
        embed.add_field(
            name="🎮 Spiel-Befehle",
            value="• `/quiz` - Drachenlord Quiz\n"
                  "• `/mett` - Mett-Level anzeigen\n"
                  "• `/zitat` - Zufälliges Zitat\n"
                  "• `/lordmeme <text> [position]` - Drachenlord Meme erstellen (oben/unten/beide)",
            inline=False
        )
        
        embed.add_field(
            name="🔊 Sound-Befehle",
            value="• `/sound <name>` - Bestimmten Sound abspielen\n"
                  "• `/sounds` - Alle verfügbaren Sounds anzeigen\n"
                  "• `/lord` - Zufälligen Drachenlord Sound abspielen",
            inline=False
        )
        
        embed.add_field(
            name="📊 Bot-Info & Kontakt",
            value="• `/ping` - Bot-Latenz\n"
                  "• `/drache` - Bot-Statistiken mit Farbauswahl\n"
                  "• `/privacy` - Datenschutzerklärung\n"
                  "• `/kontakt` - Kontakt zum Entwickler",
            inline=False
        )
        
        if is_bot_owner:
            embed.add_field(
                name="⚙️ Bot-Owner Befehle",
                value="• `/server [page]` - Server-Liste & Statistiken\n"
                      "• `/servercount` - Server-Update\n"
                      "• `/antwort` - Admin-Antwort\n"
                      "• `/debug_sounds` - Sound-Debug\n"
                      "• `/butteriq` - ButterIQ Admin-Funktionen\n"
                      "• `/memory` - Memory-Verwaltung",
                inline=False
            )
        
        embed.add_field(
            name="ℹ️ Bot-Informationen",
            value=f"**Owner:** ninjazan420\n"
                  f"**Bot-Version:** 6.0.0\n"
                  f"**Discord.py-Version:** {discord.__version__}\n"
                  f"**Support Server:** [Hier beitreten](https://discord.gg/4kHkaaS2wq)\n"
                  f"**Spenden:** [Ko-fi unterstützen](https://ko-fi.com/buttergolem)",
            inline=False
        )
        
        embed.set_footer(text="Meddl Leudde! ♥️")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @bot.tree.command(name="memory", description="Verwaltet die Memory-Funktionalität (Admin)")
    @app_commands.describe(
        action="Die Aktion (list/show/add/delete)",
        user_id="Die Benutzer-ID",
        data="Zusätzliche Daten"
    )
    async def memory_slash(interaction: discord.Interaction, action: str = "list", user_id: str = None, data: str = None):
        """Memory Slash Command (Admin only)"""
        if interaction.user.id != bot.owner_id:
            await interaction.response.send_message(
                "❌ Nur der Bot-Owner kann diesen Befehl nutzen!", 
                ephemeral=True
            )
            return
        
        if not hasattr(bot, 'memory_manager'):
            await interaction.response.send_message(
                "❌ Memory-Manager ist nicht initialisiert!", 
                ephemeral=True
            )
            return
        
        if action == "list":
            # Liste alle Benutzer mit Erinnerungen auf
            user_ids = bot.memory_manager.get_all_memories()
            
            if not user_ids:
                await interaction.response.send_message(
                    "📋 Keine Erinnerungen gefunden.", 
                    ephemeral=True
                )
                return
            
            embed = discord.Embed(
                title="🧠 Benutzer mit Erinnerungen",
                description=f"Insgesamt {len(user_ids)} Benutzer",
                color=0x3498db
            )
            
            # Versuche, die Benutzernamen zu den IDs zu finden
            user_list = []
            for uid in user_ids[:20]:  # Limitiere auf 20 für bessere Darstellung
                try:
                    memory = bot.memory_manager.load_memory(uid)
                    user_name = memory["user_info"].get("name", "Unbekannt")
                    interactions = memory["interactions_count"]
                    user_list.append(f"• {user_name} (ID: {uid}) - {interactions} Interaktionen")
                except:
                    user_list.append(f"• Unbekannt (ID: {uid})")
            
            embed.add_field(
                name="Benutzer",
                value="\n".join(user_list) if user_list else "Keine Benutzer gefunden",
                inline=False
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        elif action == "show" and user_id:
            try:
                memory = bot.memory_manager.load_memory(user_id)
                
                embed = discord.Embed(
                    title=f"🧠 Erinnerungen für {memory['user_info'].get('name', 'Unbekannt')}",
                    description=f"Benutzer-ID: {user_id}",
                    color=0x3498db
                )
                
                embed.add_field(
                    name="Interaktionen",
                    value=str(memory.get('interactions_count', 0)),
                    inline=True
                )
                
                # Zeige wichtige Fakten
                facts = memory.get('important_facts', [])
                if facts:
                    embed.add_field(
                        name="Wichtige Fakten",
                        value="\n".join([f"• {fact}" for fact in facts[-10:]]),  # Letzte 10
                        inline=False
                    )
                
                # Zeige besprochene Themen
                topics = memory.get('discussed_topics', [])
                if topics:
                    embed.add_field(
                        name="Besprochene Themen",
                        value="\n".join([f"• {topic}" for topic in topics[-10:]]),  # Letzte 10
                        inline=False
                    )
                
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
            except Exception as e:
                await interaction.response.send_message(
                    f"❌ Fehler beim Laden der Erinnerungen: {e}", 
                    ephemeral=True
                )
                
        elif action == "add" and user_id and data:
            try:
                bot.memory_manager.add_important_fact(user_id, data)
                await interaction.response.send_message(
                    f"✅ Wichtiger Fakt für Benutzer {user_id} hinzugefügt: {data}", 
                    ephemeral=True
                )
            except Exception as e:
                await interaction.response.send_message(
                    f"❌ Fehler beim Hinzufügen des Fakts: {e}", 
                    ephemeral=True
                )
                
        elif action == "delete" and user_id:
            try:
                bot.memory_manager.delete_memory(user_id)
                await interaction.response.send_message(
                    f"✅ Erinnerungen für Benutzer {user_id} gelöscht.", 
                    ephemeral=True
                )
            except Exception as e:
                await interaction.response.send_message(
                    f"❌ Fehler beim Löschen der Erinnerungen: {e}", 
                    ephemeral=True
                )
        else:
            # Zeige Hilfe
            embed = discord.Embed(
                title="🧠 Memory-Befehle",
                description="Verwalte die Erinnerungen des Bots an Benutzer",
                color=0x3498db
            )
            
            embed.add_field(
                name="Verfügbare Aktionen",
                value="• `/memory list` - Listet alle Benutzer mit Erinnerungen auf\n"
                      "• `/memory show <user_id>` - Zeigt die Erinnerungen für einen Benutzer\n"
                      "• `/memory add <user_id> <fact>` - Fügt einen wichtigen Fakt hinzu\n"
                      "• `/memory delete <user_id>` - Löscht die Erinnerungen für einen Benutzer",
                inline=False
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
    

    
    # ===== ADMIN SLASH COMMANDS =====
    
    @bot.tree.command(name="servercount", description="Führt ein manuelles Servercounter-Update durch (Admin)")
    async def servercount_slash(interaction: discord.Interaction):
        """Servercount Slash Command (Admin only)"""
        # Admin-Check
        if interaction.user.id != bot.owner_id:
            await interaction.response.send_message(
                "❌ Dieser Befehl ist nur für den Bot-Owner verfügbar!",
                ephemeral=True
            )
            return
        
        await interaction.response.send_message(
            "🔄 Starte manuelles Servercounter Update...",
            ephemeral=True
        )
        
        try:
            import servercounter
            success = await servercounter.single_update(bot)
            
            if success:
                await interaction.followup.send(
                    "✅ Servercounter Update erfolgreich durchgeführt!",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    "❌ Servercounter Update fehlgeschlagen! Überprüfe die Logs.",
                    ephemeral=True
                )
        except Exception as e:
            await interaction.followup.send(
                f"❌ Fehler beim Servercounter Update: {str(e)}",
                ephemeral=True
            )
    
    @bot.tree.command(name="server", description="Zeigt Server-Liste & Statistiken (Admin)")
    @app_commands.describe(page="Seitenzahl der Server-Liste")
    async def server_slash(interaction: discord.Interaction, page: int = 1):
        """Server-Liste Slash Command (Admin only)"""
        # Admin-Check
        if interaction.user.id != bot.owner_id:
            await interaction.response.send_message(
                "❌ Dieser Befehl ist nur für den Bot-Owner verfügbar!",
                ephemeral=True
            )
            return
        
        # Server-Liste abrufen und sortieren
        guilds = list(bot.guilds)
        
        # Import der ServerListView
        from admins.server_list_view import ServerListView
        
        # View erstellen
        view = ServerListView(interaction, guilds, bot.owner_id, bot.logging_channel, bot.server_id_map)
        
        # Setze die aktuelle Seite, falls angegeben
        if page > 0 and page <= view.total_pages:
            view.current_page = page
        
        # Sende das Embed mit der View
        await interaction.response.send_message(embed=view.create_embed(), view=view, ephemeral=True)
        
        # Speichere die Nachricht in der View für spätere Aktualisierungen
        view.message = await interaction.original_response()
        
        if bot.logging_channel:
            try:
                await bot.logging_channel.send(f"Admin-Befehl /server wurde von {interaction.user.name} ausgeführt")
            except:
                pass
    
    @bot.tree.command(name="antwort", description="Sendet eine Admin-Antwort (Admin)")
    @app_commands.describe(
        message_id="Message ID der ursprünglichen Nachricht",
        nachricht="Die Antwort, die gesendet werden soll"
    )
    async def antwort_slash(interaction: discord.Interaction, message_id: str, nachricht: str):
        """Antwort Slash Command (Admin only)"""
        # Admin-Check
        if interaction.user.id != bot.owner_id:
            await interaction.response.send_message(
                "❌ Dieser Befehl ist nur für den Bot-Owner verfügbar!",
                ephemeral=True
            )
            return
        
        try:
            msg_id = int(message_id)
        except ValueError:
            await interaction.response.send_message(
                "❌ Ungültige Message-ID! Muss eine Zahl sein.",
                ephemeral=True
            )
            return
        
        await interaction.response.send_message(
            f"📤 Admin-Antwort auf Nachricht {message_id} wird gesendet...",
            ephemeral=True
        )
        
        try:
            # Importiere message_history aus admin_commands
            from admins.admin_commands import message_history
            
            if msg_id not in message_history:
                await interaction.followup.send(
                    f"❌ Nachricht mit ID `{message_id}` nicht gefunden!",
                    ephemeral=True
                )
                return
            
            original_message = message_history[msg_id]
            user_id = original_message['user_id']
            
            try:
                user = await bot.fetch_user(user_id)
                
                embed = discord.Embed(
                    title="📬 Antwort vom Bot-Administrator",
                    description=nachricht,
                    color=0x3498db,
                    timestamp=discord.utils.utcnow()
                )
                
                embed.add_field(
                    name="Deine ursprüngliche Nachricht:",
                    value=original_message['content'][:1000] + ("..." if len(original_message['content']) > 1000 else ""),
                    inline=False
                )
                
                embed.set_footer(text="Du kannst jederzeit weitere Nachrichten an den Bot senden.")
                
                await user.send(embed=embed)
                
                await interaction.followup.send(
                    f"✅ Antwort an {user.display_name} gesendet!",
                    ephemeral=True
                )
                
            except discord.Forbidden:
                await interaction.followup.send(
                    "❌ Kann keine DM an den User senden (DMs deaktiviert oder Bot blockiert)",
                    ephemeral=True
                )
            except discord.NotFound:
                await interaction.followup.send(
                    "❌ User nicht gefunden!",
                    ephemeral=True
                )
                
        except Exception as e:
            await interaction.followup.send(
                f"❌ Fehler beim Senden der Antwort: {str(e)}",
                ephemeral=True
            )
    
    @bot.tree.command(name="debug_sounds", description="Zeigt Debug-Informationen über das Sound-System (Admin)")
    async def debug_sounds_slash(interaction: discord.Interaction):
        """Debug Sounds Slash Command (Admin only)"""
        if interaction.user.id != bot.owner_id:
            await interaction.response.send_message(
                "❌ Dieser Befehl ist nur für den Bot-Owner verfügbar!", 
                ephemeral=True
            )
            return
        
        await interaction.response.send_message(
            "🔧 Sound-System Debug-Informationen werden geladen...", 
            ephemeral=True
        )
        
        try:
            import os
            import glob
            
            # Sound-Verzeichnis prüfen (korrekter Pfad)
            sound_dir = "/app/data/clips"
            if os.path.exists(sound_dir):
                sound_files = glob.glob(os.path.join(sound_dir, "*.mp3"))
                sound_count = len(sound_files)
            else:
                sound_count = 0
                sound_files = []
                
            # Zusätzlich SoundBrowser Cache prüfen
            try:
                from sounds import sound_browser
                cached_count = len(sound_browser.cached_sounds) if hasattr(sound_browser, 'cached_sounds') else 0
                total_pages = sound_browser.total_pages if hasattr(sound_browser, 'total_pages') else 0
            except:
                cached_count = 0
                total_pages = 0
            
            # Voice Client Status
            voice_clients = len(bot.voice_clients)
            
            # Debug Embed erstellen
            embed = discord.Embed(
                title="🔧 Sound-System Debug",
                color=0xe74c3c,
                timestamp=discord.utils.utcnow()
            )
            
            embed.add_field(
                name="📁 Sound-Dateien",
                value=f"Gefunden: {sound_count} MP3-Dateien\nVerzeichnis: `{sound_dir}`\nCache: {cached_count} Sounds\nSeiten: {total_pages}",
                inline=False
            )
            
            embed.add_field(
                name="🔊 Voice Clients",
                value=f"Aktive Verbindungen: {voice_clients}",
                inline=True
            )
            
            embed.add_field(
                name="🤖 Bot Status",
                value=f"Latenz: {round(bot.latency * 1000)}ms\nServer: {len(bot.guilds)}",
                inline=True
            )
            
            if sound_files:
                # Erste 10 Sound-Dateien anzeigen
                file_list = "\n".join([os.path.basename(f) for f in sound_files[:10]])
                if len(sound_files) > 10:
                    file_list += f"\n... und {len(sound_files) - 10} weitere"
                
                embed.add_field(
                    name="🎵 Verfügbare Sounds (Auswahl)",
                    value=f"```\n{file_list}\n```",
                    inline=False
                )
            
            embed.set_footer(text="Debug-Informationen für Bot-Owner")
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            await interaction.followup.send(
                f"❌ Fehler beim Laden der Debug-Informationen: {str(e)}",
                ephemeral=True
            )
    
    @bot.tree.command(name="butteriq", description="ButterIQ Management (Admin)")
    @app_commands.describe(
        action="Aktion: enable, disable, status",
        user="Benutzer für enable/disable"
    )
    async def butteriq_slash(interaction: discord.Interaction, action: str, user: discord.User = None):
        """ButterIQ Slash Command (Admin only)"""
        # Admin-Check
        if interaction.user.id != bot.owner_id:
            await interaction.response.send_message(
                "❌ Dieser Befehl ist nur für den Bot-Owner verfügbar!",
                ephemeral=True
            )
            return
        
        try:
            from butteriq import ButterIQManager
            
            # Initialisiere ButterIQ Manager falls nicht vorhanden
            if not hasattr(bot, 'butteriq_manager'):
                bot.butteriq_manager = ButterIQManager()
            
            manager = bot.butteriq_manager
            
            if action.lower() == "status":
                disabled_count = len(manager.disabled_users)
                embed = discord.Embed(
                    title="📊 ButterIQ Status",
                    description=f"Gesperrte Benutzer: {disabled_count}",
                    color=0x3498db
                )
                
                if disabled_count > 0:
                    disabled_list = list(manager.disabled_users)[:10]  # Zeige nur erste 10
                    embed.add_field(
                        name="Gesperrte Benutzer (erste 10)",
                        value="\n".join([f"• <@{uid}>" for uid in disabled_list]),
                        inline=False
                    )
                
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
            elif action.lower() == "disable":
                if not user:
                    await interaction.response.send_message(
                        "❌ Bitte gib einen Benutzer an!", 
                        ephemeral=True
                    )
                    return
                
                if manager.disable_user(user.id):
                    await interaction.response.send_message(
                        f"✅ Benutzer {user.mention} wurde für ButterIQ gesperrt!", 
                        ephemeral=True
                    )
                else:
                    await interaction.response.send_message(
                        f"❌ Fehler beim Sperren von {user.mention}!", 
                        ephemeral=True
                    )
                    
            elif action.lower() == "enable":
                if not user:
                    await interaction.response.send_message(
                        "❌ Bitte gib einen Benutzer an!", 
                        ephemeral=True
                    )
                    return
                
                if manager.enable_user(user.id):
                    await interaction.response.send_message(
                        f"✅ Benutzer {user.mention} wurde für ButterIQ entsperrt!", 
                        ephemeral=True
                    )
                else:
                    await interaction.response.send_message(
                        f"❌ Benutzer {user.mention} war nicht gesperrt!", 
                        ephemeral=True
                    )
                    
            else:
                await interaction.response.send_message(
                    "❌ Unbekannte Aktion! Verfügbare Aktionen: status, enable, disable", 
                    ephemeral=True
                )
                
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Fehler beim ButterIQ Management: {e}", 
                ephemeral=True
            )
    
    @bot.tree.command(name="global", description="Sende eine globale Nachricht an alle Community-Update Kanäle")
    @app_commands.describe(nachricht="Die Nachricht, die an alle Server gesendet werden soll")
    async def global_message(interaction: discord.Interaction, nachricht: str):
        """Sendet eine globale Nachricht an alle Community-Update Kanäle"""
        
        # Prüfe Admin-Berechtigung
        if interaction.user.id != admin_user_id:
            await interaction.response.send_message(
                "❌ Du hast keine Berechtigung für diesen Befehl!", 
                ephemeral=True
            )
            return
        
        await interaction.response.defer(ephemeral=True)
        
        sent_count = 0
        failed_count = 0
        
        # Erstelle Embed für die globale Nachricht
        embed = discord.Embed(
            title="📢 Community Update",
            description=nachricht,
            color=0x3498db,
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(text="ButterGolem Community Update")
        
        # Durchlaufe alle Server
        for guild in bot.guilds:
            try:
                # Suche nach Community-Update Kanal
                target_channel = None
                
                # Prüfe System-Channel für Community-Updates
                if guild.system_channel and guild.system_channel_flags.join_notifications:
                    target_channel = guild.system_channel
                
                # Nur System-Channel mit Join-Notifications verwenden
                # Keine anderen Kanäle suchen um Spam zu vermeiden
                
                # Sende Nachricht
                if target_channel:
                    await target_channel.send(embed=embed)
                    sent_count += 1
                else:
                    failed_count += 1
                    
            except Exception as e:
                failed_count += 1
                await _log(f"Fehler beim Senden der globalen Nachricht an {guild.name}: {e}")
        
        # Bestätigungsnachricht
        result_embed = discord.Embed(
            title="✅ Globale Nachricht gesendet",
            description=f"**Erfolgreich:** {sent_count} Server\n**Fehlgeschlagen:** {failed_count} Server",
            color=0x2ecc71
        )
        
        await interaction.followup.send(embed=result_embed, ephemeral=True)
        await _log(f"Admin {interaction.user.name} hat eine globale Nachricht an {sent_count} Server gesendet: {nachricht[:100]}...")

def setup(bot):
    register_slash_commands(bot)