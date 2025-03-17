import discord
from discord.ext import commands
from discord import Status
import datetime
import uuid
import servercounter
import math
import asyncio
import json
import os
import re

class StatsManager:
    def __init__(self):
        self.stats_file = '/app/data/stats.json'
        self.stats = {
            'unique_users': set(),
            'commands_used': 0,
            'sounds_played': 0
        }
        self._load_stats()
    
    def _load_stats(self):
        """Lädt die Statistiken aus der Datei, falls vorhanden"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    data = json.load(f)
                    # Sets können nicht direkt als JSON gespeichert werden
                    # daher werden sie als Liste gespeichert und hier zurück konvertiert
                    self.stats['unique_users'] = set(data.get('unique_users', []))
                    self.stats['commands_used'] = data.get('commands_used', 0)
                    self.stats['sounds_played'] = data.get('sounds_played', 0)
        except Exception as e:
            print(f"Fehler beim Laden der Statistiken: {e}")
    
    def _save_stats(self):
        """Speichert die Statistiken in einer Datei"""
        try:
            os.makedirs(os.path.dirname(self.stats_file), exist_ok=True)
            
            # Sets können nicht direkt als JSON gespeichert werden,
            # daher konvertieren wir sie in eine Liste
            save_data = {
                'unique_users': list(self.stats['unique_users']),
                'commands_used': self.stats['commands_used'],
                'sounds_played': self.stats['sounds_played']
            }
            
            with open(self.stats_file, 'w') as f:
                json.dump(save_data, f)
        except Exception as e:
            print(f"Fehler beim Speichern der Statistiken: {e}")

def register_admin_commands(bot):
    admin_user_id = bot.admin_user_id
    logging_channel = bot.logging_channel
    message_history = bot.message_history

    async def _log(message):
        """Helper function for logging"""
        channel = bot.get_channel(logging_channel)
        await channel.send("```\n" + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S # ") + str(message) + "```\n")

    @bot.command(pass_context=True)
    async def user(ctx, page: int = 1):
        """Zeigt Nutzerstatistiken und Server-Informationen an"""
        if ctx.author.id != admin_user_id:
            await ctx.send("Du bist nicht berechtigt, diesen Befehl zu nutzen!")
            return
        
        # Auf 15 Server pro Seite erhöhen
        servers_per_page = 15
        guilds = list(bot.guilds)
        total_pages = math.ceil(len(guilds) / servers_per_page)
        
        if page < 1 or page > total_pages:
            await ctx.send(f"❌ Ungültige Seite! Es gibt insgesamt {total_pages} Seiten.")
            return
        
        # Gesamte Nutzerzahlen berechnen
        total_users = 0
        online_users = 0
        for guild in bot.guilds:
            guild_total = guild.member_count
            guild_online = len([m for m in guild.members if m.status != Status.offline and not m.bot])
            total_users += guild_total
            online_users += guild_online
        
        # Funktion zum Erstellen der kombinierten Statistik für eine bestimmte Seite
        def create_page(current_page):
            start_idx = (current_page - 1) * servers_per_page
            end_idx = min(start_idx + servers_per_page, len(guilds))
            
            # Server-Namen mit Regex bereinigen
            server_stats = []
            
            for guild in guilds[start_idx:end_idx]:
                # Bereinigung des Server-Namens mit Regex
                clean_name = re.sub(r'<a?:[a-zA-Z0-9_]+:[0-9]+>', '', guild.name)  # Entfernt Discord Emojis
                clean_name = re.sub(r'[^\w\s\-\.]', '', clean_name).strip()  # Entfernt Sonderzeichen
                
                guild_total = guild.member_count
                guild_online = len([m for m in guild.members if m.status != Status.offline and not m.bot])
                
                # Berechne Prozentsatz der Online-Nutzer
                online_percent = round((guild_online / guild_total * 100), 1) if guild_total > 0 else 0
                
                server_stats.append((clean_name, guild_total, guild_online, online_percent))
            
            # Definiere feste Spaltenbreiten
            name_width = 18  # Name-Spaltenbreite 
            num_width = 9    # Zahlenspaltenbreite
            
            # Erstelle eine kompaktere Tabelle mit konsistenten Breiten
            header_line = f"Bot ist auf {len(guilds)} Servern aktiv | "
            header_line += f"Gesamt: {total_users} Nutzer ({online_users} online)"
            page_line = f"Seite {current_page}/{total_pages}"
            
            # Formatierung mit Tabellenlayout
            stats_message = [
                "┌" + "─" * (name_width + 2 + num_width*3 + 6) + "┐",
                "│ " + header_line.ljust(name_width + 2 + num_width*3 + 4) + " │",
                "├" + "─" * (name_width + 2 + num_width*3 + 6) + "┤",
                "│ " + page_line.ljust(name_width + 2 + num_width*3 + 4) + " │",
                "├" + "─" * name_width + "┬" + "─" * num_width + "┬" + "─" * num_width + "┬" + "─" * num_width + "┤",
                "│" + "SERVER".center(name_width) + "│" + "NUTZER".center(num_width) + "│" + "ONLINE".center(num_width) + "│" + "PROZENT".center(num_width) + "│",
                "├" + "─" * name_width + "┼" + "─" * num_width + "┼" + "─" * num_width + "┼" + "─" * num_width + "┤"
            ]
            
            # Nutzerstatistiken als Tabelle mit festen Breiten
            for name, total, online, percent in server_stats:
                # Kürzen des Namens wenn nötig
                display_name = name[:name_width-3] + "..." if len(name) > name_width else name
                
                # Alle Spalten mit exakter Breite formatieren
                server_col = display_name.ljust(name_width)
                users_col = str(total).ljust(num_width)
                online_col = str(online).ljust(num_width)
                percent_col = f"{percent} %".ljust(num_width)
                
                stats_message.append(f"│{server_col}│{users_col}│{online_col}│{percent_col}│")
            
            stats_message.append("└" + "─" * name_width + "┴" + "─" * num_width + "┴" + "─" * num_width + "┴" + "─" * num_width + "┘")
            
            return "```\n" + "\n".join(stats_message) + "\n```"
        
        # Erste Seite senden
        message = await ctx.send(create_page(page))
        
        # Nur Reaktionen hinzufügen, wenn es mehr als eine Seite gibt
        if total_pages > 1:
            await message.add_reaction("⬅️")
            await message.add_reaction("➡️")
            
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"] and reaction.message.id == message.id
            
            current_page = page
            
            # Auf Reaktionen warten und Seiten ändern
            while True:
                try:
                    reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
                    
                    if str(reaction.emoji) == "➡️" and current_page < total_pages:
                        current_page += 1
                    elif str(reaction.emoji) == "⬅️" and current_page > 1:
                        current_page -= 1
                    
                    await message.edit(content=create_page(current_page))
                    await message.remove_reaction(reaction, user)
                    
                except asyncio.TimeoutError:
                    break
        
        else:
            if logging_channel:
                await _log(f"Admin-Befehl !user wurde von {ctx.author.name} ausgeführt (Seite {page}/{total_pages})")

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def ping(ctx):
        """Zeigt die Bot-Latenz an"""
        latency = round(bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Bot Latenz: {latency}ms")

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def servercount(ctx):
        """Führt ein manuelles Servercounter-Update durch"""
        await ctx.send("🔄 Starte manuelles Servercounter Update...")
        success = await servercounter.single_update(bot)
        if not success:
            await ctx.send("❌ Servercounter Update fehlgeschlagen! Überprüfe die Logs.")

    @bot.command(name='kontakt')
    async def contact(ctx, *, message=None):
        """Sendet eine Nachricht an den Bot-Administrator"""
        if not message:
            await ctx.send("Bitte gib eine Nachricht an! Beispiel: `!kontakt Hallo, ich habe eine Frage`")
            return

        admin_user = await bot.fetch_user(admin_user_id)
        if not admin_user:
            await ctx.send("❌ Fehler: Admin konnte nicht gefunden werden!")
            return

        message_id = str(uuid.uuid4())[:8]
        message_history[message_id] = ctx.author.id

        embed = discord.Embed(
            title="📨 Neue Nachricht",
            description=message,
            color=0x3498db,
            timestamp=datetime.datetime.now(datetime.UTC)
        )
        embed.add_field(name="Absender", value=f"{ctx.author} (ID: {ctx.author.id})")
        embed.add_field(name="Server", value=ctx.guild.name if ctx.guild else "DM")
        embed.add_field(name="Nachrichten-ID", value=message_id, inline=False)
        embed.set_footer(text=f"Antworte mit: !antwort {message_id} <deine Antwort>")

        try:
            await admin_user.send(embed=embed)
            await ctx.send("✅ Deine Nachricht wurde erfolgreich an den Administrator gesendet!")
            if logging_channel:
                await _log(f"Kontaktnachricht von {ctx.author} (ID: {message_id})")
        except:
            await ctx.send("❌ Fehler beim Senden der Nachricht!")

    @bot.command(name='antwort')
    async def reply(ctx, message_id=None, *, response=None):
        """Ermöglicht dem Admin, auf Kontaktnachrichten zu antworten"""
        if ctx.author.id != admin_user_id:
            await ctx.send("❌ Nur der Administrator kann diesen Befehl nutzen!")
            return

        if not message_id or not response:
            await ctx.send("❌ Syntax: `!antwort <message_id> <deine Antwort>`")
            return

        if message_id not in message_history:
            await ctx.send("❌ Diese Nachrichten-ID existiert nicht!")
            return

        user_id = message_history[message_id]
        try:
            user = await bot.fetch_user(user_id)
            embed = discord.Embed(
                title="📩 Antwort vom Administrator",
                description=response,
                color=0x2ecc71,
                timestamp=datetime.datetime.now(datetime.UTC)
            )
            embed.add_field(name="Bezugnehmend auf ID", value=message_id)
            
            await user.send(embed=embed)
            await ctx.send("✅ Antwort wurde erfolgreich gesendet!")
            if logging_channel:
                await _log(f"Admin-Antwort an User {user.id} (ID: {message_id})")
        except:
            await ctx.send("❌ Fehler beim Senden der Antwort!")

def setup(bot):
    register_admin_commands(bot)
