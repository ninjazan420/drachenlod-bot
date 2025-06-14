import discord
from discord.ext import commands
import datetime
import uuid
import psutil
import platform
import sys
import os
import servercounter
from .stats_manager import StatsManager
from .ban_manager import BanManager
from .server_list_view import ServerListView

# Globale Variablen für Nachrichten-History
message_history = {}

def register_admin_commands(bot):
    """Registriert alle Admin-Befehle"""
    
    # Initialisiere Manager
    bot.stats_manager = StatsManager()
    bot.ban_manager = BanManager("data/ban.json")
    
    # Admin-Konfiguration aus Environment Variables
    admin_user_id = int(os.getenv('ADMIN_USER_ID'))
    logging_channel = int(os.getenv('LOGGING_CHANNEL'))
    
    async def _log(message):
        """Hilfsfunktion für Logging"""
        channel = bot.get_channel(logging_channel)
        if channel:
            await channel.send(f"```\n{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} # {message}```")

    # ping befehl entfernt - nur !lord bleibt bestehen

    # servercount befehl entfernt - nur !lord bleibt bestehen

    @bot.command(name='drache')
    async def drache(ctx, action=None, server_id=None, *args):
        """Hauptbefehl für Admin-Funktionen"""
        
        # PING-Befehl (für alle Nutzer zugänglich)
        if action and action.lower() == 'ping':
            latency = round(bot.latency * 1000)
            await ctx.send(f"🏓 Pong! Latenz: {latency}ms")
            
            if logging_channel:
                await _log(f"Ping-Befehl von {ctx.author.name}: {latency}ms")
            return
        
        # SERVERCOUNT-Befehl (nur für Admin)
        elif action and action.lower() == 'servercount':
            if ctx.author.id != admin_user_id:
                return
            
            await ctx.send("🔄 Starte manuelles Servercounter Update...")
            success = await servercounter.single_update(bot)
            if not success:
                await ctx.send("❌ Servercounter Update fehlgeschlagen! Überprüfe die Logs.")
            return
        
        # ANTWORT-Befehl (nur für Admin)
        elif action and action.lower() == 'antwort':
            if ctx.author.id != admin_user_id:
                return
            
            if not server_id or not args:
                await ctx.send("❌ Syntax: `!drache antwort <message_id> <deine Antwort>`")
                return
            
            try:
                message_id = int(server_id)
                antwort_text = ' '.join(args)
                
                if message_id not in message_history:
                    await ctx.send(f"❌ Nachricht mit ID `{message_id}` nicht gefunden!")
                    return
                
                original_message = message_history[message_id]
                user_id = original_message['user_id']
                
                try:
                    user = await bot.fetch_user(user_id)
                    
                    embed = discord.Embed(
                        title="📬 Antwort vom Bot-Administrator",
                        description=antwort_text,
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
                    await ctx.send(f"✅ Antwort an {user.display_name} gesendet!")
                    
                    if logging_channel:
                        await _log(f"Admin hat auf Nachricht {message_id} von {user.display_name} geantwortet: {antwort_text[:100]}...")
                        
                except discord.Forbidden:
                    await ctx.send(f"❌ Kann keine DM an den User senden (DMs deaktiviert oder Bot blockiert)")
                except discord.NotFound:
                    await ctx.send(f"❌ User nicht gefunden!")
                except Exception as e:
                    await ctx.send(f"❌ Fehler beim Senden der Antwort: {str(e)}")
                    
            except ValueError:
                await ctx.send("❌ Ungültige Message-ID! Muss eine Zahl sein.")
            return
        
        # PRIVACY-Befehl (für alle Nutzer zugänglich)
        elif action and action.lower() == 'privacy':
            embed = discord.Embed(
                title="🔐 Datenschutzerklärung",
                description="Informationen zum Datenschutz und zur Datenverarbeitung des Buttergolem Bots",
                color=0x3498db
            )
            
            embed.add_field(
                name="📋 Erhobene Daten",
                value="• **Message Content:** Temporäre Verarbeitung für Befehle, Quiz, KI-Chat und Sound-Features\n"
                      "• **Server Members:** Mitgliederzahlen für Statistiken und Gaming-Features\n"
                      "• **User IDs:** Für Befehlsverarbeitung und Session-Management",
                inline=False
            )
            
            embed.add_field(
                name="🛡️ Datenschutz-Garantien",
                value="• **Keine Weitergabe an Dritte**\n"
                      "• **Keine Nutzung für KI-Training**\n"
                      "• **Keine kommerzielle Verwertung**\n"
                      "• **Automatische Löschung** bei Bot-Entfernung",
                inline=False
            )
            
            embed.add_field(
                name="📄 Vollständige Datenschutzerklärung",
                value="[Hier findest du die vollständige Datenschutzerklärung](https://github.com/ninjazan420/drachenlod-bot/blob/master/privacy_policy.md)\n\n"
                      "Bei Fragen zur Datenverarbeitung wende dich an: **drache@f0ck.org**",
                inline=False
            )
            
            embed.set_footer(text="Durch die Nutzung des Bots stimmst du der Datenschutzerklärung zu.")
            await ctx.send(embed=embed)
            
            if logging_channel:
                await _log(f"Datenschutzerklärung wurde von {ctx.author.name} abgerufen")
            return
        
        # Admin-Check für alle anderen Befehle
        if ctx.author.id != admin_user_id:
            await ctx.send("❌ Nur der Administrator kann diesen Befehl nutzen!")
            return

        if not action:
            help_text = (
                "**🐉 Admin-Befehle**\n\n"
                "• `!drache stats` - Bot-Statistiken anzeigen\n"
                "• `!drache server [seite]` - Server-Liste anzeigen\n"
                "• `!drache leave <server_id> [message_id] [grund...]` - Server verlassen (und optional bannen)\n"
                "• `!drache ban <server|user> <id> [grund...]` - Server oder User bannen\n"
                "• `!drache unban <server|user> <ban_id>` - Ban aufheben\n"
                "• `!drache bans <server|user>` - Aktive Bans anzeigen\n"
                "• `!drache kontakt <nachricht>` - Kontakt-System\n"
                 "• `!drache privacy` - Datenschutzerklärung anzeigen (für alle Nutzer)\n"
                 "• `!drache hilfe` - Zeigt die Bot-Hilfe an (für alle Nutzer)\n"
                 "• `!drache lord` - Spielt einen zufälligen Sound ab (für alle Nutzer)\n"
                 "• `!drache butteriq <disable|enable> <user_id>` - ButterIQ verwalten\n"
            )
            await ctx.send(help_text)
            return

        # STATS-Befehl
        if action.lower() == 'stats':
            # System-Informationen
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Bot-Informationen
            guild_count = len(bot.guilds)
            user_count = sum(guild.member_count or 0 for guild in bot.guilds)
            
            # Uptime berechnen
            if hasattr(bot, 'start_time'):
                uptime = datetime.datetime.now() - bot.start_time
                uptime_str = str(uptime).split('.')[0]  # Entferne Mikrosekunden
            else:
                uptime_str = "Unbekannt"
            
            # Statistiken vom StatsManager
            stats = bot.stats_manager.get_stats()
            
            # Zufälliges Zitat laden
            import os
            import json
            quote = "Meddl Leude!"
            try:
                quotes_paths = [
                    os.path.join(os.path.dirname(__file__), '..', 'data', 'quotes.json'),
                    'src/data/quotes.json',
                    'data/quotes.json'
                ]
                
                for quotes_path in quotes_paths:
                    if os.path.exists(quotes_path):
                        with open(quotes_path, 'r', encoding='utf-8') as f:
                            quotes = json.load(f)
                            if quotes:
                                quote = random.choice(quotes)
                        break
            except Exception:
                pass
            
            embed = discord.Embed(
                title="📊 ButterGolem Bot Statistiken",
                description=f"*\"{quote}\"*",
                color=0x3498db
            )
            
            # Bot-Informationen
            embed.add_field(
                name="🤖 Bot-Info",
                value=(
                    f"**Uptime:** {uptime_str}\n"
                    f"**Server:** {guild_count}\n"
                    f"**Benutzer:** {user_count:,}\n"
                    f"**Latenz:** {round(bot.latency * 1000)}ms"
                ),
                inline=True
            )
            
            # System-Informationen
            embed.add_field(
                name="💻 System",
                value=(
                    f"**OS:** {platform.system()} {platform.release()}\n"
                    f"**Python:** {sys.version.split()[0]}\n"
                    f"**Discord.py:** {discord.__version__}\n"
                    f"**CPU:** {cpu_percent}%"
                ),
                inline=True
            )
            
            # Speicher-Informationen
            embed.add_field(
                name="🧠 Speicher",
                value=(
                    f"**RAM:** {memory.percent}% ({memory.used // 1024 // 1024:,} MB / {memory.total // 1024 // 1024:,} MB)\n"
                    f"**Disk:** {disk.percent}% ({disk.used // 1024 // 1024 // 1024:,} GB / {disk.total // 1024 // 1024 // 1024:,} GB)"
                ),
                inline=True
            )
            
            # Bot-Statistiken
            embed.add_field(
                name="📈 Bot-Statistiken",
                value=(
                    f"**Befehle ausgeführt:** {stats.get('commands_executed', 0):,}\n"
                    f"**Server beigetreten:** {stats.get('servers_joined', 0):,}\n"
                    f"**Server verlassen:** {stats.get('servers_left', 0):,}\n"
                    f"**Nachrichten verarbeitet:** {stats.get('messages_processed', 0):,}"
                ),
                inline=True
            )
            
            embed.set_footer(text="ButterGolem Bot • Neofetch-Style Stats")
            await ctx.send(embed=embed)
            
            if logging_channel:
                await _log(f"Admin-Befehl !drache stats wurde von {ctx.author.name} ausgeführt")

        # KONTAKT-Befehl
        elif action.lower() == 'kontakt':
            # Extrahiere die Nachricht aus den verbleibenden Argumenten
            if not server_id and not args:
                await ctx.send("❌ Syntax: `!drache kontakt <deine Nachricht>`")
                return

            # Kombiniere server_id und args zur vollständigen Nachricht
            message_parts = []
            if server_id:
                message_parts.append(server_id)
            if args:
                message_parts.extend(args)
            
            message = " ".join(message_parts)
            
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



        # LEAVE-Befehl
        elif action.lower() == 'leave':
            if not server_id:
                await ctx.send("❌ Syntax: `!drache leave <server_id> [message_id] [grund...]`")
                return

            try:
                # Prüfen, ob es sich um eine fortlaufende ID oder eine Discord-ID handelt
                if server_id.isdigit():
                    seq_id = int(server_id)
                    # Wenn es eine fortlaufende ID ist, hole die Discord-ID aus dem Dictionary
                    if seq_id in bot.server_id_map:
                        discord_id = bot.server_id_map[seq_id]
                    else:
                        # Wenn die fortlaufende ID nicht existiert, versuche sie als Discord-ID zu verwenden
                        discord_id = int(server_id)
                else:
                    await ctx.send("❌ Ungültige Server-ID! Bitte gib eine gültige Zahl ein.")
                    return

                # Versuche, den Server zu finden und zu verlassen
                guild = bot.get_guild(discord_id)
                if guild:
                    # Prüfe, ob zusätzliche Argumente für Ban vorhanden sind
                    message_id = None
                    reason = None

                    if args:
                        # Wenn das erste Argument eine Zahl ist, behandle es als message_id
                        if args[0].isdigit():
                            message_id = args[0]
                            # Der Rest ist der Grund
                            if len(args) > 1:
                                reason = " ".join(args[1:])
                        else:
                            # Wenn das erste Argument keine Zahl ist, ist alles der Grund
                            reason = " ".join(args)

                    # Server verlassen
                    await ctx.send(f"🚪 Verlasse Server: {guild.name} (ID: {guild.id})...")
                    await guild.leave()

                    # Wenn Grund oder Message-ID angegeben wurde, Server bannen
                    ban_id = None
                    if reason or message_id:
                        ban_id = bot.ban_manager.add_ban(
                            server_id=guild.id,
                            server_name=guild.name,
                            reason=reason,
                            message_id=message_id
                        )
                        await ctx.send(f"🚫 Server wurde gebannt! Ban-ID: `{ban_id}`")
                        if logging_channel:
                            await _log(f"Admin hat den Server {guild.name} (ID: {guild.id}) verlassen und gebannt. Ban-ID: {ban_id}, Grund: {reason}")
                    else:
                        await ctx.send(f"✅ Server erfolgreich verlassen!")
                        if logging_channel:
                            await _log(f"Admin hat den Server {guild.name} (ID: {guild.id}) verlassen")
                else:
                    await ctx.send(f"❌ Server mit ID {server_id} nicht gefunden!")
            except Exception as e:
                await ctx.send(f"❌ Fehler beim Verlassen des Servers: {str(e)}")

        # BAN-Befehl
        elif action.lower() == 'ban':
            if not server_id or server_id.lower() not in ['server', 'user']:
                await ctx.send("❌ Syntax: `!drache ban <server|user> <id> [grund...]`")
                return

            ban_type = server_id.lower()

            # Prüfen, ob genügend Argumente vorhanden sind
            if len(args) < 1:
                await ctx.send(f"❌ Syntax: `!drache ban {ban_type} <id> [grund...]`")
                return

            target_id = args[0]

            # BAN SERVER
            if ban_type == 'server':
                try:
                    # Versuche, die ID als Zahl zu interpretieren
                    if target_id.isdigit():
                        seq_id = int(target_id)
                        # Wenn es eine fortlaufende ID ist, hole die Discord-ID aus dem Dictionary
                        if seq_id in bot.server_id_map:
                            discord_id = bot.server_id_map[seq_id]
                        else:
                            # Wenn die fortlaufende ID nicht existiert, versuche sie als Discord-ID zu verwenden
                            discord_id = int(target_id)
                    else:
                        await ctx.send("❌ Ungültige Server-ID! Bitte gib eine gültige Zahl ein.")
                        return

                    # Versuche, den Server zu finden
                    guild = bot.get_guild(discord_id)
                    if guild:
                        # Grund extrahieren
                        reason = " ".join(args[1:]) if len(args) > 1 else None

                        # Server bannen
                        ban_id = bot.ban_manager.add_ban(
                            server_id=guild.id,
                            server_name=guild.name,
                            reason=reason
                        )

                        await ctx.send(f"🚫 Server `{guild.name}` (ID: {guild.id}) wurde gebannt! Ban-ID: `{ban_id}`")
                        if logging_channel:
                            await _log(f"Admin hat den Server {guild.name} (ID: {guild.id}) gebannt. Ban-ID: {ban_id}, Grund: {reason}")
                    else:
                        await ctx.send(f"❌ Server mit ID {target_id} nicht gefunden!")
                except Exception as e:
                    await ctx.send(f"❌ Fehler beim Bannen des Servers: {str(e)}")

            # BAN USER
            elif ban_type == 'user':
                try:
                    # Prüfe, ob die User-ID eine gültige Zahl ist
                    if not target_id.isdigit():
                        await ctx.send("❌ Ungültige User-ID! Bitte gib eine gültige Zahl ein.")
                        return

                    user_id = int(target_id)

                    # Versuche, den User zu finden
                    try:
                        user = await bot.fetch_user(user_id)
                        username = f"{user.name}#{user.discriminator}" if hasattr(user, 'discriminator') else user.name
                    except:
                        # Wenn der User nicht gefunden werden kann, verwenden wir die ID als Namen
                        user = None
                        username = f"Unbekannter User ({user_id})"

                    # Prüfe, ob ein Server-ID angegeben wurde
                    server_id = None
                    server_name = None
                    reason_start_idx = 1

                    # Wenn das zweite Argument eine Zahl ist, behandle es als Server-ID
                    if len(args) > 1 and args[1].isdigit():
                        server_id = int(args[1])
                        reason_start_idx = 2

                        # Versuche, den Server zu finden
                        guild = bot.get_guild(server_id)
                        if guild:
                            server_name = guild.name
                        else:
                            server_name = f"Unbekannter Server ({server_id})"

                    # Grund extrahieren
                    reason = " ".join(args[reason_start_idx:]) if len(args) > reason_start_idx else None

                    # User bannen
                    ban_id = bot.ban_manager.add_user_ban(
                        user_id=user_id,
                        username=username,
                        server_id=server_id,
                        server_name=server_name,
                        reason=reason
                    )

                    # Erfolgsbenachrichtigung
                    if server_id:
                        await ctx.send(f"🚫 User `{username}` (ID: {user_id}) wurde auf Server `{server_name}` gebannt! Ban-ID: `{ban_id}`")
                        if logging_channel:
                            await _log(f"Admin hat den User {username} (ID: {user_id}) auf Server {server_name} gebannt. Ban-ID: {ban_id}, Grund: {reason}")
                    else:
                        await ctx.send(f"🚫 User `{username}` (ID: {user_id}) wurde global gebannt! Ban-ID: `{ban_id}`")
                        if logging_channel:
                            await _log(f"Admin hat den User {username} (ID: {user_id}) global gebannt. Ban-ID: {ban_id}, Grund: {reason}")
                except Exception as e:
                    await ctx.send(f"❌ Fehler beim Bannen des Users: {str(e)}")

        # UNBAN-Befehl
        elif action.lower() == 'unban':
            if not server_id or server_id.lower() not in ['server', 'user']:
                await ctx.send("❌ Syntax: `!drache unban <server|user> <ban_id>`")
                return

            ban_type = server_id.lower()

            # Prüfen, ob genügend Argumente vorhanden sind
            if len(args) < 1:
                await ctx.send(f"❌ Syntax: `!drache unban {ban_type} <ban_id>`")
                return

            ban_id = args[0]

            # UNBAN SERVER
            if ban_type == 'server':
                ban = bot.ban_manager.get_ban_by_id(ban_id)

                if not ban:
                    await ctx.send(f"❌ Server-Ban mit ID `{ban_id}` nicht gefunden!")
                    return

                if not ban["active"]:
                    await ctx.send(f"❌ Server-Ban mit ID `{ban_id}` ist bereits aufgehoben!")
                    return

                success = bot.ban_manager.remove_ban(ban_id)
                if success:
                    await ctx.send(f"✅ Ban für Server `{ban['server_name']}` (ID: {ban['server_id']}) wurde aufgehoben!")
                    if logging_channel:
                        await _log(f"Admin hat den Ban für Server {ban['server_name']} (ID: {ban['server_id']}) aufgehoben. Ban-ID: {ban_id}")
                else:
                    await ctx.send(f"❌ Fehler beim Aufheben des Server-Bans!")

            # UNBAN USER
            elif ban_type == 'user':
                ban = bot.ban_manager.get_user_ban_by_id(ban_id)

                if not ban:
                    await ctx.send(f"❌ User-Ban mit ID `{ban_id}` nicht gefunden!")
                    return

                if not ban["active"]:
                    await ctx.send(f"❌ User-Ban mit ID `{ban_id}` ist bereits aufgehoben!")
                    return

                success = bot.ban_manager.remove_user_ban(ban_id)
                if success:
                    if ban["server_id"]:
                        await ctx.send(f"✅ Ban für User `{ban['username']}` (ID: {ban['user_id']}) auf Server `{ban['server_name']}` wurde aufgehoben!")
                        if logging_channel:
                            await _log(f"Admin hat den Ban für User {ban['username']} (ID: {ban['user_id']}) auf Server {ban['server_name']} aufgehoben. Ban-ID: {ban_id}")
                    else:
                        await ctx.send(f"✅ Globaler Ban für User `{ban['username']}` (ID: {ban['user_id']}) wurde aufgehoben!")
                        if logging_channel:
                            await _log(f"Admin hat den globalen Ban für User {ban['username']} (ID: {ban['user_id']}) aufgehoben. Ban-ID: {ban_id}")
                else:
                    await ctx.send(f"❌ Fehler beim Aufheben des User-Bans!")

        # SERVER-Befehl
        elif action.lower() == 'server':
            # Seite aus server_id Parameter extrahieren, falls vorhanden
            page = 1
            if server_id and server_id.isdigit():
                page = int(server_id)

            # Server-Liste abrufen und sortieren
            guilds = list(bot.guilds)

            # View erstellen
            view = ServerListView(ctx, guilds, admin_user_id, logging_channel, bot.server_id_map)

            # Setze die aktuelle Seite, falls angegeben
            if page > 0 and page <= view.total_pages:
                view.current_page = page

            # Sende das Embed mit der View
            message = await ctx.send(embed=view.create_embed(), view=view)

            # Speichere die Nachricht in der View für spätere Aktualisierungen
            view.message = message

            if logging_channel:
                await _log(f"Admin-Befehl !drache server wurde von {ctx.author.name} ausgeführt")

            return

        # BANS-Befehl
        elif action.lower() == 'bans':
            if not server_id or server_id.lower() not in ['server', 'user']:
                await ctx.send("❌ Syntax: `!drache bans <server|user>`")
                return

            ban_type = server_id.lower()

            # BANS SERVER
            if ban_type == 'server':
                bans = bot.ban_manager.get_all_bans()

                if not bans:
                    await ctx.send("ℹ️ Es sind keine aktiven Server-Bans vorhanden.")
                    return

                # Erstelle ein Embed mit den Ban-Informationen
                embed = discord.Embed(
                    title="🚫 Gebannte Server",
                    description=f"Anzahl aktiver Bans: {len(bans)}",
                    color=0xe74c3c,
                    timestamp=discord.utils.utcnow()
                )

                for ban in bans:
                    # Erstelle einen lesbaren Eintrag für jeden Ban
                    value = (
                        f"**Server:** {ban['server_name']}\n"
                        f"**Server-ID:** {ban['server_id']}\n"
                        f"**Grund:** {ban['reason']}\n"
                        f"**Datum:** {ban['timestamp']}\n"
                    )

                    if ban['message_id']:
                        value += f"**Nachricht-ID:** {ban['message_id']}\n"

                    embed.add_field(
                        name=f"Ban-ID: {ban['ban_id']}",
                        value=value,
                        inline=False
                    )

                embed.set_footer(text="Nutze !drache unban server <ban_id> zum Aufheben eines Bans")
                await ctx.send(embed=embed)

            # BANS USER
            elif ban_type == 'user':
                bans = bot.ban_manager.get_all_user_bans()

                if not bans:
                    await ctx.send("ℹ️ Es sind keine aktiven User-Bans vorhanden.")
                    return

                # Erstelle ein Embed mit den Ban-Informationen
                embed = discord.Embed(
                    title="🚫 Gebannte User",
                    description=f"Anzahl aktiver Bans: {len(bans)}",
                    color=0xe74c3c,
                    timestamp=discord.utils.utcnow()
                )

                for ban in bans:
                    # Erstelle einen lesbaren Eintrag für jeden Ban
                    value = (
                        f"**User:** {ban['username']}\n"
                        f"**User-ID:** {ban['user_id']}\n"
                    )

                    if ban['server_id']:
                        value += f"**Server:** {ban['server_name']}\n"
                        value += f"**Server-ID:** {ban['server_id']}\n"
                    else:
                        value += f"**Geltungsbereich:** Global\n"

                    value += f"**Grund:** {ban['reason']}\n"
                    value += f"**Datum:** {ban['timestamp']}\n"

                    embed.add_field(
                        name=f"Ban-ID: {ban['ban_id']}",
                        value=value,
                        inline=False
                    )

                embed.set_footer(text="Nutze !drache unban user <ban_id> zum Aufheben eines Bans")
                await ctx.send(embed=embed)

        # BUTTERIQ-Befehl
        elif action.lower() == 'butteriq':
            if not server_id:
                help_text = (
                    "**⚙️ ButterIQ Admin-Befehle**\n\n"
                    "• `!drache butteriq disable <user_id>` - Sperrt eine Benutzer-ID für ButterIQ\n"
                    "• `!drache butteriq enable <user_id>` - Gibt eine Benutzer-ID für ButterIQ frei\n"
                )
                await ctx.send(help_text)
                return
            
            butteriq_action = server_id.lower()
            
            if not args:
                await ctx.send("❌ Syntax: `!drache butteriq <disable|enable> <user_id>`")
                return
            
            user_id_str = args[0]
            
            # Versuche, die Benutzer-ID zu konvertieren
            try:
                user_id = int(user_id_str)
            except ValueError:
                await ctx.send("❌ Ungültige Benutzer-ID! Bitte gib eine gültige ID an.")
                return

            if butteriq_action == 'disable':
                # Benutzer-ID sperren
                bot.butteriq_manager.disable_user(user_id)
                await ctx.send(f"✅ Benutzer-ID {user_id} wurde für ButterIQ gesperrt.")
                if logging_channel:
                    await _log(f"Admin hat Benutzer-ID {user_id} für ButterIQ gesperrt")
            elif butteriq_action == 'enable':
                # Benutzer-ID freigeben
                if bot.butteriq_manager.enable_user(user_id):
                    await ctx.send(f"✅ Benutzer-ID {user_id} wurde für ButterIQ freigegeben.")
                    if logging_channel:
                        await _log(f"Admin hat Benutzer-ID {user_id} für ButterIQ freigegeben")
                else:
                    await ctx.send(f"❌ Benutzer-ID {user_id} war nicht gesperrt.")
            else:
                await ctx.send("❌ Ungültige Aktion! Verfügbare Aktionen: `disable`, `enable`")

        # HILFE-Befehl (für alle Nutzer zugänglich)
        elif action and action.lower() == 'hilfe':
            from hilfe import create_help_embed
            is_server_admin = ctx.author.guild_permissions.administrator if ctx.guild else False
            embed = await create_help_embed(ctx.author.id, is_server_admin, admin_user_id)
            await ctx.send(embed=embed)
            return
        
        # LORD-Befehl (für alle Nutzer zugänglich)
        elif action.lower() == 'lord':
            if not ctx.author.voice:
                await ctx.send('Das funktioniert nur in Voice-Channels du scheiß HAIDER')
                return

            voice_channel = ctx.author.voice.channel
            # Import der Sound-Funktionen
            from sounds import playsound, get_random_clipname
            await playsound(voice_channel, get_random_clipname(), bot)
            return

        else:
            available_actions = "server, leave, ban, unban, bans, hilfe, lord"
            if ctx.author.id == admin_user_id:
                available_actions += ", antwort, servercount, butteriq"
            
            await ctx.send(f"❌ Unbekannte Aktion! Verfügbare Aktionen: {available_actions}")

    # antwort befehl entfernt - nur !lord bleibt bestehen