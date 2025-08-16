import json
import random
import asyncio
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
import time
import datetime

def load_hangman_words():
    """Lädt Hangman-Wörter aus JSON-Datei"""
    try:
        with open('/app/data/hangman_words.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # Fallback-Wörter falls Datei nicht existiert
        return {
            "words": [
                {"word": "DRACHENLORD", "hint": "Der Lord himself"},
                {"word": "MEDDL", "hint": "Berühmter Gruß"},
                {"word": "SCHANZE", "hint": "Ehemaliges Zuhause"},
                {"word": "HAIDER", "hint": "Unerwünschte Besucher"},
                {"word": "WINKLER", "hint": "Nachname des Lords"},
                {"word": "ALTSCHAUERBERG", "hint": "Berühmte Adresse"},
                {"word": "RAINER", "hint": "Echter Vorname"},
                {"word": "BUTTERGOLEM", "hint": "Dieser Bot"},
                {"word": "METTWURST", "hint": "Lieblingsspeise"},
                {"word": "UNTERKIEFER", "hint": "Markantes Merkmal"}
            ]
        }

def load_hangman_rankings():
    """Lädt Hangman-Rankings aus JSON-Datei"""
    try:
        with open('/app/data/rankings.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # Erstelle leere Rankings-Struktur
        return {
            "correct_letters": {},  # {user_id: count}
            "games_won": {}  # {user_id: count}
        }

def save_hangman_rankings(rankings):
    """Speichert Hangman-Rankings in JSON-Datei"""
    try:
        import os
        os.makedirs('/app/data', exist_ok=True)
        with open('/app/data/rankings.json', 'w', encoding='utf-8') as file:
            json.dump(rankings, file, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving hangman rankings: {e}")

def update_player_stats(user_id, correct_letters=0, won_game=False):
    """Aktualisiert Spieler-Statistiken"""
    rankings = load_hangman_rankings()

    user_id_str = str(user_id)

    # Aktualisiere richtige Buchstaben
    if correct_letters > 0:
        if user_id_str not in rankings["correct_letters"]:
            rankings["correct_letters"][user_id_str] = 0
        rankings["correct_letters"][user_id_str] += correct_letters

    # Aktualisiere gewonnene Spiele
    if won_game:
        if user_id_str not in rankings["games_won"]:
            rankings["games_won"][user_id_str] = 0
        rankings["games_won"][user_id_str] += 1

    save_hangman_rankings(rankings)

class HangmanParticipant:
    def __init__(self, user):
        self.user = user
        self.score = 0
        self.has_guessed = False
        self.last_guess = None

class HangmanGame:
    def __init__(self, guild_id=None):
        self.guild_id = guild_id
        self.participants = {}  # {user_id: HangmanParticipant}
        self.current_word = None
        self.current_hint = None
        self.guessed_letters = set()
        self.wrong_letters = set()
        self.message = None
        self.thread = None
        self.active = True
        self.max_wrong = 6
        self.game_won = False
        self.current_guesser = None
        self.turn_order = []
        self.turn_index = 0
        self.last_activity = time.time()
        self.winner_user_id = None  # ID des Users der das Wort gelöst hat

    def get_display_word(self):
        """Zeigt das Wort mit erratenen Buchstaben"""
        return ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.current_word])

    def get_hangman_ascii(self):
        """ASCII-Art für Hangman basierend auf falschen Versuchen"""
        stages = [
            # 0 falsche Versuche
            "```\n  +---+\n  |   |\n      |\n      |\n      |\n ======```",
            # 1 falscher Versuch
            "```\n  +---+\n  |   |\n  O   |\n      |\n      |\n ======```",
            # 2 falsche Versuche
            "```\n  +---+\n  |   |\n  O   |\n  |   |\n      |\n ======```",
            # 3 falsche Versuche
            "```\n  +---+\n  |   |\n  O   |\n /|   |\n      |\n ======```",
            # 4 falsche Versuche
            "```\n  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n ======```",
            # 5 falsche Versuche
            "```\n  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n ======```",
            # 6 falsche Versuche (Game Over)
            "```\n  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n ======```"
        ]
        return stages[min(len(self.wrong_letters), 6)]

    def is_word_complete(self):
        """Prüft ob das Wort vollständig erraten wurde"""
        return all(letter in self.guessed_letters for letter in self.current_word)

    def is_game_over(self):
        """Prüft ob das Spiel vorbei ist"""
        return len(self.wrong_letters) >= self.max_wrong or self.is_word_complete()

    def get_next_player(self):
        """Bestimmt den nächsten Spieler"""
        if not self.turn_order:
            return None
        self.turn_index = (self.turn_index + 1) % len(self.turn_order)
        return self.turn_order[self.turn_index]

# Globale Variable für aktive Spiele
active_hangman_games = {}  # {guild_id: HangmanGame}  # Geändert zu guild_id für server-weite Spiele
hangman_words = load_hangman_words()

async def show_hangman_help(ctx):
    """Zeigt Hangman-Hilfe"""
    embed = discord.Embed(
        title="🎮 Hangman Hilfe 🎮",
        color=0x00ff00
    )
    
    embed.add_field(
        name="📋 Befehle",
        value="`/hangman` - Startet ein neues Hangman-Spiel\n\n"
              "Das Spiel wird in einem eigenen Thread gespielt um Spam zu vermeiden.",
        inline=False
    )
    
    embed.add_field(
        name="🎯 Spielregeln",
        value="• Errate das Wort Buchstabe für Buchstabe\n"
              "• Jeder Spieler ist abwechselnd dran\n"
              "• 6 falsche Versuche = Game Over\n"
              "• Alle Wörter haben Drachenlord-Bezug",
        inline=False
    )
    
    embed.add_field(
        name="⚠️ Anti-Spam",
        value="Das Spiel läuft in einem separaten Thread.\n"
              "Nachrichten außerhalb des Threads werden automatisch gelöscht.",
        inline=False
    )
    
    await ctx.send(embed=embed)

async def collect_hangman_participants(ctx, game):
    """Sammelt Teilnehmer für Hangman"""
    signup_msg = await ctx.send(
        "🎮 **Neue Hangman-Runde startet!**\n"
        "Reagiere mit 🎯 um teilzunehmen!\n"
        "Start in 20 Sekunden..."
    )
    await signup_msg.add_reaction("🎯")
    
    await asyncio.sleep(20)  # 20 Sekunden Wartezeit
    
    # Hole aktualisierte Nachricht um alle Reaktionen zu sehen
    signup_msg = await ctx.channel.fetch_message(signup_msg.id)
    reaction = discord.utils.get(signup_msg.reactions, emoji="🎯")
    
    if reaction:
        async for user in reaction.users():
            if not user.bot:
                game.participants[user.id] = HangmanParticipant(user)
                game.turn_order.append(user.id)
    
    return len(game.participants) > 0

async def start_hangman(ctx):
    """Startet ein neues Hangman-Spiel"""
    guild_id = ctx.guild.id if ctx.guild else None
    if not guild_id:
        await ctx.send("❌ Hangman kann nur auf Servern gespielt werden!")
        return

    if guild_id in active_hangman_games:
        # Es läuft bereits ein Spiel auf diesem Server
        existing_game = active_hangman_games[guild_id]
        thread_mention = existing_game.thread.mention if existing_game.thread else "Unknown Thread"

        msg = await ctx.send(
            f"❌ **Es läuft bereits ein Hangman-Spiel auf diesem Server!**\n"
            f"🧵 **Aktuelles Spiel:** {thread_mention}\n\n"
            f"Warte bis das aktuelle Spiel beendet ist oder tritt dem laufenden Spiel bei!"
        )

        # Lösche die Nachricht nach 10 Sekunden
        await asyncio.sleep(10)
        try:
            await msg.delete()
        except:
            pass
        return

    # Prüfe Bot-Berechtigungen
    bot_member = ctx.guild.me if ctx.guild else None
    if bot_member:
        channel_perms = ctx.channel.permissions_for(bot_member)
        if not channel_perms.create_public_threads:
            await ctx.send("❌ **Fehlende Berechtigung!**\nIch brauche die `Erstelle öffentliche Threads` Rolle um Hangman zu starten!")
            return
        if not channel_perms.manage_messages:
            await ctx.send("❌ **Fehlende Berechtigung!**\nnIch brauche die `Nachrichten bearbeiten` Rolle um Hangman zu starten!")
            return

    game = HangmanGame(guild_id)
    
    # Sammle Teilnehmer
    has_participants = await collect_hangman_participants(ctx, game)
    
    if not has_participants:
        await ctx.send("❌ Keine Teilnehmer gefunden. Hangman wird abgebrochen!")
        return
    
    # Wähle zufälliges Wort
    word_data = random.choice(hangman_words["words"])
    game.current_word = word_data["word"].upper()
    game.current_hint = word_data["hint"]
    
    active_hangman_games[guild_id] = game
    
    participant_mentions = " ".join([f"{p.user.mention}" for p in game.participants.values()])
    
    # Erstelle Thread für das Spiel
    thread_name = f"🎯 Hangman - {game.current_hint}"
    game.thread = await ctx.channel.create_thread(
        name=thread_name,
        type=discord.ChannelType.public_thread,
        auto_archive_duration=60  # 1 Stunde (falls nicht gelöscht wird)
    )
    
    # Lade alle Teilnehmer in den Thread ein
    for participant in game.participants.values():
        try:
            await game.thread.add_user(participant.user)
        except:
            pass  # Ignoriere Fehler beim Hinzufügen
    
    # Countdown vor Spielstart
    countdown_msg = await ctx.send(f"🎯 **Achtung {participant_mentions}!**\nDas Spiel beginnt in...")
    for i in range(3, 0, -1):
        await countdown_msg.edit(content=f"🎯 **Achtung {participant_mentions}!**\nDas Spiel beginnt in...\n**{i}**")
        await asyncio.sleep(1)
    await countdown_msg.edit(content=f"🎯 **Los geht's! {participant_mentions}**\n\n🧵 **Das Spiel läuft im Thread: {game.thread.mention}**")

    # Warte kurz und lösche dann die Nachrichten im Hauptchannel um Spam zu vermeiden
    await asyncio.sleep(5)  # 5 Sekunden warten damit User den Thread-Link sehen können

    try:
        # Lösche die Countdown-Nachricht
        await countdown_msg.delete()

        # Lösche auch die ursprüngliche Signup-Nachricht falls sie noch existiert
        try:
            async for message in ctx.channel.history(limit=10):
                if (message.author.bot and
                    ("🎯 **Hangman startet!**" in message.content or "Neue Hangman-Runde startet!" in message.content) and
                    message.created_at > datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=5)):
                    try:
                        await message.delete()
                    except:
                        pass
                    break
        except Exception as cleanup_error:
            print(f"Error during signup message cleanup: {cleanup_error}")
    except Exception as e:
        print(f"Error cleaning up hangman messages: {e}")

    # Starte das Spiel im Thread
    await start_hangman_round(game)

async def start_hangman_round(game):
    """Startet eine Hangman-Runde im Thread"""
    if not game.thread:
        return
    
    # Bestimme ersten Spieler
    game.current_guesser = game.turn_order[0]
    current_player = game.participants[game.current_guesser]
    
    # ASCII-Art für Hangman-Titel
    hangman_title = r"""
```

  /\  /\__ _ _ __   __ _ _ __ ___   __ _ _ __
 / /_/ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \
/ __  / (_| | | | | (_| | | | | | | (_| | | | |
\/ /_/ \__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                   |___/


```
"""
    
    embed = discord.Embed(
        title="🎯 Hangman - Drachenlord Edition",
        description=hangman_title,
        color=0x00ff00
    )
    
    embed.add_field(
        name="💡 Hinweis",
        value=f"**{game.current_hint}**",
        inline=False
    )
    
    embed.add_field(
        name="🔤 Wort",
        value=f"`{game.get_display_word()}`",
        inline=False
    )
    
    embed.add_field(
        name="🎯 Aktueller Spieler",
        value=f"{current_player.user.mention} ist dran!",
        inline=True
    )
    
    embed.add_field(
        name="❌ Falsche Buchstaben",
        value="Noch keine" if not game.wrong_letters else " ".join(sorted(game.wrong_letters)),
        inline=True
    )
    
    embed.add_field(
        name="📊 Hangman",
        value=game.get_hangman_ascii(),
        inline=False
    )
    
    game.message = await game.thread.send(embed=embed)
    
    # Starte Timeout-Timer
    asyncio.create_task(hangman_timeout_check(game))

async def hangman_timeout_check(game):
    """Prüft auf Timeout und beendet das Spiel bei Inaktivität"""
    await asyncio.sleep(600)  # 10 Minuten Timeout
    
    if game.active and time.time() - game.last_activity > 300:
        game.active = False
        if game.thread:
            await game.thread.send("⏰ **Spiel beendet wegen Inaktivität!**\n"
                                 f"Das Wort war: **{game.current_word}**")
            # Cleanup
            if game.guild_id in active_hangman_games:
                del active_hangman_games[game.guild_id]

async def process_hangman_guess(game, user, guess):
    """Verarbeitet einen Buchstaben-Tipp"""
    if not game.active or game.is_game_over():
        return False
    
    # Prüfe ob der User dran ist
    if user.id != game.current_guesser:
        current_player = game.participants[game.current_guesser]
        await game.thread.send(f"❌ {user.mention}, du bist nicht dran! {current_player.user.mention} ist am Zug.", delete_after=5)
        return False
    
    guess = guess.upper()
    
    # Prüfe ob Buchstabe bereits geraten wurde
    if guess in game.guessed_letters or guess in game.wrong_letters:
        await game.thread.send(f"❌ {user.mention}, der Buchstabe **{guess}** wurde bereits geraten!", delete_after=5)
        return False
    
    game.last_activity = time.time()
    
    # Verarbeite den Tipp
    if guess in game.current_word:
        game.guessed_letters.add(guess)
        game.participants[user.id].score += 1
        result_msg = f"✅ **{guess}** ist richtig!"
        # Aktualisiere Statistiken für richtigen Buchstaben
        update_player_stats(user.id, correct_letters=1)

        # Prüfe ob das Wort jetzt komplett ist (dieser User hat das Wort gelöst!)
        if game.is_word_complete():
            # Dieser User hat das komplette Wort gelöst und bekommt einen Gewinn-Punkt
            update_player_stats(user.id, won_game=True)
            game.winner_user_id = user.id  # Merke dir wer gewonnen hat
    else:
        game.wrong_letters.add(guess)
        result_msg = f"❌ **{guess}** ist falsch!"
    
    # Nächster Spieler
    game.current_guesser = game.get_next_player()
    
    await update_hangman_display(game, result_msg)
    
    # Prüfe Spielende
    if game.is_game_over():
        await end_hangman_game(game)
    
    return True

async def update_hangman_display(game, result_msg):
    """Aktualisiert die Hangman-Anzeige"""
    if not game.message or not game.thread:
        return
    
    current_player = game.participants[game.current_guesser] if game.current_guesser else None
    
    embed = discord.Embed(
        title="🎯 Hangman - Drachenlord Edition",
        description=f"```\n|-| /\\ |\\| (_, |\\/| /\\ |\\| \n```\n{result_msg}",
        color=0x00ff00 if not game.is_game_over() else (0xff0000 if len(game.wrong_letters) >= game.max_wrong else 0x00ff00)
    )
    
    embed.add_field(
        name="💡 Hinweis",
        value=f"**{game.current_hint}**",
        inline=False
    )
    
    embed.add_field(
        name="🔤 Wort",
        value=f"`{game.get_display_word()}`",
        inline=False
    )
    
    if current_player and not game.is_game_over():
        embed.add_field(
            name="🎯 Aktueller Spieler",
            value=f"{current_player.user.mention} ist dran!",
            inline=True
        )
    
    embed.add_field(
        name="❌ Falsche Buchstaben",
        value="Noch keine" if not game.wrong_letters else " ".join(sorted(game.wrong_letters)),
        inline=True
    )
    
    embed.add_field(
        name="📊 Hangman",
        value=game.get_hangman_ascii(),
        inline=False
    )
    
    try:
        await game.message.edit(embed=embed)
    except:
        pass

async def end_hangman_game(game):
    """Beendet das Hangman-Spiel"""
    game.active = False
    
    if game.is_word_complete():
        # Gewonnen!
        rankings = sorted(game.participants.values(), key=lambda p: p.score, reverse=True)

        # Finde den echten Gewinner (wer das Wort gelöst hat)
        winner_user = None
        if game.winner_user_id and game.winner_user_id in game.participants:
            winner_user = game.participants[game.winner_user_id].user

        if winner_user:
            winner_text = f"🎉 **{winner_user.mention} hat das Wort gelöst!**\n"
            winner_text += f"Das Wort war: **{game.current_word}**\n\n"
        else:
            winner_text = f"🎉 **Gewonnen!** Das Wort war: **{game.current_word}**\n\n"

        if rankings:
            winner_text += "🏆 **Punktestand:**\n"
            for idx, participant in enumerate(rankings):
                emoji = "👑" if participant.user.id == game.winner_user_id else f"{idx + 1}."
                winner_text += f"{emoji} {participant.user.mention}: **{participant.score} Punkte**\n"
    else:
        # Verloren
        winner_text = f"💀 **Game Over!** Das Wort war: **{game.current_word}**\n\n"
        winner_text += "Beim nächsten Mal klappt's bestimmt!"
    
    embed = discord.Embed(
        title="🎮 Hangman beendet!",
        description=winner_text,
        color=0x00ff00 if game.is_word_complete() else 0xff0000
    )
    
    if game.thread:
        await game.thread.send(embed=embed)

        # Thread nach 30 Sekunden löschen (schnelle Bereinigung)
        await asyncio.sleep(30)  # 30 Sekunden warten damit User das Ergebnis sehen können
        try:
            await game.thread.delete()
            print(f"Hangman-Thread {game.thread.id} wurde nach Spielende gelöscht")
        except Exception as e:
            print(f"Fehler beim Löschen des Hangman-Threads: {e}")
            # Fallback: Thread archivieren falls löschen fehlschlägt
            try:
                await game.thread.edit(archived=True)
                print(f"Hangman-Thread {game.thread.id} wurde archiviert (Fallback)")
            except:
                pass
    
    # Cleanup - entferne Spiel aus aktiven Spielen
    if game.guild_id in active_hangman_games:
        del active_hangman_games[game.guild_id]
        print(f"Hangman-Spiel für Guild {game.guild_id} aus aktiven Spielen entfernt")

async def cleanup_inactive_games():
    """Bereinigt inaktive Hangman-Spiele und löscht Threads"""
    current_time = time.time()
    games_to_remove = []

    for guild_id, game in active_hangman_games.items():
        # Spiele die länger als 10 Minuten inaktiv sind
        if current_time - game.last_activity > 600:  # 10 Minuten
            games_to_remove.append(guild_id)
            if game.thread:
                try:
                    await game.thread.send("⏰ **Spiel automatisch beendet wegen Inaktivität!**")
                    # Thread nach kurzer Wartezeit löschen
                    await asyncio.sleep(10)  # 10 Sekunden warten
                    await game.thread.delete()
                    print(f"Inaktiver Hangman-Thread {game.thread.id} wurde gelöscht")
                except Exception as e:
                    print(f"Fehler beim Löschen des inaktiven Hangman-Threads: {e}")
                    # Fallback: Thread archivieren
                    try:
                        await game.thread.edit(archived=True)
                    except:
                        pass

    for guild_id in games_to_remove:
        del active_hangman_games[guild_id]

def get_hangman_stats():
    """Gibt Hangman-Statistiken zurück"""
    return {
        "active_games": len(active_hangman_games),
        "total_participants": sum(len(game.participants) for game in active_hangman_games.values()),
        "available_words": len(hangman_words.get("words", []))
    }

async def show_hangman_rankings(bot, user):
    """Zeigt Hangman-Rankings für einen User"""
    rankings = load_hangman_rankings()

    # Sortiere nach richtigen Buchstaben
    letter_rankings = sorted(
        rankings["correct_letters"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]  # Top 10

    # Sortiere nach gewonnenen Spielen
    win_rankings = sorted(
        rankings["games_won"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]  # Top 10

    embed = discord.Embed(
        title="🏆 Hangman Rankings",
        description="The best Hangman players!",
        color=0xffd700  # Gold
    )

    # Richtige Buchstaben Ranking
    if letter_rankings:
        letter_text = ""
        for idx, (user_id, count) in enumerate(letter_rankings):
            try:
                discord_user = await bot.fetch_user(int(user_id))
                username = discord_user.display_name if hasattr(discord_user, 'display_name') else discord_user.name
            except Exception:
                username = f"Unknown User"

            # Emoji für Top 3
            if idx == 0:
                emoji = "🥇"
            elif idx == 1:
                emoji = "🥈"
            elif idx == 2:
                emoji = "🥉"
            else:
                emoji = f"{idx + 1}."

            letter_text += f"{emoji} **{username}**: {count} letters\n"

        embed.add_field(
            name="📝 Meisten richtige Buchstaben",
            value=letter_text,
            inline=True
        )

    # Gewonnene Spiele Ranking
    if win_rankings:
        win_text = ""
        for idx, (user_id, count) in enumerate(win_rankings):
            try:
                discord_user = await bot.fetch_user(int(user_id))
                username = discord_user.display_name if hasattr(discord_user, 'display_name') else discord_user.name
            except Exception:
                username = f"Unknown User"

            # Emoji für Top 3
            if idx == 0:
                emoji = "🥇"
            elif idx == 1:
                emoji = "🥈"
            elif idx == 2:
                emoji = "🥉"
            else:
                emoji = f"{idx + 1}."

            win_text += f"{emoji} **{username}**: {count} wins\n"

        embed.add_field(
            name="🏆 Meisten gewonnene Spiele",
            value=win_text,
            inline=True
        )

    if not letter_rankings and not win_rankings:
        embed.description = "No rankings available yet! Play some Hangman games to get on the leaderboard!"

    return embed

async def cleanup_all_hangman_threads(bot):
    """Bereinigt alle Hangman-Threads beim Bot-Start (falls welche übrig sind)"""
    try:
        for guild in bot.guilds:
            for channel in guild.text_channels:
                for thread in channel.threads:
                    if thread.name.startswith("🎯 Hangman -"):
                        try:
                            await thread.delete()
                            print(f"Alter Hangman-Thread {thread.id} beim Bot-Start gelöscht")
                        except:
                            pass
        # Leere auch das active_hangman_games dict
        active_hangman_games.clear()
        print("Alle alten Hangman-Threads bereinigt")
    except Exception as e:
        print(f"Fehler beim Bereinigen alter Hangman-Threads: {e}")

def register_hangman_commands(bot):
    """Registriert Hangman-Commands und startet Cleanup-Tasks"""

    # Hangman Slash Command
    @bot.tree.command(name="hangman", description="🎯 Spiele Hangman mit Drachenlord-Wörtern!")
    @discord.app_commands.checks.cooldown(1, 30.0)  # 30 Sekunden Cooldown
    async def hangman_slash(interaction: discord.Interaction):
        """Hangman Slash Command - Drachenlord Hangman Spiel"""
        try:
            # Mock Context für Kompatibilität mit bestehenden Funktionen
            class MockContext:
                def __init__(self, interaction):
                    self.channel = interaction.channel
                    self.guild = interaction.guild
                    self.author = interaction.user
                    self.send = interaction.channel.send

            mock_ctx = MockContext(interaction)

            await interaction.response.send_message(
                "🎯 **Hangman startet!**\n"
                "Sammle Teilnehmer und errate Drachenlord-Wörter!\n"
                "Das Spiel wird in einem separaten Thread gespielt um Spam zu vermeiden."
            )

            # Starte Hangman (die Funktion macht jetzt alle checks selbst)
            await start_hangman(mock_ctx)

        except Exception as e:
            print(f"Fehler in hangman command: {e}")
            await interaction.response.send_message("❌ Hangman konnte nicht gestartet werden!", ephemeral=True)

    # Hangman Ranking Slash Command
    @bot.tree.command(name="hangman_ranking", description="🏆 Zeigt die Hangman-Bestenliste")
    async def hangman_ranking_slash(interaction: discord.Interaction):
        """Hangman Ranking Slash Command - Zeigt die Bestenliste"""
        try:
            # Erstelle Ranking-Embed
            embed = await show_hangman_rankings(bot, interaction.user)

            # Sende als ephemeral (nur für den User sichtbar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(f"Error in hangman_ranking command: {e}")
            await interaction.response.send_message("❌ Rankings konnten nicht geladen werden!", ephemeral=True)

    # Cleanup-Task für inaktive Spiele
    @tasks.loop(minutes=5)
    async def cleanup_task():
        await cleanup_inactive_games()

    # Starte Cleanup-Task
    cleanup_task.start()
    print("Hangman-System mit Slash Commands initialisiert")

def setup(bot):
    register_hangman_commands(bot)
