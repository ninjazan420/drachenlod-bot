#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import datetime
import json
import os
from os.path import join, dirname, abspath
import logging

# Pfad für ButterIQ-Dateien
BUTTERIQ_DIR = join(dirname(dirname(abspath(__file__))), 'data', 'butteriq')

# Stellen Sie sicher, dass das Verzeichnis existiert
os.makedirs(BUTTERIQ_DIR, exist_ok=True)

def register_butteriq_commands(client):
    """Registriert Befehle für die ButterIQ-Funktionalität"""

    @client.command(name="drache_butteriq")
    async def drache_butteriq_command(ctx, action=None, subaction=None, user_id=None, data_type=None, *args):
        """
        Verwaltet die ButterIQ-Funktionalität des Bots über das !drache butteriq System.

        Aktionen:
        - butteriq list: Listet alle Benutzer mit ButterIQ-Daten auf
        - butteriq show <user_id> [data_type]: Zeigt die ButterIQ-Daten für einen bestimmten Benutzer
        - butteriq add <user_id> <fact>: Fügt einen wichtigen Fakt für einen Benutzer hinzu
        - butteriq update <user_id>: Aktualisiert die Profilinformationen eines Benutzers
        - butteriq delete <user_id>: Löscht die ButterIQ-Daten für einen bestimmten Benutzer
        """
        # Prüfe ob es sich um einen ButterIQ-Befehl handelt
        if action != "butteriq":
            return  # Nicht unser Befehl, lass andere Handler ran

        if not hasattr(client, 'butteriq_manager'):
            await ctx.send("❌ ButterIQ-Manager ist nicht initialisiert!")
            return

        # Nur Admin darf diesen Befehl nutzen
        if ctx.author.id != client.admin_user_id:
            await ctx.send("❌ Nur der Administrator kann diesen Befehl nutzen!")
            return

        if subaction is None:
            # Zeige Hilfe
            embed = discord.Embed(
                title="🧠 ButterIQ-Befehle",
                description="Verwalte die ButterIQ-Daten des Bots über Benutzer",
                color=discord.Color.blue()
            )

            embed.add_field(
                name="Verfügbare Aktionen",
                value="```\n"
                      "!drache butteriq list                - Listet alle Benutzer mit ButterIQ-Daten auf\n"
                      "!drache butteriq show <user_id> [data_type] - Zeigt die ButterIQ-Daten für einen Benutzer\n"
                      "!drache butteriq add <user_id> <fact> - Fügt einen wichtigen Fakt hinzu\n"
                      "!drache butteriq update <user_id>    - Aktualisiert die Profilinformationen\n"
                      "!drache butteriq delete <user_id>    - Löscht die ButterIQ-Daten für einen Benutzer\n"
                      "!drache butteriq enable <user_id>    - Aktiviert das Tracking für einen Benutzer\n"
                      "!drache butteriq disable <user_id>   - Deaktiviert das Tracking für einen Benutzer\n"
                      "```",
                inline=False
            )

            embed.add_field(
                name="Verfügbare Datentypen",
                value="```\n"
                      "profile - Zeigt Profilinformationen (Standard)\n"
                      "games   - Zeigt gespielte Spiele\n"
                      "chat    - Zeigt Chatverläufe und Interaktionen\n"
                      "all     - Zeigt alle verfügbaren Informationen\n"
                      "```",
                inline=False
            )

            await ctx.send(embed=embed)
            return

        elif subaction.lower() == "list":
            # Liste alle Benutzer mit ButterIQ-Daten auf
            try:
                user_ids = client.butteriq_manager.get_all_users()

                if not user_ids:
                    await ctx.send("Keine ButterIQ-Daten vorhanden.")
                    return

                # Erstelle ein Embed mit der Liste der Benutzer
                embed = discord.Embed(
                    title="🧠 Benutzer mit ButterIQ-Daten",
                    description=f"Insgesamt {len(user_ids)} Benutzer",
                    color=discord.Color.blue()
                )

                # Versuche, die Benutzernamen zu laden
                user_list = []
                for uid in user_ids:
                    try:
                        data = client.butteriq_manager.load_user_data(uid)
                        profile = data["profile"]
                        user_name = profile.get("display_name", profile.get("name", "Unbekannt"))
                        user_list.append(f"• {user_name} (ID: {uid})")
                    except Exception as e:
                        user_list.append(f"• ID: {uid} (Fehler: {str(e)})")

                # Teile die Liste in Chunks auf, falls sie zu lang ist
                chunks = [user_list[i:i+20] for i in range(0, len(user_list), 20)]

                for i, chunk in enumerate(chunks):
                    embed.add_field(
                        name=f"Benutzer {i*20+1}-{i*20+len(chunk)}",
                        value="\n".join(chunk),
                        inline=False
                    )

                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(f"❌ Fehler beim Auflisten der Benutzer: {str(e)}")

        elif subaction.lower() == "show":
            # Zeige die ButterIQ-Daten für einen bestimmten Benutzer
            if user_id is None:
                await ctx.send("❌ Bitte gib eine Benutzer-ID an!")
                return

            # Wenn kein Datentyp angegeben wurde, verwende "profile"
            if data_type is None:
                data_type = "profile"

            # Überprüfe, ob der Datentyp gültig ist
            valid_types = ["profile", "games", "chat", "all"]
            if data_type.lower() not in valid_types:
                await ctx.send(f"❌ Ungültiger Datentyp! Gültige Typen: {', '.join(valid_types)}")
                return

            try:
                # Formatiere die Daten im neofetch-Stil
                formatted_data = client.butteriq_manager.format_user_data_neofetch(user_id, data_type.lower())

                # Sende die formatierte Nachricht
                await ctx.send(formatted_data)

                # Füge das aktuelle Datum und die Uhrzeit hinzu
                current_time = datetime.datetime.now().strftime("heute um %H:%M Uhr")
                await ctx.send(current_time)

            except Exception as e:
                await ctx.send(f"❌ Fehler beim Anzeigen der ButterIQ-Daten: {str(e)}")

        elif subaction.lower() == "add":
            # Füge einen wichtigen Fakt für einen Benutzer hinzu
            if user_id is None:
                await ctx.send("❌ Bitte gib eine Benutzer-ID an!")
                return

            if not args:
                await ctx.send("❌ Bitte gib einen Fakt an!")
                return

            fact = " ".join(args)

            try:
                client.butteriq_manager.add_important_fact(user_id, fact)
                await ctx.send(f"✅ Fakt für Benutzer {user_id} hinzugefügt: {fact}")
            except Exception as e:
                await ctx.send(f"❌ Fehler beim Hinzufügen des Fakts: {str(e)}")

        elif subaction.lower() == "update":
            # Aktualisiere die Profilinformationen eines Benutzers
            if user_id is None:
                await ctx.send("❌ Bitte gib eine Benutzer-ID an!")
                return

            try:
                # Versuche, den Benutzer zu finden
                user = None
                for guild in client.guilds:
                    user = guild.get_member(int(user_id))
                    if user:
                        break

                if not user:
                    await ctx.send(f"❌ Benutzer mit ID {user_id} wurde nicht gefunden!")
                    return

                # Aktualisiere die Profilinformationen
                client.butteriq_manager.update_user_from_discord(user_id, user)
                await ctx.send(f"✅ Profilinformationen für Benutzer {user.display_name} (ID: {user_id}) wurden aktualisiert.")

            except Exception as e:
                await ctx.send(f"❌ Fehler beim Aktualisieren der Profilinformationen: {str(e)}")

        elif subaction.lower() == "delete":
            # Lösche die ButterIQ-Daten für einen bestimmten Benutzer
            if user_id is None:
                await ctx.send("❌ Bitte gib eine Benutzer-ID an!")
                return

            try:
                # Lösche die ButterIQ-Datei
                butteriq_path = join(BUTTERIQ_DIR, f"{user_id}.json")

                if os.path.exists(butteriq_path):
                    os.remove(butteriq_path)

                    # Entferne auch aus dem Cache, falls vorhanden
                    if hasattr(client.butteriq_manager, 'user_data') and user_id in client.butteriq_manager.user_data:
                        del client.butteriq_manager.user_data[user_id]

                    await ctx.send(f"✅ ButterIQ-Daten für Benutzer {user_id} wurden gelöscht.")
                else:
                    await ctx.send(f"❌ Keine ButterIQ-Daten für Benutzer {user_id} gefunden.")

            except Exception as e:
                await ctx.send(f"❌ Fehler beim Löschen der ButterIQ-Daten: {str(e)}")

        elif subaction.lower() == "disable":
            # Deaktiviere das Tracking für einen bestimmten Benutzer
            if user_id is None:
                await ctx.send("❌ Bitte gib eine Benutzer-ID an!")
                return

            try:
                # Deaktiviere das Tracking
                client.butteriq_manager.disable_tracking(user_id)
                await ctx.send(f"✅ Tracking für Benutzer {user_id} wurde deaktiviert. Der Benutzer kann weiterhin Befehle ausführen, aber es werden keine neuen Informationen gespeichert.")
            except Exception as e:
                await ctx.send(f"❌ Fehler beim Deaktivieren des Trackings: {str(e)}")

        elif subaction.lower() == "enable":
            # Aktiviere das Tracking für einen bestimmten Benutzer
            if user_id is None:
                await ctx.send("❌ Bitte gib eine Benutzer-ID an!")
                return

            try:
                # Aktiviere das Tracking
                client.butteriq_manager.enable_tracking(user_id)
                await ctx.send(f"✅ Tracking für Benutzer {user_id} wurde aktiviert. Es werden wieder Informationen über den Benutzer gespeichert.")
            except Exception as e:
                await ctx.send(f"❌ Fehler beim Aktivieren des Trackings: {str(e)}")

        else:
            await ctx.send(f"❌ Unbekannte ButterIQ-Aktion: {subaction}")
            await ctx.send("Verfügbare Aktionen: list, show, add, update, delete, enable, disable")
