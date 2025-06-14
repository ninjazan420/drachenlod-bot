import json
import os
import uuid
from datetime import datetime

class BanManager:
    def __init__(self, ban_file="data/ban.json"):
        self.ban_file = ban_file
        self.data = self.load_data()
        self.bans = self.data.get("server_bans", [])
        self.user_bans = self.data.get("user_bans", [])

    def load_data(self):
        """Lädt alle Ban-Daten aus der JSON-Datei"""
        if os.path.exists(self.ban_file):
            try:
                with open(self.ban_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {"server_bans": [], "user_bans": []}

    def save_data(self):
        """Speichert alle Ban-Daten in die JSON-Datei"""
        try:
            # Erstelle Verzeichnis falls es nicht existiert
            os.makedirs(os.path.dirname(self.ban_file), exist_ok=True)
            
            self.data = {
                "server_bans": self.bans,
                "user_bans": self.user_bans
            }
            
            with open(self.ban_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Fehler beim Speichern der Ban-Daten: {e}")

    def add_ban(self, server_id, server_name, reason=None, message_id=None):
        """Fügt einen Server-Ban hinzu"""
        ban_id = str(uuid.uuid4())
        
        ban = {
            "ban_id": ban_id,
            "server_id": str(server_id),
            "server_name": server_name,
            "reason": reason or "Kein Grund angegeben",
            "message_id": message_id,
            "timestamp": datetime.now().isoformat(),
            "active": True
        }
        self.bans.append(ban)
        self.save_data()
        return ban_id

    def add_user_ban(self, user_id, username, server_id=None, server_name=None, reason=None):
        """Fügt einen User-Ban hinzu"""
        ban_id = str(uuid.uuid4())
        
        ban = {
            "ban_id": ban_id,
            "user_id": str(user_id),
            "username": username,
            "server_id": str(server_id) if server_id else None,
            "server_name": server_name,
            "reason": reason or "Kein Grund angegeben",
            "timestamp": datetime.now().isoformat(),
            "active": True
        }
        self.user_bans.append(ban)
        self.save_data()
        return ban_id

    def remove_ban(self, ban_id):
        """Entfernt einen Server-Ban (setzt ihn auf inaktiv)"""
        for ban in self.bans:
            if ban["ban_id"] == str(ban_id) and ban["active"]:
                ban["active"] = False
                ban["removed_timestamp"] = datetime.now().isoformat()
                self.save_data()
                return True
        return False

    def remove_user_ban(self, ban_id):
        """Entfernt einen User-Ban (setzt ihn auf inaktiv)"""
        for ban in self.user_bans:
            if ban["ban_id"] == str(ban_id) and ban["active"]:
                ban["active"] = False
                ban["removed_timestamp"] = datetime.now().isoformat()
                self.save_data()
                return True
        return False

    def is_banned(self, server_id):
        """Prüft, ob ein Server gebannt ist"""
        for ban in self.bans:
            if ban["server_id"] == str(server_id) and ban["active"]:
                return True
        return False

    def is_user_banned(self, user_id, server_id=None):
        """Prüft, ob ein User gebannt ist (global oder auf einem bestimmten Server)"""
        for ban in self.user_bans:
            if ban["user_id"] == str(user_id) and ban["active"]:
                # Globaler Ban (kein server_id gesetzt)
                if ban["server_id"] is None:
                    return True
                # Server-spezifischer Ban
                if server_id and ban["server_id"] == str(server_id):
                    return True
        return False

    def get_ban_by_id(self, ban_id):
        """Gibt einen Server-Ban anhand der ID zurück"""
        for ban in self.bans:
            if ban["ban_id"] == str(ban_id):
                return ban
        return None

    def get_user_ban_by_id(self, ban_id):
        """Gibt einen User-Ban anhand der ID zurück"""
        for ban in self.user_bans:
            if ban["ban_id"] == str(ban_id):
                return ban
        return None

    def get_all_bans(self):
        """Gibt alle aktiven Server-Bans zurück"""
        return [ban for ban in self.bans if ban["active"]]

    def get_all_user_bans(self):
        """Gibt alle aktiven User-Bans zurück"""
        return [ban for ban in self.user_bans if ban["active"]]

    def get_server_ban(self, server_id):
        """Gibt den aktiven Ban für einen Server zurück"""
        for ban in self.bans:
            if ban["server_id"] == str(server_id) and ban["active"]:
                return ban
        return None

    def get_user_ban(self, user_id, server_id=None):
        """Gibt den aktiven Ban für einen User zurück"""
        for ban in self.user_bans:
            if ban["user_id"] == str(user_id) and ban["active"]:
                # Globaler Ban hat Priorität
                if ban["server_id"] is None:
                    return ban
                # Server-spezifischer Ban
                if server_id and ban["server_id"] == str(server_id):
                    return ban
        return None