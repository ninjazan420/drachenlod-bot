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
from pathlib import Path

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

class BanManager:
    def __init__(self, data_dir='/app/data'):
        self.bans_file = os.path.join(data_dir, 'bans.json')
        self.user_bans_file = os.path.join(data_dir, 'user_bans.json')
        self.bans = []
        self.user_bans = []
        self._load_bans()
        self._load_user_bans()

    def _load_bans(self):
        """Lädt die Server-Bans aus der Datei, falls vorhanden"""
        try:
            if os.path.exists(self.bans_file):
                with open(self.bans_file, 'r', encoding='utf-8') as f:
                    self.bans = json.load(f)
            else:
                # Erstelle die Datei, wenn sie nicht existiert
                self._save_bans()
        except Exception as e:
            print(f"Fehler beim Laden der Server-Bans: {e}")
            self.bans = []

    def _load_user_bans(self):
        """Lädt die User-Bans aus der Datei, falls vorhanden"""
        try:
            if os.path.exists(self.user_bans_file):
                with open(self.user_bans_file, 'r', encoding='utf-8') as f:
                    self.user_bans = json.load(f)
            else:
                # Erstelle die Datei, wenn sie nicht existiert
                self._save_user_bans()
        except Exception as e:
            print(f"Fehler beim Laden der User-Bans: {e}")
            self.user_bans = []

    def _save_bans(self):
        """Speichert die Server-Bans in einer Datei"""
        try:
            # Stelle sicher, dass das Verzeichnis existiert
            os.makedirs(os.path.dirname(self.bans_file), exist_ok=True)
            with open(self.bans_file, 'w', encoding='utf-8') as f:
                json.dump(self.bans, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Fehler beim Speichern der Server-Bans: {e}")

    def _save_user_bans(self):
        """Speichert die User-Bans in einer Datei"""
        try:
            # Stelle sicher, dass das Verzeichnis existiert
            os.makedirs(os.path.dirname(self.user_bans_file), exist_ok=True)
            with open(self.user_bans_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_bans, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Fehler beim Speichern der User-Bans: {e}")

    def add_ban(self, server_id, server_name, reason=None, message_id=None):
        """Fügt einen neuen Server-Ban hinzu"""
        # Generiere eine eindeutige Ban-ID
        ban_id = str(uuid.uuid4())[:8]

        # Erstelle den Ban-Eintrag
        ban_entry = {
            "ban_id": ban_id,
            "server_id": str(server_id),
            "server_name": server_name,
            "reason": reason if reason else "Kein Grund angegeben",
            "message_id": message_id if message_id else None,
            "timestamp": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "active": True
        }

        # Füge den Ban zur Liste hinzu
        self.bans.append(ban_entry)
        self._save_bans()

        return ban_id

    def add_user_ban(self, user_id, username, server_id=None, server_name=None, reason=None):
        """Fügt einen neuen User-Ban hinzu"""
        # Generiere eine eindeutige Ban-ID
        ban_id = str(uuid.uuid4())[:8]

        # Erstelle den Ban-Eintrag
        ban_entry = {
            "ban_id": ban_id,
            "user_id": str(user_id),
            "username": username,
            "server_id": str(server_id) if server_id else None,
            "server_name": server_name if server_name else None,
            "reason": reason if reason else "Kein Grund angegeben",
            "timestamp": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "active": True
        }

        # Füge den Ban zur Liste hinzu
        self.user_bans.append(ban_entry)
        self._save_user_bans()

        return ban_id

    def remove_ban(self, ban_id):
        """Entfernt einen Server-Ban anhand der Ban-ID"""
        for ban in self.bans:
            if ban["ban_id"] == ban_id and ban["active"]:
                ban["active"] = False
                ban["unbanned_at"] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                self._save_bans()
                return True
        return False

    def remove_user_ban(self, ban_id):
        """Entfernt einen User-Ban anhand der Ban-ID"""
        for ban in self.user_bans:
            if ban["ban_id"] == ban_id and ban["active"]:
                ban["active"] = False
                ban["unbanned_at"] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                self._save_user_bans()
                return True
        return False

    def get_all_bans(self, include_inactive=False):
        """Gibt alle Server-Bans zurück"""
        if include_inactive:
            return self.bans
        else:
            return [ban for ban in self.bans if ban["active"]]

    def get_all_user_bans(self, include_inactive=False):
        """Gibt alle User-Bans zurück"""
        if include_inactive:
            return self.user_bans
        else:
            return [ban for ban in self.user_bans if ban["active"]]

    def is_banned(self, server_id):
        """Prüft, ob ein Server gebannt ist"""
        server_id_str = str(server_id)
        for ban in self.bans:
            if ban["server_id"] == server_id_str and ban["active"]:
                return True
        return False

    def is_user_banned(self, user_id, server_id=None):
        """Prüft, ob ein User gebannt ist"""
        user_id_str = str(user_id)
        for ban in self.user_bans:
            if ban["user_id"] == user_id_str and ban["active"]:
                # Wenn server_id angegeben ist, prüfe ob der Ban für diesen Server gilt
                if server_id:
                    # Wenn server_id im Ban None ist, gilt der Ban global
                    if ban["server_id"] is None:
                        return True
                    # Sonst prüfe, ob der Ban für diesen Server gilt
                    elif ban["server_id"] == str(server_id):
                        return True
                else:
                    # Wenn keine server_id angegeben ist, gilt jeder aktive Ban
                    return True
        return False

    def get_ban_by_id(self, ban_id):
        """Gibt einen Server-Ban anhand der Ban-ID zurück"""
        for ban in self.bans:
            if ban["ban_id"] == ban_id:
                return ban
        return None

    def get_user_ban_by_id(self, ban_id):
        """Gibt einen User-Ban anhand der Ban-ID zurück"""
        for ban in self.user_bans:
            if ban["ban_id"] == ban_id:
                return ban
        return None

def register_admin_commands(bot):
    admin_user_id = bot.admin_user_id
    logging_channel = bot.logging_channel
    message_history = bot.message_history
    # Dictionary für fortlaufende Server-IDs
    bot.server_id_map = {}
    # Ban-Manager initialisieren
    bot.ban_manager = BanManager()

    async def _log(message):
        """Helper function for logging"""
        channel = bot.get_channel(logging_channel)
        await channel.send("```\n" + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S # ") + str(message) + "```\n")

    class ServerListView(discord.ui.View):
        def __init__(self, ctx, guilds, admin_user_id, logging_channel, server_id_map, sort_by="name"):
            super().__init__(timeout=180)  # 3 Minuten Timeout
            self.ctx = ctx
            self.guilds = guilds
            self.admin_user_id = admin_user_id
            self.logging_channel = logging_channel
            self.server_id_map = server_id_map
            self.current_page = 1
            self.servers_per_page = 10
            self.sort_by = sort_by
            self.total_pages = math.ceil(len(self.guilds) / self.servers_per_page)
            self.sort_guilds()

        def sort_guilds(self):
            """Sortiert die Server-Liste basierend auf dem ausgewählten Kriterium"""
            if self.sort_by == "name":
                self.guilds.sort(key=lambda g: g.name.lower())
            elif self.sort_by == "members":
                self.guilds.sort(key=lambda g: g.member_count, reverse=True)
            elif self.sort_by == "online":
                self.guilds.sort(key=lambda g: len([m for m in g.members if m.status != Status.offline and not m.bot]), reverse=True)
            elif self.sort_by == "id":
                self.guilds.sort(key=lambda g: g.id)

            # Aktualisiere die Server-ID-Map nach der Sortierung
            self.server_id_map.clear()
            for i, guild in enumerate(self.guilds, 1):
                self.server_id_map[i] = guild.id

        def create_embed(self):
            """Erstellt ein Embed mit den Server-Informationen für die aktuelle Seite"""
            # Gesamte Nutzerzahlen berechnen
            total_users = sum(guild.member_count for guild in self.guilds)
            online_users = sum(len([m for m in guild.members if m.status != Status.offline and not m.bot]) for guild in self.guilds)

            # Erstelle das Embed
            embed = discord.Embed(
                title=f"🖥️ Server-Übersicht ({len(self.guilds)} Server)",
                description=f"**Gesamt:** {total_users} Nutzer ({online_users} online)\n\n"
                           f"**Sortierung:** {self.get_sort_name()}\n"
                           f"**Seite:** {self.current_page}/{self.total_pages}",
                color=0x3498db,
                timestamp=discord.utils.utcnow()
            )

            # Füge Server-Informationen hinzu
            start_idx = (self.current_page - 1) * self.servers_per_page
            end_idx = min(start_idx + self.servers_per_page, len(self.guilds))

            # Kompakteres Layout mit 3 Servern pro Zeile
            servers_per_row = 3
            current_row = []

            for i, guild in enumerate(self.guilds[start_idx:end_idx], start_idx + 1):
                # Bereinige den Server-Namen
                clean_name = re.sub(r'<a?:[a-zA-Z0-9_]+:[0-9]+>', '', guild.name)
                clean_name = re.sub(r'[^\w\s\-\.]', '', clean_name).strip()

                # Kürze den Namen, wenn er zu lang ist
                if len(clean_name) > 20:
                    clean_name = clean_name[:17] + "..."

                # Berechne Nutzerstatistiken
                guild_total = guild.member_count
                guild_online = len([m for m in guild.members if m.status != Status.offline and not m.bot])
                online_percent = round((guild_online / guild_total * 100), 1) if guild_total > 0 else 0

                # Fortlaufende ID
                server_id = i

                # Füge Server-Informationen zum Embed hinzu
                embed.add_field(
                    name=f"ID {server_id}: {clean_name}",
                    value=f"👥 {guild_total} ({guild_online} online)\n"
                          f"🆔 {guild.id}",
                    inline=True
                )

                # Nach jedem dritten Server eine leere Zeile einfügen für bessere Lesbarkeit
                if (i - start_idx + 1) % servers_per_row == 0:
                    # Füge einen leeren Spacer hinzu, wenn wir nicht am Ende sind
                    if i < end_idx - 1:
                        embed.add_field(name="\u200b", value="\u200b", inline=False)

            # Füge Hinweis zum Verlassen eines Servers hinzu
            embed.set_footer(text=f"Nutze !drache leave <ID> zum Verlassen eines Servers")

            return embed

        def get_sort_name(self):
            """Gibt den lesbaren Namen der aktuellen Sortierung zurück"""
            sort_names = {
                "name": "Alphabetisch (A-Z)",
                "members": "Mitgliederanzahl (absteigend)",
                "online": "Online-Nutzer (absteigend)",
                "id": "Discord-ID"
            }
            return sort_names.get(self.sort_by, "Unbekannt")

        @discord.ui.button(label="◀️ Zurück", style=discord.ButtonStyle.secondary)
        async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            """Button zum Zurückblättern"""
            if interaction.user.id != self.admin_user_id:
                await interaction.response.send_message("Du bist nicht berechtigt, diese Buttons zu nutzen!", ephemeral=True)
                return

            if self.current_page > 1:
                self.current_page -= 1
                await interaction.response.edit_message(embed=self.create_embed(), view=self)
            else:
                await interaction.response.defer()

        @discord.ui.button(label="▶️ Weiter", style=discord.ButtonStyle.secondary)
        async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            """Button zum Vorwärtsblättern"""
            if interaction.user.id != self.admin_user_id:
                await interaction.response.send_message("Du bist nicht berechtigt, diese Buttons zu nutzen!", ephemeral=True)
                return

            if self.current_page < self.total_pages:
                self.current_page += 1
                await interaction.response.edit_message(embed=self.create_embed(), view=self)
            else:
                await interaction.response.defer()

        @discord.ui.button(label="🔄 Aktualisieren", style=discord.ButtonStyle.primary)
        async def refresh_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            """Button zum Aktualisieren der Daten"""
            if interaction.user.id != self.admin_user_id:
                await interaction.response.send_message("Du bist nicht berechtigt, diese Buttons zu nutzen!", ephemeral=True)
                return

            # Aktualisiere die Guildliste
            self.guilds = list(interaction.client.guilds)
            self.total_pages = math.ceil(len(self.guilds) / self.servers_per_page)
            self.sort_guilds()

            # Stelle sicher, dass die aktuelle Seite gültig ist
            if self.current_page > self.total_pages:
                self.current_page = self.total_pages

            await interaction.response.edit_message(embed=self.create_embed(), view=self)

        @discord.ui.select(
            placeholder="Sortierung wählen",
            options=[
                discord.SelectOption(label="Alphabetisch (A-Z)", value="name", emoji="🔤"),
                discord.SelectOption(label="Mitgliederanzahl", value="members", emoji="👥"),
                discord.SelectOption(label="Online-Nutzer", value="online", emoji="🟢"),
                discord.SelectOption(label="Discord-ID", value="id", emoji="🆔")
            ]
        )
        async def sort_select(self, interaction: discord.Interaction, select: discord.ui.Select):
            """Dropdown-Menü zur Auswahl der Sortierung"""
            if interaction.user.id != self.admin_user_id:
                await interaction.response.send_message("Du bist nicht berechtigt, diese Buttons zu nutzen!", ephemeral=True)
                return

            self.sort_by = select.values[0]
            self.sort_guilds()
            self.current_page = 1  # Zurück zur ersten Seite

            await interaction.response.edit_message(embed=self.create_embed(), view=self)

        async def on_timeout(self):
            """Wird aufgerufen, wenn das Timeout abläuft"""
            # Deaktiviere alle Buttons
            for item in self.children:
                item.disabled = True

            # Aktualisiere die Nachricht, um die deaktivierten Buttons anzuzeigen
            try:
                message = await self.ctx.fetch_message(self.message.id)
                await message.edit(view=self)
            except:
                pass

    # Entfernen des alten !user Befehls, da er durch !drache server ersetzt wird

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

    @bot.command(name='buttergolem')
    async def buttergolem_command(ctx, action=None):
        """Admin-Befehle für den Bot"""
        if ctx.author.id != admin_user_id:
            await ctx.send("❌ Nur der Administrator kann diesen Befehl nutzen!")
            return

        if not action or action.lower() != 'stats':
            # Hilfe anzeigen
            help_text = (
                "**⚙️ Buttergolem Admin-Befehle**\n\n"
                "• `!buttergolem stats` - Zeigt detaillierte Bot-Statistiken an\n"
            )
            await ctx.send(help_text)
            return

        # STATS-Befehl
        if action.lower() == 'stats':
            # Sammle Statistiken
            total_servers = len(bot.guilds)
            total_members = sum(g.member_count for g in bot.guilds)
            unique_users = len(bot.stats_manager.stats['unique_users']) if hasattr(bot, 'stats_manager') else 0
            commands_used = bot.stats_manager.stats['commands_used'] if hasattr(bot, 'stats_manager') else 0
            sounds_played = bot.stats_manager.stats['sounds_played'] if hasattr(bot, 'stats_manager') else 0

            # Uptime berechnen
            bot_start_time = getattr(bot, 'start_time', datetime.datetime.now())
            uptime = datetime.datetime.now() - bot_start_time
            days, remainder = divmod(uptime.total_seconds(), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime_str = f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"

            # Systeminfo sammeln
            cpu_count = os.cpu_count() or "N/A"
            memory_usage = "N/A"
            try:
                import psutil
                memory = psutil.virtual_memory()
                memory_usage = f"{memory.percent}%"
            except ImportError:
                pass

            # Korrigiertes ASCII-Art mit ANSI-Farben
            ascii_art = (
                "```ansi\n"
                "[31;1m     .--. \n"
                "[31;1m[33;1m    /ò_ó  \\\n"
                "[31;1m[32;1m    |:_/  |\n"
                "[31;1m[36;1m   /     \\\\\n"
                "[31;1m[34;1m(|DRACHENLORD|)\n"
                "[31;1m[35;1m /'\_   _/`\\\n"
                "[31;1m[31;1m \___)=(___/\n"
                "```"
            )

            # Erstelle ein Embed mit den Statistiken im Neofetch-Stil
            embed = discord.Embed(
                title="📊 Buttergolem Bot Statistiken",
                description=f"{ascii_art}\n",
                color=0x3498db,
                timestamp=discord.utils.utcnow()
            )

            # Server & Nutzer (linke Spalte)
            embed.add_field(
                name="🖥️ Server & Nutzer",
                value=f"• **Server:** {total_servers}\n"
                      f"• **Gesamte Mitglieder:** {total_members}\n"
                      f"• **Eindeutige Nutzer:** {unique_users}\n"
                      f"• **Befehle ausgeführt:** {commands_used}\n"
                      f"• **Sounds abgespielt:** {sounds_played}",
                inline=True
            )

            # System (rechte Spalte)
            embed.add_field(
                name="⚙️ System",
                value=f"• **Uptime:** {uptime_str}\n"
                      f"• **Latenz:** {round(bot.latency * 1000)}ms\n"
                      f"• **CPU Kerne:** {cpu_count}\n"
                      f"• **RAM Nutzung:** {memory_usage}\n"
                      f"• **Discord.py:** {discord.__version__}",
                inline=True
            )

            # Sende das Embed
            await ctx.send(embed=embed)

            if logging_channel:
                await _log(f"Admin-Befehl !buttergolem stats wurde von {ctx.author.name} ausgeführt")

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

    @bot.command(name='drache')
    async def drache_command(ctx, action=None, server_id=None, *args):
        """Admin-Befehle für den Bot"""
        if ctx.author.id != admin_user_id:
            await ctx.send("❌ Nur der Administrator kann diesen Befehl nutzen!")
            return

        # Hilfe anzeigen, wenn keine Aktion angegeben wurde
        if not action:
            help_text = (
                "**⚙️ Admin-Befehle für den Bot**\n\n"
                "**Server-Verwaltung:**\n"
                "• `!drache server [page]` - Zeigt Server-Liste & Nutzerstatistiken\n"
                "• `!drache leave <server_id> [message_id] [grund...]` - Bot von einem Server entfernen\n"
                "• `!drache ban server <server_id> [grund...]` - Server bannen (ohne zu verlassen)\n"
                "• `!drache unban server <ban_id>` - Ban für einen Server aufheben\n"
                "• `!drache bans server` - Liste aller gebannten Server anzeigen\n\n"
                "**User-Verwaltung:**\n"
                "• `!drache ban user <user_id> [server_id] [grund...]` - User bannen (global oder serverspezifisch)\n"
                "• `!drache unban user <ban_id>` - Ban für einen User aufheben\n"
                "• `!drache bans user` - Liste aller gebannten User anzeigen\n\n"
                "**Beispiele:**\n"
                "`!drache server 2` - Zeigt Seite 2 der Server-Liste\n"
                "`!drache leave 123456789` - Verlässt den Server ohne Ban\n"
                "`!drache ban server 123456789 Spam und Belästigung` - Bannt den Server mit Grund\n"
                "`!drache ban user 987654321 123456789 Belästigung` - Bannt den User auf dem angegebenen Server\n"
                "`!drache ban user 987654321 Belästigung` - Bannt den User global\n"
                "`!drache unban server abc123` - Hebt den Server-Ban mit der ID abc123 auf\n"
                "`!drache unban user def456` - Hebt den User-Ban mit der ID def456 auf"
            )
            await ctx.send(help_text)
            return

        # LEAVE-Befehl
        if action.lower() == 'leave':
            if not server_id:
                await ctx.send("❌ Syntax: `!drache leave <server_id> [message_id] [grund...]`")
                return

            # Prüfen, ob es sich um eine fortlaufende ID oder eine Discord-ID handelt
            try:
                # Versuche, die ID als Zahl zu interpretieren (fortlaufende ID)
                if server_id.isdigit():
                    seq_id = int(server_id)
                    # Wenn es eine fortlaufende ID ist, hole die Discord-ID aus dem Dictionary
                    if seq_id in bot.server_id_map:
                        discord_id = bot.server_id_map[seq_id]
                    else:
                        # Wenn die fortlaufende ID nicht existiert, versuche sie als Discord-ID zu verwenden
                        discord_id = int(server_id)
                else:
                    # Wenn keine Zahl, kann es keine gültige ID sein
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
                        # Wenn keine Zahl, kann es keine gültige ID sein
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

        else:
            await ctx.send("❌ Unbekannte Aktion! Verfügbare Aktionen: `server`, `leave`, `ban`, `unban`, `bans`")

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
