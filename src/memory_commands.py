#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import datetime
import json
import os
from os.path import join, dirname, abspath
import logging

# Pfad für Memory-Dateien
MEMORY_DIR = join(dirname(dirname(abspath(__file__))), 'data', 'memories')

# Stellen Sie sicher, dass das Verzeichnis existiert
os.makedirs(MEMORY_DIR, exist_ok=True)

def register_memory_commands(client):
    """Registriert Befehle für die Memory-Funktionalität"""
    
    @client.command(name="memory_admin")
    @commands.is_owner()
    async def memory_command(ctx, action=None, user_id=None, *args):
        """
        Verwaltet die Memory-Funktionalität des Bots.
        
        Aktionen:
        - list: Listet alle Benutzer mit Erinnerungen auf
        - show <user_id>: Zeigt die Erinnerungen für einen bestimmten Benutzer
        - add <user_id> <fact>: Fügt einen wichtigen Fakt für einen Benutzer hinzu
        - topic <user_id> <topic>: Fügt ein besprochenes Thema für einen Benutzer hinzu
        - delete <user_id>: Löscht die Erinnerungen für einen bestimmten Benutzer
        """
        if not hasattr(client, 'memory_manager'):
            await ctx.send("❌ Memory-Manager ist nicht initialisiert!")
            return
        
        if action is None:
            # Zeige Hilfe
            embed = discord.Embed(
                title="🧠 Memory-Befehle",
                description="Verwalte die Erinnerungen des Bots an Benutzer",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="Verfügbare Aktionen",
                value="```\n"
                      "!memory list                - Listet alle Benutzer mit Erinnerungen auf\n"
                      "!memory show <user_id>      - Zeigt die Erinnerungen für einen Benutzer\n"
                      "!memory add <user_id> <fact> - Fügt einen wichtigen Fakt hinzu\n"
                      "!memory topic <user_id> <topic> - Fügt ein besprochenes Thema hinzu\n"
                      "!memory delete <user_id>    - Löscht die Erinnerungen für einen Benutzer\n"
                      "```",
                inline=False
            )
            
            await ctx.send(embed=embed)
            return
        
        # Verarbeite die verschiedenen Aktionen
        if action.lower() == "list":
            # Liste alle Benutzer mit Erinnerungen auf
            user_ids = client.memory_manager.get_all_memories()
            
            if not user_ids:
                await ctx.send("Keine Erinnerungen gefunden.")
                return
            
            embed = discord.Embed(
                title="🧠 Benutzer mit Erinnerungen",
                description=f"Insgesamt {len(user_ids)} Benutzer",
                color=discord.Color.blue()
            )
            
            # Versuche, die Benutzernamen zu den IDs zu finden
            user_list = []
            for uid in user_ids:
                try:
                    # Lade die Erinnerung, um den Namen zu bekommen
                    memory = client.memory_manager.load_memory(uid)
                    user_name = memory["user_info"].get("name", "Unbekannt")
                    interactions = memory["interactions_count"]
                    user_list.append(f"• {user_name} (ID: {uid}) - {interactions} Interaktionen")
                except:
                    user_list.append(f"• Unbekannt (ID: {uid})")
            
            # Teile die Liste in Chunks auf, falls sie zu lang ist
            chunks = [user_list[i:i+20] for i in range(0, len(user_list), 20)]
            
            for i, chunk in enumerate(chunks):
                if i == 0:
                    embed.add_field(
                        name="Benutzer",
                        value="\n".join(chunk),
                        inline=False
                    )
                else:
                    embed.add_field(
                        name=f"Benutzer (Fortsetzung {i+1})",
                        value="\n".join(chunk),
                        inline=False
                    )
            
            await ctx.send(embed=embed)
        
        elif action.lower() == "show":
            # Zeige die Erinnerungen für einen bestimmten Benutzer
            if user_id is None:
                await ctx.send("❌ Bitte gib eine Benutzer-ID an!")
                return
            
            try:
                # Versuche, die Erinnerungen zu laden
                memory = client.memory_manager.load_memory(user_id)
                
                # Erstelle ein Embed mit den Informationen
                user_name = memory["user_info"].get("name", "Unbekannt")
                
                embed = discord.Embed(
                    title=f"🧠 Erinnerungen für {user_name}",
                    description=f"Benutzer-ID: {user_id}",
                    color=discord.Color.blue()
                )
                
                # Füge Benutzerinformationen hinzu
                user_info_text = ""
                for key, value in memory["user_info"].items():
                    user_info_text += f"• {key}: {value}\n"
                
                embed.add_field(
                    name="Benutzerinformationen",
                    value=user_info_text or "Keine Informationen",
                    inline=False
                )
                
                # Füge wichtige Fakten hinzu
                facts_text = ""
                for fact in memory["important_facts"]:
                    facts_text += f"• {fact}\n"
                
                embed.add_field(
                    name="Wichtige Fakten",
                    value=facts_text or "Keine wichtigen Fakten",
                    inline=False
                )
                
                # Füge besprochene Themen hinzu
                topics_text = ""
                for topic in memory["topics_discussed"]:
                    topics_text += f"• {topic}\n"
                
                embed.add_field(
                    name="Besprochene Themen",
                    value=topics_text or "Keine besprochenen Themen",
                    inline=False
                )
                
                # Füge letzte Konversationen hinzu (begrenzt auf 3)
                recent_conversations = client.memory_manager.get_recent_conversations(user_id, 3)
                
                if recent_conversations:
                    conv_text = ""
                    for i, conv in enumerate(recent_conversations):
                        conv_text += f"**Konversation {i+1}:**\n"
                        conv_text += f"Benutzer: {conv['user_message'][:100]}...\n"
                        conv_text += f"Bot: {conv['bot_response'][:100]}...\n\n"
                    
                    embed.add_field(
                        name="Letzte Konversationen",
                        value=conv_text,
                        inline=False
                    )
                else:
                    embed.add_field(
                        name="Letzte Konversationen",
                        value="Keine Konversationen",
                        inline=False
                    )
                
                # Füge Metadaten hinzu
                embed.set_footer(text=f"Erste Interaktion: {memory['created_at']} | Letzte Interaktion: {memory['last_interaction']}")
                
                await ctx.send(embed=embed)
            
            except Exception as e:
                await ctx.send(f"❌ Fehler beim Laden der Erinnerungen: {str(e)}")
        
        elif action.lower() == "add":
            # Füge einen wichtigen Fakt für einen Benutzer hinzu
            if user_id is None:
                await ctx.send("❌ Bitte gib eine Benutzer-ID an!")
                return
            
            if not args:
                await ctx.send("❌ Bitte gib einen Fakt an!")
                return
            
            fact = " ".join(args)
            
            try:
                client.memory_manager.add_important_fact(user_id, fact)
                await ctx.send(f"✅ Fakt für Benutzer {user_id} hinzugefügt: {fact}")
            except Exception as e:
                await ctx.send(f"❌ Fehler beim Hinzufügen des Fakts: {str(e)}")
        
        elif action.lower() == "topic":
            # Füge ein besprochenes Thema für einen Benutzer hinzu
            if user_id is None:
                await ctx.send("❌ Bitte gib eine Benutzer-ID an!")
                return
            
            if not args:
                await ctx.send("❌ Bitte gib ein Thema an!")
                return
            
            topic = " ".join(args)
            
            try:
                client.memory_manager.add_topic(user_id, topic)
                await ctx.send(f"✅ Thema für Benutzer {user_id} hinzugefügt: {topic}")
            except Exception as e:
                await ctx.send(f"❌ Fehler beim Hinzufügen des Themas: {str(e)}")
        
        elif action.lower() == "delete":
            # Lösche die Erinnerungen für einen bestimmten Benutzer
            if user_id is None:
                await ctx.send("❌ Bitte gib eine Benutzer-ID an!")
                return
            
            try:
                # Lösche die Erinnerungsdatei
                memory_path = join(MEMORY_DIR, f"{user_id}.json")
                
                if os.path.exists(memory_path):
                    os.remove(memory_path)
                    
                    # Entferne auch aus dem Cache, falls vorhanden
                    if hasattr(client.memory_manager, 'memories') and user_id in client.memory_manager.memories:
                        del client.memory_manager.memories[user_id]
                    
                    await ctx.send(f"✅ Erinnerungen für Benutzer {user_id} wurden gelöscht.")
                else:
                    await ctx.send(f"❌ Keine Erinnerungen für Benutzer {user_id} gefunden.")
            
            except Exception as e:
                await ctx.send(f"❌ Fehler beim Löschen der Erinnerungen: {str(e)}")
        
        else:
            await ctx.send(f"❌ Unbekannte Aktion: {action}")
