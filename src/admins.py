import discord
from discord.ext import commands
from discord import Status
import datetime
import uuid
import servercounter
import math
import asyncio

def register_admin_commands(bot):
    admin_user_id = bot.admin_user_id
    logging_channel = bot.logging_channel
    message_history = bot.message_history

    async def _log(message):
        """Helper function for logging"""
        channel = bot.get_channel(logging_channel)
        await channel.send("```\n" + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S # ") + str(message) + "```\n")

    @bot.command(pass_context=True)
    async def server(ctx, page: int = 1):
        """Zeigt eine Liste aller Server an"""
        if ctx.author.id != admin_user_id:
            await ctx.send("Du bist nicht berechtigt, diesen Befehl zu nutzen!")
            return
        
        servers_per_page = 15
        guilds = list(bot.guilds)
        total_pages = math.ceil(len(guilds) / servers_per_page)
        
        if page < 1 or page > total_pages:
            await ctx.send(f"❌ Ungültige Seite! Es gibt insgesamt {total_pages} Seiten.")
            return
        
        # Funktion zum Erstellen der Server-Liste für eine bestimmte Seite
        def create_server_page(current_page):
            start_idx = (current_page - 1) * servers_per_page
            end_idx = min(start_idx + servers_per_page, len(guilds))
            
            server_list = "\n".join([f"• {guild.name} (ID: {guild.id})" for guild in guilds[start_idx:end_idx]])
            
            return f"```Der Bot ist auf folgenden Servern aktiv (Seite {current_page}/{total_pages}):\n{server_list}```"
        
        # Erste Seite senden
        message = await ctx.send(create_server_page(page))
        
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
                    
                    await message.edit(content=create_server_page(current_page))
                    await message.remove_reaction(reaction, user)
                    
                    if logging_channel:
                        await _log(f"Admin-Befehl !server Seitenwechsel auf {current_page}/{total_pages} von {ctx.author.name}")
                        
                except asyncio.TimeoutError:
                    break
        
        else:
            if logging_channel:
                await _log(f"Admin-Befehl !server wurde von {ctx.author.name} ausgeführt (Seite {page}/{total_pages})")

    @bot.command(pass_context=True)
    async def user(ctx, page: int = 1):
        """Zeigt Nutzerstatistiken an"""
        if ctx.author.id != admin_user_id:
            await ctx.send("Du bist nicht berechtigt, diesen Befehl zu nutzen!")
            return
        
        servers_per_page = 15
        guilds = list(bot.guilds)
        total_pages = math.ceil(len(guilds) / servers_per_page)
        
        if page < 1 or page > total_pages:
            await ctx.send(f"❌ Ungültige Seite! Es gibt insgesamt {total_pages} Seiten.")
            return
        
        # Gesamte Nutzerzahlen berechnen (bleibt gleich für alle Seiten)
        total_users = 0
        online_users = 0
        for guild in bot.guilds:
            guild_total = guild.member_count
            guild_online = len([m for m in guild.members if m.status != Status.offline and not m.bot])
            total_users += guild_total
            online_users += guild_online
        
        # Funktion zum Erstellen der Nutzerstatistik für eine bestimmte Seite
        def create_user_page(current_page):
            start_idx = (current_page - 1) * servers_per_page
            end_idx = min(start_idx + servers_per_page, len(guilds))
            
            # Nur Server für die aktuelle Seite anzeigen
            server_stats = []
            for guild in guilds[start_idx:end_idx]:
                guild_total = guild.member_count
                guild_online = len([m for m in guild.members if m.status != Status.offline and not m.bot])
                server_stats.append(f"• {guild.name}: {guild_total} Nutzer ({guild_online} online)")
            
            stats_message = [
                "```Nutzerstatistiken:\n",
                f"Gesamt über alle Server: {total_users} Nutzer",
                f"Davon online: {online_users} Nutzer\n",
                f"Details pro Server (Seite {current_page}/{total_pages}):",
                *server_stats,
                "```"
            ]
            
            return "\n".join(stats_message)
        
        # Erste Seite senden
        message = await ctx.send(create_user_page(page))
        
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
                    
                    await message.edit(content=create_user_page(current_page))
                    await message.remove_reaction(reaction, user)
                    
                    if logging_channel:
                        await _log(f"Admin-Befehl !user Seitenwechsel auf {current_page}/{total_pages} von {ctx.author.name}")
                        
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
