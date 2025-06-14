import json
import os
from datetime import datetime

class StatsManager:
    def __init__(self, stats_file="data/stats.json"):
        self.stats_file = stats_file
        self.stats = self.load_stats()

    def load_stats(self):
        """Lädt die Statistiken aus der JSON-Datei"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        # Standard-Statistiken wenn Datei nicht existiert oder fehlerhaft ist
        return {
            "commands_executed": 0,
            "servers_joined": 0,
            "servers_left": 0,
            "messages_processed": 0,
            "sounds_played": 0,
            "unique_users": [],
            "uptime_start": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }

    def save_stats(self):
        """Speichert die Statistiken in die JSON-Datei"""
        try:
            # Erstelle Verzeichnis falls es nicht existiert
            os.makedirs(os.path.dirname(self.stats_file), exist_ok=True)
            
            self.stats["last_updated"] = datetime.now().isoformat()
            
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Fehler beim Speichern der Statistiken: {e}")

    def increment_commands(self):
        """Erhöht den Zähler für ausgeführte Befehle"""
        self.stats["commands_executed"] += 1
        self.save_stats()

    def increment_sounds_played(self):
        """Erhöht den Zähler für abgespielte Sounds"""
        if "sounds_played" not in self.stats:
            self.stats["sounds_played"] = 0
        self.stats["sounds_played"] += 1
        self.save_stats()

    def increment_servers_joined(self):
        """Erhöht den Zähler für beigetretene Server"""
        self.stats["servers_joined"] += 1
        self.save_stats()

    def increment_servers_left(self):
        """Erhöht den Zähler für verlassene Server"""
        self.stats["servers_left"] += 1
        self.save_stats()

    def increment_messages(self):
        """Erhöht den Zähler für verarbeitete Nachrichten"""
        self.stats["messages_processed"] += 1
        self.save_stats()

    def add_unique_user(self, user_id):
        """Fügt einen einzigartigen Benutzer zur Liste hinzu"""
        if "unique_users" not in self.stats:
            self.stats["unique_users"] = []
        
        if user_id not in self.stats["unique_users"]:
            self.stats["unique_users"].append(user_id)
            self.save_stats()

    def get_stats(self):
        """Gibt die aktuellen Statistiken zurück"""
        return self.stats.copy()

    def reset_stats(self):
        """Setzt alle Statistiken zurück"""
        self.stats = {
            "commands_executed": 0,
            "servers_joined": 0,
            "servers_left": 0,
            "messages_processed": 0,
            "sounds_played": 0,
            "unique_users": [],
            "uptime_start": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        self.save_stats()