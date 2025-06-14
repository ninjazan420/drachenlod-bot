#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import logging
import datetime
from os.path import join, dirname, abspath
import collections

# Pfad für Memory-Dateien
MEMORY_DIR = join(dirname(dirname(abspath(__file__))), 'data', 'memories')

# Stellen Sie sicher, dass das Verzeichnis existiert
os.makedirs(MEMORY_DIR, exist_ok=True)

class MemoryManager:
    """
    Verwaltet langfristige Erinnerungen für Benutzerinteraktionen mit dem Bot.
    Speichert Benutzerinformationen und Gesprächsverläufe in JSON-Dateien.
    """
    def __init__(self):
        self.memories = {}  # Cache für geladene Erinnerungen
        self.ensure_memory_dir()
    
    def ensure_memory_dir(self):
        """Stellt sicher, dass das Memory-Verzeichnis existiert"""
        os.makedirs(MEMORY_DIR, exist_ok=True)
    
    def get_memory_path(self, user_id):
        """Gibt den Pfad zur Memory-Datei für einen Benutzer zurück"""
        return join(MEMORY_DIR, f"{user_id}.json")
    
    def load_memory(self, user_id):
        """Lädt die Erinnerungen für einen Benutzer"""
        if user_id in self.memories:
            return self.memories[user_id]
        
        memory_path = self.get_memory_path(user_id)
        
        if os.path.exists(memory_path):
            try:
                with open(memory_path, 'r', encoding='utf-8') as f:
                    memory = json.load(f)
                    self.memories[user_id] = memory
                    return memory
            except Exception as e:
                logging.error(f"Fehler beim Laden der Erinnerungen für Benutzer {user_id}: {str(e)}")
                # Erstelle neue Erinnerung bei Fehler
                return self.create_new_memory(user_id)
        else:
            # Erstelle neue Erinnerung, wenn keine existiert
            return self.create_new_memory(user_id)
    
    def create_new_memory(self, user_id):
        """Erstellt eine neue Erinnerung für einen Benutzer"""
        memory = {
            "user_id": user_id,
            "created_at": datetime.datetime.now().isoformat(),
            "last_interaction": datetime.datetime.now().isoformat(),
            "interactions_count": 0,
            "user_info": {},
            "topics_discussed": [],
            "important_facts": [],
            "conversation_history": []
        }
        
        self.memories[user_id] = memory
        self.save_memory(user_id)
        return memory
    
    def save_memory(self, user_id):
        """Speichert die Erinnerungen für einen Benutzer"""
        if user_id not in self.memories:
            return
        
        memory_path = self.get_memory_path(user_id)
        
        try:
            with open(memory_path, 'w', encoding='utf-8') as f:
                json.dump(self.memories[user_id], f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"Fehler beim Speichern der Erinnerungen für Benutzer {user_id}: {str(e)}")
    
    def update_user_info(self, user_id, user_info):
        """Aktualisiert die Benutzerinformationen"""
        memory = self.load_memory(user_id)
        memory["user_info"].update(user_info)
        memory["last_interaction"] = datetime.datetime.now().isoformat()
        self.save_memory(user_id)
    
    def add_interaction(self, user_id, user_message, bot_response, user_info=None):
        """Fügt eine neue Interaktion zur Erinnerung hinzu"""
        memory = self.load_memory(user_id)
        
        # Aktualisiere Benutzerinformationen, falls vorhanden
        if user_info:
            memory["user_info"].update(user_info)
        
        # Füge Interaktion zum Verlauf hinzu
        interaction = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_message": user_message,
            "bot_response": bot_response
        }
        
        # Begrenze die Anzahl der gespeicherten Interaktionen auf 50
        memory["conversation_history"].append(interaction)
        if len(memory["conversation_history"]) > 50:
            memory["conversation_history"] = memory["conversation_history"][-50:]
        
        # Aktualisiere Metadaten
        memory["interactions_count"] += 1
        memory["last_interaction"] = datetime.datetime.now().isoformat()
        
        self.save_memory(user_id)
    
    def get_memory_summary(self, user_id):
        """Gibt eine Zusammenfassung der Erinnerungen für einen Benutzer zurück"""
        memory = self.load_memory(user_id)
        
        user_info = memory["user_info"]
        user_name = user_info.get("name", "Unbekannt")
        
        summary = f"Benutzer: {user_name} (ID: {user_id})\n"
        summary += f"Erste Interaktion: {memory['created_at']}\n"
        summary += f"Letzte Interaktion: {memory['last_interaction']}\n"
        summary += f"Anzahl der Interaktionen: {memory['interactions_count']}\n"
        
        if memory["important_facts"]:
            summary += "\nWichtige Fakten:\n"
            for fact in memory["important_facts"]:
                summary += f"- {fact}\n"
        
        if memory["topics_discussed"]:
            summary += "\nBesprochene Themen:\n"
            for topic in memory["topics_discussed"]:
                summary += f"- {topic}\n"
        
        return summary
    
    def add_important_fact(self, user_id, fact):
        """Fügt einen wichtigen Fakt zur Erinnerung hinzu"""
        memory = self.load_memory(user_id)
        
        if fact not in memory["important_facts"]:
            memory["important_facts"].append(fact)
            self.save_memory(user_id)
    
    def add_topic(self, user_id, topic):
        """Fügt ein besprochenes Thema zur Erinnerung hinzu"""
        memory = self.load_memory(user_id)
        
        if topic not in memory["topics_discussed"]:
            memory["topics_discussed"].append(topic)
            self.save_memory(user_id)
    
    def get_recent_conversations(self, user_id, limit=5):
        """Gibt die letzten Konversationen mit einem Benutzer zurück"""
        memory = self.load_memory(user_id)
        
        # Gib die letzten X Konversationen zurück
        return memory["conversation_history"][-limit:] if memory["conversation_history"] else []
    
    def get_all_memories(self):
        """Gibt eine Liste aller Benutzer-IDs zurück, für die Erinnerungen existieren"""
        memory_files = os.listdir(MEMORY_DIR)
        user_ids = [f.replace('.json', '') for f in memory_files if f.endswith('.json')]
        return user_ids
    
    def get_memory_context(self, user_id):
        """
        Erstellt einen Kontext für die KI basierend auf den Erinnerungen.
        Dieser Kontext kann in den Prompt eingefügt werden.
        """
        memory = self.load_memory(user_id)
        
        # Benutzerinformationen
        user_info = memory["user_info"]
        user_name = user_info.get("name", "Unbekannt")
        
        # Wichtige Fakten
        important_facts = memory["important_facts"]
        
        # Letzte Konversationen (begrenzt auf 3)
        recent_conversations = self.get_recent_conversations(user_id, 3)
        
        # Erstelle Kontext
        context = f"Informationen über {user_name} (Benutzer-ID: {user_id}):\n"
        
        # Füge Benutzerinformationen hinzu
        if user_info:
            context += "Benutzerinformationen:\n"
            for key, value in user_info.items():
                if key != "name":  # Name wurde bereits verwendet
                    context += f"- {key}: {value}\n"
        
        # Füge wichtige Fakten hinzu
        if important_facts:
            context += "\nWichtige Fakten über diesen Benutzer:\n"
            for fact in important_facts:
                context += f"- {fact}\n"
        
        # Füge letzte Konversationen hinzu
        if recent_conversations:
            context += "\nLetzte Konversationen mit diesem Benutzer:\n"
            for conv in recent_conversations:
                context += f"Benutzer: {conv['user_message']}\n"
                context += f"Du: {conv['bot_response']}\n\n"
        
        return context

# Funktion zum Registrieren des MemoryManagers
def register_memory_manager(client):
    """Registriert den MemoryManager für den Bot"""
    client.memory_manager = MemoryManager()
    logging.info("MemoryManager wurde initialisiert")
