#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import os
import json
import logging
import datetime
from os.path import join, dirname, abspath

import discord
from discord.ext import commands
from discord import app_commands

# Pfad für die Datei mit gesperrten Benutzer-IDs
DISABLED_USERS_PATH = join(dirname(abspath(__file__)), 'data', 'disabled_users.json')
PREMIUM_USERS_PATH = join(dirname(abspath(__file__)), 'data', 'premium_users.json')

# Stellen Sie sicher, dass das Verzeichnis existiert
os.makedirs(join(dirname(abspath(__file__)), 'data'), exist_ok=True)

class ButterIQManager:
    """Verwaltet die Sperrung und Freigabe von Benutzer-IDs für ButterIQ"""
    def __init__(self):
        self.disabled_users = set()  # Set mit gesperrten Benutzer-IDs
        self.premium_users = {}  # Dict mit Unterstützern und Ablaufdatum (früher "Premium-Benutzer")
        self._load_disabled_users()
        self._load_supporters()

    def _load_disabled_users(self):
        """Lädt die gesperrten Benutzer-IDs aus der Datei"""
        try:
            if os.path.exists(DISABLED_USERS_PATH):
                with open(DISABLED_USERS_PATH, 'r') as f:
                    data = json.load(f)
                    self.disabled_users = set(data.get('disabled_users', []))
                    logging.info(f"Gesperrte Benutzer-IDs geladen: {len(self.disabled_users)}")
        except Exception as e:
            logging.error(f"Fehler beim Laden der gesperrten Benutzer-IDs: {e}")

    def _save_disabled_users(self):
        """Speichert die gesperrten Benutzer-IDs in einer Datei"""
        try:
            save_data = {
                'disabled_users': list(self.disabled_users),
                'last_update': datetime.datetime.now().isoformat()
            }
            with open(DISABLED_USERS_PATH, 'w') as f:
                json.dump(save_data, f)
            logging.info(f"Gesperrte Benutzer-IDs gespeichert: {len(self.disabled_users)}")
        except Exception as e:
            logging.error(f"Fehler beim Speichern der gesperrten Benutzer-IDs: {e}")

    def _load_supporters(self):
        """Lädt die Unterstützer aus der Datei"""
        try:
            if os.path.exists(PREMIUM_USERS_PATH):
                with open(PREMIUM_USERS_PATH, 'r') as f:
                    data = json.load(f)
                    self.premium_users = data.get('premium_users', {})
                    logging.info(f"Unterstützer geladen: {len(self.premium_users)}")
        except Exception as e:
            logging.error(f"Fehler beim Laden der Unterstützer: {e}")

    def _save_supporters(self):
        """Speichert die Unterstützer in einer Datei"""
        try:
            save_data = {
                'premium_users': self.premium_users,  # Behalte den Schlüssel für Abwärtskompatibilität
                'last_update': datetime.datetime.now().isoformat()
            }
            with open(PREMIUM_USERS_PATH, 'w') as f:
                json.dump(save_data, f)
            logging.info(f"Unterstützer gespeichert: {len(self.premium_users)}")
        except Exception as e:
            logging.error(f"Fehler beim Speichern der Unterstützer: {e}")

    def disable_user(self, user_id):
        """Sperrt eine Benutzer-ID für ButterIQ"""
        user_id = str(user_id)  # Konvertiere zu String für konsistente Speicherung
        self.disabled_users.add(user_id)
        self._save_disabled_users()
        return True

    def enable_user(self, user_id):
        """Gibt eine Benutzer-ID für ButterIQ frei"""
        user_id = str(user_id)  # Konvertiere zu String für konsistente Speicherung
        if user_id in self.disabled_users:
            self.disabled_users.remove(user_id)
            self._save_disabled_users()
            return True
        return False

    def is_disabled(self, user_id):
        """Prüft, ob eine Benutzer-ID für ButterIQ gesperrt ist"""
        return str(user_id) in self.disabled_users

    def add_supporter(self, user_id, duration_days=30):
        """Fügt einen Benutzer als Unterstützer hinzu"""
        user_id = str(user_id)  # Konvertiere zu String für konsistente Speicherung

        # Berechne Ablaufdatum
        expiry_date = (datetime.datetime.now() + datetime.timedelta(days=duration_days)).isoformat()

        self.premium_users[user_id] = {
            "expiry_date": expiry_date,
            "added_date": datetime.datetime.now().isoformat(),
            "duration_days": duration_days
        }

        self._save_supporters()
        return True

    def remove_supporter(self, user_id):
        """Entfernt einen Benutzer aus den Unterstützern"""
        user_id = str(user_id)  # Konvertiere zu String für konsistente Speicherung

        if user_id in self.premium_users:
            del self.premium_users[user_id]
            self._save_supporters()
            return True
        return False

    def is_supporter(self, user_id):
        """Prüft, ob ein Benutzer den Bot unterstützt"""
        user_id = str(user_id)  # Konvertiere zu String für konsistente Speicherung

        if user_id not in self.premium_users:
            return False

        # Prüfe, ob der Unterstützungszeitraum abgelaufen ist
        expiry_date = datetime.datetime.fromisoformat(self.premium_users[user_id]["expiry_date"])
        if expiry_date < datetime.datetime.now():
            # Unterstützungszeitraum ist abgelaufen, entferne den Benutzer
            self.remove_supporter(user_id)
            return False

        return True

    # Behalte die alte Methode für Abwärtskompatibilität
    def is_premium(self, user_id):
        """Alias für is_supporter (für Abwärtskompatibilität)"""
        return self.is_supporter(user_id)

def register_butteriq_commands(bot):
    """Registriert die ButterIQ-Befehle"""
    # Initialisiere den ButterIQ-Manager
    bot.butteriq_manager = ButterIQManager()

    @bot.command(name='butteriq')
    async def butteriq_command(ctx, action=None, user_id=None):
        """Admin-Befehle für ButterIQ"""
        if ctx.author.id != bot.admin_user_id:
            await ctx.send("❌ Nur der Administrator kann diesen Befehl nutzen!")
            return

        if not action or not user_id:
            # Hilfe anzeigen
            help_text = (
                "**⚙️ ButterIQ Admin-Befehle**\n\n"
                "• `!butteriq disable <user_id>` - Sperrt eine Benutzer-ID für ButterIQ\n"
                "• `!butteriq enable <user_id>` - Gibt eine Benutzer-ID für ButterIQ frei\n"
            )
            await ctx.send(help_text)
            return

        # Versuche, die Benutzer-ID zu konvertieren
        try:
            user_id = int(user_id)
        except ValueError:
            await ctx.send("❌ Ungültige Benutzer-ID! Bitte gib eine gültige ID an.")
            return

        if action.lower() == 'disable':
            # Benutzer-ID sperren
            bot.butteriq_manager.disable_user(user_id)
            await ctx.send(f"✅ Benutzer-ID {user_id} wurde für ButterIQ gesperrt.")
        elif action.lower() == 'enable':
            # Benutzer-ID freigeben
            if bot.butteriq_manager.enable_user(user_id):
                await ctx.send(f"✅ Benutzer-ID {user_id} wurde für ButterIQ freigegeben.")
            else:
                await ctx.send(f"❌ Benutzer-ID {user_id} war nicht gesperrt.")
        else:
            await ctx.send("❌ Ungültige Aktion! Verfügbare Aktionen: `disable`, `enable`")

    # Slash-Befehle für Unterstützung/Spenden
    premium_group = app_commands.Group(name="premium", description="Unterstütze den Bot mit einer Spende")

    @premium_group.command(name="info", description="Zeigt Informationen zur Unterstützung des Bots an")
    async def premium_info(interaction: discord.Interaction):
        """Zeigt Informationen zur Unterstützung des Bots an"""
        is_supporter = bot.butteriq_manager.is_supporter(interaction.user.id)

        embed = discord.Embed(
            title="💖 Bot unterstützen",
            description="Wenn dir der Bot gefällt, kannst du ihn mit einer Spende unterstützen.",
            color=0x00ff00 if is_supporter else 0xff0000
        )

        embed.add_field(
            name="Status",
            value="✅ Du unterstützt den Bot bereits - vielen Dank!" if is_supporter else "❌ Du unterstützt den Bot noch nicht",
            inline=False
        )

        embed.add_field(
            name="Warum spenden?",
            value="• Hilf mit, die Serverkosten zu decken\n"
                  "• Unterstütze die Weiterentwicklung\n"
                  "• Zeige deine Wertschätzung",
            inline=False
        )

        if not is_supporter:
            embed.add_field(
                name="Bot unterstützen",
                value="Nutze `/premium spenden` um mehr zu erfahren!",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @premium_group.command(name="spenden", description="Unterstütze den Bot mit einer Spende")
    async def premium_donate(interaction: discord.Interaction):
        """Unterstütze den Bot mit einer Spende"""
        is_supporter = bot.butteriq_manager.is_supporter(interaction.user.id)

        if is_supporter:
            await interaction.response.send_message("Du unterstützt den Bot bereits - vielen Dank für deine Unterstützung!", ephemeral=True)
            return

        # Erstelle ein Embed mit Spendeninformationen
        embed = discord.Embed(
            title="💖 Bot unterstützen",
            description="Wenn dir der Bot gefällt, kannst du ihn mit einer Spende unterstützen:",
            color=0x00ff00
        )

        embed.add_field(
            name="Warum spenden?",
            value="• Hilf mit, die Serverkosten zu decken\n"
                  "• Unterstütze die Weiterentwicklung\n"
                  "• Zeige deine Wertschätzung",
            inline=False
        )

        embed.add_field(
            name="Spendenmöglichkeiten",
            value="Bitte kontaktiere den Bot-Administrator über `!kontakt` wenn du den Bot unterstützen möchtest.",
            inline=False
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    # Registriere die Premium-Gruppe
    bot.tree.add_command(premium_group)
