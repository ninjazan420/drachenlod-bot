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
# Premium-Funktionalität entfernt - nur noch Spenden-Hinweise

# Stellen Sie sicher, dass das Verzeichnis existiert
os.makedirs(join(dirname(abspath(__file__)), 'data'), exist_ok=True)

class ButterIQManager:
    """Verwaltet die Sperrung und Freigabe von Benutzer-IDs für ButterIQ"""
    def __init__(self):
        self.disabled_users = set()  # Set mit gesperrten Benutzer-IDs
        # Premium-Funktionalität entfernt
        self._load_disabled_users()
        # Supporter-System entfernt

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

    # Premium/Supporter-System entfernt - nur noch Spenden-Hinweise

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

    # Premium/Supporter-System entfernt - keine Vorteile mehr
    # Nur noch Spenden-Hinweise verfügbar

def register_butteriq_commands(bot):
    """Registriert die ButterIQ-Befehle"""
    # Initialisiere den ButterIQ-Manager
    bot.butteriq_manager = ButterIQManager()

    # Removed - integrated into main drache command as 'butteriq' subcommand
    # See admins.py for the new implementation

        # Logic moved to admins.py drache command

    # Spenden-Funktionalität wurde zu /spende Slash Command migriert
    # Siehe slash_commands.py für die neue Monero-basierte Spenden-Funktionalität
