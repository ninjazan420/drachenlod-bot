# -*- coding: utf-8 -*-
import discord
from discord import app_commands
import json
import os
import random
import asyncio
from datetime import datetime, timedelta
import math

# --- CONFIGURATION ---
DATA_FILE = 'data/drachigotchis.json'
LOOP_TIME_MINUTES = 15  # Häufigere Updates für mehr Dynamik

# --- GAME DATA STRUCTURES ---

# ASCII Art & Emojis - Erweitert mit mehr Drachenlord-Sprüchen
DRACHIGOTCHI_ART = {
    'normal': "🐉 \"Etzala ein neuer Tag.\"",
    'happy': "🎉 \"Meddl on! Besser als wie man denkt!\"",
    'sad': "😢 \"Die Hater machen mich feddich.\"",
    'angry': "💢 \"Jetzt hab ich die Schnauze voll!\"",
    'hungry': "🍕 \"Ich könnt' etzala was verdrücken.\"",
    'dirty': "🛁 \"Zeit für ein Bad in der Tschechei.\"",
    'sleeping': "😴 \"Träume vom Schanzenfest...\"",
    'dead': "💀 \"Game Over, du Lellek.\"",
    'working': "💼 \"Arbeit, Arbeit... ABEID!\"",
    'rich': "🤑 \"Geld regiert die Welt!\"",
    'training': "💪 \"Stark wie ein Drache!\"",
    'defending': "🛡️ \"Die Schanze hält!\"",
    'exploring': "🗺️ \"Mal gucken, was draußen so los ist.\"",
    'questing': "📜 \"Ein Auftrag ist ein Auftrag!\"",
    'crafting': "🛠️ \"Da wird was zammegebrügelt.\"",
    'streaming': "📺 \"Meddl Loide! Willkommen im Stream!\"",
    'drunk': "🍺 \"Prost! Auf die Schanze!\"",
    'sick': "🤒 \"Mir geht's nimmer so gut...\"",
    'legendary': "⭐ \"Ich bin eine Legende geworden!\"",
    'broke': "💸 \"Kein Geld mehr... wie immer.\"",
    'famous': "🌟 \"Sogar das BKA kennt mich!\"",
    'homeless': "🏠 \"Ohne Schanze bin ich nichts...\"",
    'comeback': "🔥 \"2025 wird mein Jahr!\""
}

# Items, Resources, and Shop - Massiv erweitert
ITEMS = {
    # Food - Drachenlord-Style
    'mettbrötchen': {'type': 'food', 'name': 'Mettbrötchen', 'price': 5, 'hunger': 20, 'happiness': 5, 'description': 'Ein ordentliches Mettbrötchen.'},
    'tiefkühlpizza': {'type': 'food', 'name': 'Tiefkühlpizza', 'price': 8, 'hunger': 35, 'happiness': 10, 'description': 'Für den großen Hunger.'},
    'energy_drink': {'type': 'food', 'name': 'Energy Drink', 'price': 3, 'hunger': 5, 'happiness': 10, 'description': 'Gibt einen schnellen Schub.'},
    'döner': {'type': 'food', 'name': 'Döner', 'price': 7, 'hunger': 30, 'happiness': 15, 'description': 'Mit allem und scharf!'},
    'bier': {'type': 'food', 'name': 'Bier', 'price': 4, 'hunger': 5, 'happiness': 20, 'effect': {'drunk': True}, 'description': 'Prost auf die Schanze!'},
    'schnitzel': {'type': 'food', 'name': 'Schnitzel', 'price': 12, 'hunger': 50, 'happiness': 25, 'description': 'Wie bei Muttern.'},
    'currywurst': {'type': 'food', 'name': 'Currywurst', 'price': 6, 'hunger': 25, 'happiness': 12, 'description': 'Mit Pommes natürlich.'},
    'leberkäse': {'type': 'food', 'name': 'Leberkäse', 'price': 5, 'hunger': 22, 'happiness': 8, 'description': 'Bayerische Spezialität.'},
    
    # Tools & Gear - Drachenlord Equipment
    'meddl_hammer': {'type': 'gear', 'name': 'Meddl Hammer', 'price': 50, 'stats': {'strength': 2}, 'description': 'Ein mächtiger Hammer.'},
    'anti_hater_spray': {'type': 'consumable', 'name': 'Anti-Hater Spray', 'price': 25, 'effect': {'health': 20}, 'description': 'Schützt vor fiesen Kommentaren.'},
    'buttergolem': {'type': 'special', 'name': 'Buttergolem', 'price': 1000, 'happiness': 100, 'description': 'Ein treuer Freund und Helfer.'},
    'schanzenschild': {'type': 'gear', 'name': 'Schanzenschild', 'price': 200, 'stats': {'defense': 10}, 'description': 'Verteidigt die heilige Schanze.'},
    'drachenschwert': {'type': 'gear', 'name': 'Drachenschwert', 'price': 500, 'stats': {'strength': 15}, 'description': 'Das legendäre Schwert des Drachenlords.'},
    'streamer_setup': {'type': 'gear', 'name': 'Streamer Setup', 'price': 800, 'stats': {'charisma': 20}, 'description': 'Professionelles Streaming-Equipment.'},
    'ford_blu': {'type': 'vehicle', 'name': 'Ford Blu', 'price': 5000, 'stats': {'speed': 50}, 'description': 'Das legendäre blaue Auto.'},
    'führerschein': {'type': 'license', 'name': 'Führerschein', 'price': 2000, 'requirement': {'ford_blu': True}, 'description': 'Endlich wieder fahren!'},
    
    # Resources - Erweitert
    'holz': {'type': 'resource', 'name': 'Holz', 'price': 10, 'description': 'Einfaches Holz, zum Bauen und Basteln.'},
    'stein': {'type': 'resource', 'name': 'Stein', 'price': 15, 'description': 'Stabiler Stein.'},
    'eisen': {'type': 'resource', 'name': 'Eisen', 'price': 50, 'description': 'Wertvolles Eisenerz.'},
    'gold': {'type': 'resource', 'name': 'Gold', 'price': 200, 'description': 'Seltenes Gold für besondere Gegenstände.'},
    'drachenschuppen': {'type': 'resource', 'name': 'Drachenschuppen', 'price': 100, 'description': 'Magische Schuppen mit besonderen Kräften.'},
    'mett': {'type': 'resource', 'name': 'Mett', 'price': 8, 'description': 'Rohes Hackfleisch für Mettbrötchen.'},
    'pilze': {'type': 'resource', 'name': 'Pilze', 'price': 12, 'description': 'Frische Pilze aus dem Wald.'},

    # Crafted Items - Neue Rezepte
    'holzschild': {'type': 'gear', 'name': 'Holzschild', 'stats': {'defense': 5}, 'description': 'Ein einfacher Schild aus Holz.'},
    'verbesserte_axt': {'type': 'gear', 'name': 'Verbesserte Axt', 'stats': {'strength': 3}, 'description': 'Zum besseren Holzfällen.'},
    'goldener_thron': {'type': 'furniture', 'name': 'Goldener Thron', 'stats': {'happiness': 50}, 'description': 'Ein Thron würdig eines Drachenlords.'},
    'schanzenflagge': {'type': 'decoration', 'name': 'Schanzenflagge', 'stats': {'fame': 10}, 'description': 'Zeigt allen, wer hier der Boss ist.'},

    # Special Items - Legendäre Gegenstände
    'bka_anerkennung': {'type': 'achievement', 'name': 'BKA Anerkennung', 'price': 0, 'stats': {'fame': 100}, 'description': 'Sogar das BKA kennt dich!'},
    'mainstream_status': {'type': 'achievement', 'name': 'Mainstream Status', 'price': 0, 'stats': {'fame': 200}, 'description': 'Du bist Teil der deutschen Kultur!'},
    'comeback_ticket': {'type': 'special', 'name': 'Comeback Ticket', 'price': 10000, 'effect': {'comeback': True}, 'description': '2025 wird dein Jahr!'},

    # Consumables - Heilung und Buffs
    'aspirin': {'type': 'consumable', 'name': 'Aspirin', 'price': 5, 'effect': {'health': 15}, 'description': 'Gegen Kopfschmerzen.'},
    'kaffee': {'type': 'consumable', 'name': 'Kaffee', 'price': 3, 'effect': {'energy': 20}, 'description': 'Macht wach und munter.'},
    'motivationsbuch': {'type': 'consumable', 'name': 'Motivationsbuch', 'price': 20, 'effect': {'happiness': 30}, 'description': 'Für schwere Zeiten.'},
    'hater_blocker': {'type': 'consumable', 'name': 'Hater Blocker', 'price': 50, 'effect': {'defense_buff': 24}, 'description': 'Blockiert Hater für 24h.'}
}

# Crafting Recipes - Massiv erweitert
CRAFTING_RECIPES = {
    'holzschild': {'name': 'Holzschild', 'materials': {'holz': 10, 'stein': 2}, 'skill_req': {'crafting': 5}},
    'verbesserte_axt': {'name': 'Verbesserte Axt', 'materials': {'holz': 5, 'eisen': 3}, 'skill_req': {'crafting': 10}},
    'schanzenschild': {'name': 'Schanzenschild', 'materials': {'holz': 20, 'eisen': 10, 'drachenschuppen': 5}, 'skill_req': {'crafting': 25}},
    'drachenschwert': {'name': 'Drachenschwert', 'materials': {'eisen': 15, 'gold': 5, 'drachenschuppen': 10}, 'skill_req': {'crafting': 40}},
    'goldener_thron': {'name': 'Goldener Thron', 'materials': {'holz': 50, 'gold': 20, 'drachenschuppen': 15}, 'skill_req': {'crafting': 60}},
    'schanzenflagge': {'name': 'Schanzenflagge', 'materials': {'holz': 15, 'stein': 5}, 'skill_req': {'crafting': 20}},
    'mettbrötchen': {'name': 'Mettbrötchen', 'materials': {'mett': 1}, 'skill_req': {'crafting': 1}},
    'anti_hater_spray': {'name': 'Anti-Hater Spray', 'materials': {'drachenschuppen': 3, 'gold': 1}, 'skill_req': {'crafting': 30}},
    'streamer_setup': {'name': 'Streamer Setup', 'materials': {'eisen': 25, 'gold': 10}, 'skill_req': {'crafting': 50, 'charisma': 30}}
}

# Locations - Erweiterte Drachenlord-Welt basierend auf echter Lore
LOCATIONS = {
    'schanze': {
        'name': 'Die Schanze (Altschauerberg 8)', 
        'description': 'Dein legendäres Zuhause, die Drachenschanze in Altschauerberg. Hier fing alles an.', 
        'actions': ['schlafen', 'craften', 'streamen', 'verteidigen', 'tor_reparieren', 'bulldoghalle_aufräumen'], 
        'danger': 0,
        'shop': ['bier', 'pizza', 'energy_drink', 'poster', 'drachenlord_merch'],
        'special_events': ['hater_invasion', 'polizei_besuch', 'nachbar_beschwerde', 'schanzenfest']
    },
    'altschauerberg': {
        'name': 'Altschauerberg Dorf',
        'description': 'Das kleine 42-Einwohner Dorf um deine Schanze. Hier kennt dich jeder.',
        'actions': ['spazieren', 'nachbarn_besuchen', 'burgruine_erkunden', 'dorfklatsch'],
        'danger': 1,
        'shop': ['brot', 'milch', 'eier', 'dorfzeitung'],
        'special_events': ['dorfbewohner_treffen', 'wanderer_begegnung', 'eppala_besichtigung']
    },
    'emskirchen': {
        'name': 'Emskirchen',
        'description': 'Die Gemeinde die dein Haus gekauft hat. Hier ist das Rathaus und die Verwaltung.',
        'actions': ['rathaus_besuchen', 'shop', 'reden', 'quests_annehmen', 'kirche_besuchen'],
        'danger': 1,
        'shop': ['brot', 'wurst', 'käse', 'bier', 'zeitung', 'briefmarken', 'formulare']
    },
    'neustadt_aisch': {
        'name': 'Neustadt an der Aisch',
        'description': 'Deine Geburtsstadt mit Krankenhaus und wichtigen Behörden.',
        'actions': ['krankenhaus_besuchen', 'amt_besuchen', 'arbeiten', 'geburtshaus_besuchen'],
        'danger': 1,
        'shop': ['medikamente', 'formulare', 'bier', 'geburtsurkunde']
    },
    'nürnberg': {
        'name': 'Nürnberg',
        'description': 'Die große Stadt mit Radio Z, Gericht und MPU-Stelle.',
        'actions': ['radio_z_besuchen', 'gericht_besuchen', 'mpu_machen', 'arbeiten', 'fame_sammeln'],
        'danger': 2,
        'shop': ['laptop', 'handy', 'gaming_stuhl', 'energy_drink', 'kamera', 'mikrofon']
    },
    'wald': {
        'name': 'Fränkischer Wald',
        'description': 'Die Wälder um Altschauerberg. Hier kannst du dich verstecken und Ressourcen sammeln.',
        'actions': ['sammeln_holz', 'jagen', 'verstecken', 'pilze_sammeln', 'entspannen'],
        'danger': 3,
        'shop': []
    },
    'mine': {
        'name': 'Verlassene Mine',
        'description': 'Eine alte fränkische Mine, reich an Erzen und Geheimnissen.',
        'actions': ['abbauen_stein', 'abbauen_eisen', 'schätze_suchen', 'bergbau_lernen'],
        'danger': 4,
        'shop': []
    },
    'haider_lager': {
        'name': 'Haider-Lager',
        'description': 'Ein gefährliches Lager voller Haider und Trolle. Hier sammeln sie sich für Raids.',
        'actions': ['angreifen', 'infiltrieren', 'sabotieren', 'spionieren'],
        'danger': 8,
        'shop': []
    },
    'autobahn_a3': {
        'name': 'Autobahn A3',
        'description': 'Die Autobahn Richtung München und Würzburg - nur mit Führerschein!',
        'actions': ['fahren', 'trampen', 'raststätte_besuchen'],
        'danger': 2,
        'requirement': 'führerschein',
        'shop': ['benzin', 'snacks']
    },
    'bamberg': {
        'name': 'Bamberg',
        'description': 'Historische Bierstadt mit Universität und Kultur.',
        'actions': ['bier_trinken', 'studieren', 'kultur_erleben', 'dom_besuchen'],
        'danger': 1,
        'shop': ['rauchbier', 'bücher', 'souvenirs']
    },
    'würzburg': {
        'name': 'Würzburg',
        'description': 'Universitätsstadt am Main mit Residenz und Festung.',
        'actions': ['studieren', 'arbeiten', 'wein_trinken', 'festung_besuchen'],
        'danger': 1,
        'shop': ['frankenwein', 'bücher', 'laptop']
    },
    'münchen': {
        'name': 'München',
        'description': 'Die bayerische Hauptstadt voller Möglichkeiten und Medien.',
        'actions': ['oktoberfest', 'tv_auftritte', 'fame_sammeln', 'bier_trinken'],
        'danger': 1,
        'shop': ['weißbier', 'lederhose', 'tv_equipment']
    },
    'berlin': {
        'name': 'Berlin',
        'description': 'Die Hauptstadt - hier wirst du berühmt! BKA und Bundestag warten.',
        'actions': ['bka_besuchen', 'bundestag_besuchen', 'mainstream_werden', 'tv_shows'],
        'danger': 2,
        'shop': ['berliner_weisse', 'currywurst', 'politik_bücher']
    },
    'tschechei': {
        'name': 'Tschechien',
        'description': 'Das Nachbarland mit günstigen Bieren und entspannter Atmosphäre.',
        'actions': ['baden', 'bier_trinken', 'entspannen', 'grenze_überqueren'],
        'danger': 1,
        'shop': ['pilsner', 'knödel', 'souvenirs']
    },
    'internet': {
        'name': 'Das Internet',
        'description': 'Die digitale Welt voller Fans, Hater und Möglichkeiten. Hier bist du der Lord!',
        'actions': ['streamen', 'videos_machen', 'hater_bekämpfen', 'social_media', 'younow_streamen'],
        'danger': 5,
        'shop': ['premium_account', 'stream_equipment', 'bot_protection']
    }
}

# NPCs - Drachenlord-Universum Charaktere
NPCS = {
    'postbote': {'name': 'Postbote', 'dialogue': ["Ich hab ein Paket für dich!", "Unterschreiben Sie hier.", "Wieder Fanpost?"], 'location': 'schanze'},
    'wirt': {'name': 'Gastwirt', 'dialogue': ["Was darfs sein?", "Hör mal, ich hab da was für dich...", "Ein Bier für den Drachenlord?"], 'location': 'emskirchen'},
    'schmied': {'name': 'Schmied', 'dialogue': ["Heißes Eisen, kalter Stahl!", "Brauchst du was Ordentliches?", "Für den Drachenlord nur das Beste!"], 'location': 'emskirchen'},
    'uwe': {'name': 'Uwe', 'dialogue': ["Meddl Rainer!", "Wie läufts denn so?", "Brauchst du Hilfe?", "Die Hater nerven, oder?"], 'location': 'emskirchen'},
    'boneclinks': {'name': 'Boneclinks', 'dialogue': ["Du bist ein Versager!", "Haha, schau dir den an!", "Fake News!"], 'location': 'haider_lager', 'hostile': True},
    'ofenkäse': {'name': 'Der heilige Ofenkäse', 'dialogue': ["Alles Lügen!", "Ich verbreite nur die Wahrheit!", "Du bist am Ende!"], 'location': 'internet', 'hostile': True},
    'forstis_welt': {'name': 'Forstis Welt', 'dialogue': ["Ich berichte neutral!", "Die Wahrheit muss raus!", "Bleib stark, Rainer!"], 'location': 'internet', 'friendly': True},
    'bka_beamter': {'name': 'BKA Beamter', 'dialogue': ["Meddl Loide ist jetzt offiziell!", "Sie sind berühmt geworden!", "Respekt für Ihre Bekanntheit!"], 'location': 'berlin'},
    'mpu_prüfer': {'name': 'MPU Prüfer', 'dialogue': ["Sind Sie bereit für die Prüfung?", "Zeigen Sie mir Ihre Fortschritte!", "Das wird schwer..."], 'location': 'emskirchen'},
    'fan': {'name': 'Echter Fan', 'dialogue': ["Meddl Loide!", "Du bist der Beste!", "Lass dich nicht unterkriegen!", "Wann kommt das nächste Video?"], 'location': 'random'},
    'hater': {'name': 'Hater', 'dialogue': ["Du bist peinlich!", "Gib auf!", "Niemand mag dich!"], 'location': 'random', 'hostile': True},
    'tv_produzent': {'name': 'TV Produzent', 'dialogue': ["Wir wollen Sie in unserer Show!", "Sie sind ein Phänomen!", "Das wird ein Hit!"], 'location': 'münchen'},
    'polizist': {'name': 'Polizist', 'dialogue': ["Führerschein bitte!", "Fahren Sie vorsichtig!", "Alles in Ordnung?"], 'location': 'autobahn'}
}

# Quests - Epische Drachenlord-Abenteuer
QUESTS = {
    # Anfänger Quests
    'mett_quest': {'name': 'Die Mett-Mission', 'description': 'Der Wirt braucht 5 Mettbrötchen.', 'requirement': {'item': 'mettbrötchen', 'amount': 5}, 'reward': {'exp': 150, 'money': 50}, 'level_req': 1},
    'holz_quest': {'name': 'Schanzen-Vorbereitung', 'description': 'Sammle 20 Holz für den Schmied.', 'requirement': {'item': 'holz', 'amount': 20}, 'reward': {'exp': 200, 'item': 'verbesserte_axt'}, 'level_req': 5},
    
    # Mittlere Quests
    'hater_abwehr': {'name': 'Hater-Abwehr', 'description': 'Besiege 10 Hater um deine Schanze zu verteidigen.', 'requirement': {'kill': 'hater', 'amount': 10}, 'reward': {'exp': 500, 'item': 'anti_hater_spray', 'fame': 20}, 'level_req': 10},
    'führerschein_quest': {'name': 'Der Weg zum Führerschein', 'description': 'Bestehe die MPU und hole dir deinen Führerschein zurück.', 'requirement': {'action': 'mpu_bestehen'}, 'reward': {'exp': 1000, 'item': 'führerschein', 'happiness': 50}, 'level_req': 15},
    'ford_blu_quest': {'name': 'Der Ford Blu', 'description': 'Kaufe dir den legendären Ford Blu.', 'requirement': {'item': 'ford_blu', 'amount': 1}, 'reward': {'exp': 800, 'fame': 30}, 'level_req': 20},
    
    # Schwere Quests
    'boneclinks_kampf': {'name': 'Der Boneclinks-Kampf', 'description': 'Besiege den schlimmsten Hater aller Zeiten.', 'requirement': {'boss': 'boneclinks'}, 'reward': {'exp': 2000, 'money': 1000, 'fame': 100, 'item': 'drachenschwert'}, 'level_req': 25},
    'mainstream_quest': {'name': 'Mainstream werden', 'description': 'Erreiche 1000 Fame-Punkte und werde Teil der deutschen Kultur.', 'requirement': {'fame': 1000}, 'reward': {'exp': 3000, 'item': 'mainstream_status', 'money': 5000}, 'level_req': 30},
    'bka_anerkennung_quest': {'name': 'BKA Anerkennung', 'description': 'Besuche das BKA in Berlin und erhalte offizielle Anerkennung.', 'requirement': {'action': 'bka_besuchen'}, 'reward': {'exp': 2500, 'item': 'bka_anerkennung', 'fame': 200}, 'level_req': 35},
    
    # Legendäre Quests
    'comeback_2025': {'name': 'Das große Comeback 2025', 'description': 'Sammle alle legendären Items und starte dein episches Comeback.', 'requirement': {'items': ['drachenschwert', 'goldener_thron', 'mainstream_status', 'bka_anerkennung']}, 'reward': {'exp': 10000, 'item': 'comeback_ticket', 'fame': 500, 'money': 25000}, 'level_req': 50},
    'schanze_wiederaufbau': {'name': 'Wiederaufbau der Schanze', 'description': 'Baue die Schanze größer und besser wieder auf.', 'requirement': {'materials': {'holz': 500, 'stein': 300, 'eisen': 200, 'gold': 100}}, 'reward': {'exp': 5000, 'schanze_level': 10, 'fame': 300}, 'level_req': 40},
    
    # Tägliche Quests
    'daily_stream': {'name': 'Täglicher Stream', 'description': 'Streame heute für mindestens 2 Stunden.', 'requirement': {'action': 'streamen', 'duration': 2}, 'reward': {'exp': 100, 'money': 50, 'fame': 5}, 'daily': True},
    'daily_hater_fight': {'name': 'Hater des Tages', 'description': 'Besiege 3 Hater heute.', 'requirement': {'kill': 'hater', 'amount': 3}, 'reward': {'exp': 80, 'money': 30}, 'daily': True},
    'daily_craft': {'name': 'Tägliches Crafting', 'description': 'Stelle heute 5 Gegenstände her.', 'requirement': {'craft': 5}, 'reward': {'exp': 60, 'materials': 'random'}, 'daily': True}
}

# Jobs - Erweiterte Karrieremöglichkeiten
JOBS = {
    # Basis Jobs
    'holzfäller': {'name': 'Holzfäller', 'description': 'Du fällst Holz im Wald.', 'income': (10, 30), 'skill': 'strength', 'location': 'wald'},
    'wache': {'name': 'Wache', 'description': 'Du bewachst das Dorf.', 'income': (20, 40), 'skill': 'defense', 'location': 'emskirchen'},
    'streamer': {'name': 'Streamer', 'description': 'Du unterhältst die Massen.', 'income': (5, 60), 'skill': 'charisma', 'location': 'internet'},
    
    # Neue Jobs
    'youtuber': {'name': 'YouTuber', 'description': 'Du machst Videos für YouTube.', 'income': (20, 100), 'skill': 'charisma', 'location': 'internet', 'fame_bonus': 2},
    'twitch_streamer': {'name': 'Twitch Streamer', 'description': 'Live-Streaming auf Twitch.', 'income': (30, 150), 'skill': 'charisma', 'location': 'internet', 'fame_bonus': 3},
    'bergarbeiter': {'name': 'Bergarbeiter', 'description': 'Du arbeitest in der Mine.', 'income': (40, 80), 'skill': 'strength', 'location': 'mine'},
    'taxifahrer': {'name': 'Taxifahrer', 'description': 'Du fährst Taxi (braucht Führerschein).', 'income': (50, 120), 'skill': 'speed', 'location': 'nürnberg', 'requirement': 'führerschein'},
    'tv_moderator': {'name': 'TV Moderator', 'description': 'Du moderierst im Fernsehen.', 'income': (200, 500), 'skill': 'charisma', 'location': 'münchen', 'fame_bonus': 10, 'level_req': 25},
    'buchautor': {'name': 'Buchautor', 'description': 'Du schreibst Bücher über dein Leben.', 'income': (100, 300), 'skill': 'charisma', 'location': 'schanze', 'fame_bonus': 5},
    'konzert_künstler': {'name': 'Konzert Künstler', 'description': 'Du gibst Konzerte und singst.', 'income': (150, 400), 'skill': 'charisma', 'location': 'münchen', 'fame_bonus': 8, 'level_req': 20},
    'hater_jäger': {'name': 'Hater Jäger', 'description': 'Du bekämpfst professionell Hater.', 'income': (80, 200), 'skill': 'defense', 'location': 'internet', 'level_req': 15},
    'influencer': {'name': 'Influencer', 'description': 'Du beeinflusst die Massen.', 'income': (300, 1000), 'skill': 'charisma', 'location': 'internet', 'fame_bonus': 15, 'level_req': 30},
    'politiker': {'name': 'Politiker', 'description': 'Du gehst in die Politik.', 'income': (500, 1500), 'skill': 'charisma', 'location': 'berlin', 'fame_bonus': 20, 'level_req': 40}
}

# --- CORE CLASSES ---

class Drachigotchi:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.age = 0
        self.level = 1
        self.exp = 0
        self.health = 100
        self.hunger = 100
        self.happiness = 100
        self.energy = 100
        self.money = 50
        self.fame = 0
        self.inventory = {}
        self.equipment = {'weapon': None, 'shield': None, 'vehicle': None, 'license': None}
        self.schanze_level = 1
        self.location = 'schanze'
        self.active_quests = []
        self.completed_quests = []
        self.daily_quests_completed = []
        self.last_daily_reset = datetime.now().date()
        self.job = None
        self.job_hours_today = 0
        self.skills = {'strength': 1, 'defense': 1, 'charisma': 1, 'crafting': 1, 'gathering': 1, 'speed': 1, 'intelligence': 1}
        self.achievements = []
        self.relationships = {}  # NPC relationships
        self.buffs = {}  # Temporary buffs with expiration
        self.last_update = datetime.now()
        self.created_at = datetime.now()
        self.is_sleeping = False
        self.status = 'normal'
        self.stream_hours = 0
        self.total_haters_defeated = 0
        self.total_items_crafted = 0
        self.comeback_progress = 0
        self.has_führerschein = False
        self.mpu_attempts = 0
        self.mpu_passed = False

    def to_dict(self):
        import datetime as dt
        data = self.__dict__.copy()
        data['last_update'] = data['last_update'].isoformat()
        data['created_at'] = data['created_at'].isoformat()
        if isinstance(data.get('last_daily_reset'), dt.date):
            data['last_daily_reset'] = data['last_daily_reset'].isoformat()

        # Convert buffs datetime objects to strings
        if 'buffs' in data and data['buffs']:
            serialized_buffs = {}
            for stat, buff in data['buffs'].items():
                if isinstance(buff, dict) and 'expiry' in buff:
                    serialized_buffs[stat] = {
                        'value': buff['value'],
                        'expiry': buff['expiry'].isoformat() if hasattr(buff['expiry'], 'isoformat') else buff['expiry']
                    }
                else:
                    serialized_buffs[stat] = buff
            data['buffs'] = serialized_buffs

        return data

    @classmethod
    def from_dict(cls, data):
        instance = cls(data['user_id'], data['name'])
        for key, value in data.items():
            if key in ['last_update', 'created_at'] and value:
                setattr(instance, key, datetime.fromisoformat(value))
            elif key == 'last_daily_reset' and value:
                setattr(instance, key, datetime.fromisoformat(value).date())
            elif key == 'buffs' and value:
                # Convert buffs back from serialized format
                deserialized_buffs = {}
                for stat, buff in value.items():
                    if isinstance(buff, dict) and 'expiry' in buff:
                        deserialized_buffs[stat] = {
                            'value': buff['value'],
                            'expiry': datetime.fromisoformat(buff['expiry']) if isinstance(buff['expiry'], str) else buff['expiry']
                        }
                    else:
                        deserialized_buffs[stat] = buff
                setattr(instance, key, deserialized_buffs)
            else:
                setattr(instance, key, value)
        return instance

    def gain_exp(self, amount):
        self.exp += amount
        leveled_up = False
        while self.exp >= self.level * 100:
            self.exp -= self.level * 100
            self.level += 1
            # Distribute skill points on level up
            self.health = self.get_max_health()
            # Gain skill points
            for skill in self.skills:
                self.skills[skill] += 1
            leveled_up = True
        return leveled_up

    def get_max_health(self):
        return 100 + (self.level * 10)
    
    def get_max_energy(self):
        return 100 + (self.level * 5)
    
    def get_max_happiness(self):
        return 100 + (self.level * 5)

    def get_total_stat(self, stat):
        base_stat = self.skills.get(stat, 0)
        for item_name in self.equipment.values():
            if item_name and item_name in ITEMS:
                base_stat += ITEMS[item_name].get('stats', {}).get(stat, 0)
        # Apply buffs
        if stat in self.buffs:
            base_stat += self.buffs[stat].get('value', 0)
        return base_stat
    
    def add_buff(self, stat, value, duration_hours):
        """Fügt einen temporären Buff hinzu"""
        from datetime import timedelta
        expiry = datetime.now() + timedelta(hours=duration_hours)
        self.buffs[stat] = {'value': value, 'expiry': expiry}
    
    def clean_expired_buffs(self):
        """Entfernt abgelaufene Buffs"""
        now = datetime.now()
        expired = []
        for stat, buff in self.buffs.items():
            if isinstance(buff, dict) and 'expiry' in buff:
                expiry = buff['expiry']
                if hasattr(expiry, 'isoformat'):  # datetime object
                    if expiry < now:
                        expired.append(stat)
                elif isinstance(expiry, str):  # string format
                    try:
                        if datetime.fromisoformat(expiry) < now:
                            expired.append(stat)
                    except:
                        expired.append(stat)  # Remove invalid buffs

        for stat in expired:
            del self.buffs[stat]
    
    def reset_daily_quests(self):
        """Setzt tägliche Quests zurück"""
        today = datetime.now().date()
        if self.last_daily_reset < today:
            self.daily_quests_completed = []
            self.job_hours_today = 0
            self.last_daily_reset = today
    
    def can_do_action(self, action, location=None):
        """Prüft ob eine Aktion möglich ist"""
        if location and self.location != location:
            return False, f"Du musst in {LOCATIONS[location]['name']} sein!"
        
        if action == 'fahren' and not self.has_führerschein:
            return False, "Du brauchst einen Führerschein!"
        
        if self.energy < 10:
            return False, "Du bist zu müde!"
            
        return True, "OK"
    
    def update_status(self):
        """Aktualisiert den Status basierend auf Werten"""
        if self.health <= 0:
            self.status = 'dead'
        elif self.fame >= 1000:
            self.status = 'famous'
        elif self.fame >= 500:
            self.status = 'legendary'
        elif self.money <= 0:
            self.status = 'broke'
        elif self.happiness <= 20:
            self.status = 'sad'
        elif self.happiness >= 90:
            self.status = 'happy'
        elif self.hunger <= 20:
            self.status = 'hungry'
        elif self.energy <= 20:
            self.status = 'sleeping'
        elif 'drunk' in self.buffs:
            self.status = 'drunk'
        else:
            self.status = 'normal'

    def trigger_random_event(self):
        """Löst zufällige Events basierend auf Location und Status aus"""
        events = []

        # Location-basierte Events
        location_data = LOCATIONS.get(self.location, {})
        special_events = location_data.get('special_events', [])

        if special_events and random.random() < 0.3:  # 30% Chance für Location-Event
            event = random.choice(special_events)

            if event == 'hater_invasion' and self.location == 'schanze':
                if random.random() < 0.5:  # 50% Chance zu gewinnen
                    self.fame += 10
                    self.happiness += 5
                    events.append("🛡️ Du hast eine Hater-Invasion erfolgreich abgewehrt! (+10 Ruhm, +5 Glück)")
                else:
                    self.health -= 15
                    self.happiness -= 10
                    events.append("💥 Hater haben deine Schanze angegriffen! (-15 Gesundheit, -10 Glück)")

            elif event == 'polizei_besuch' and self.location == 'schanze':
                self.happiness -= 5
                events.append("🚔 Die Polizei war da wegen Lärmbeschwerde. (-5 Glück)")

            elif event == 'schanzenfest' and self.location == 'schanze':
                self.happiness += 20
                self.fame += 5
                events.append("🎉 Spontanes Schanzenfest! Die Fans feiern mit dir! (+20 Glück, +5 Ruhm)")

            elif event == 'dorfbewohner_treffen' and self.location == 'altschauerberg':
                if random.random() < 0.7:  # 70% positive Begegnung
                    self.happiness += 8
                    events.append("😊 Freundliche Begegnung mit Dorfbewohnern! (+8 Glück)")
                else:
                    self.happiness -= 5
                    events.append("😒 Unfreundliche Blicke von Dorfbewohnern. (-5 Glück)")

        # Status-basierte Events
        if self.status == 'hungry' and random.random() < 0.4:
            events.append("🍕 Du träumst von einem leckeren Mettbrötchen...")

        elif self.status == 'famous' and random.random() < 0.2:
            fan_money = random.randint(10, 50)
            self.money += fan_money
            events.append(f"💰 Ein Fan hat dir {fan_money}€ gespendet!")

        elif self.status == 'broke' and random.random() < 0.3:
            events.append("💸 Du überlegst, ob du wieder bei Mama anrufen sollst...")

        # Allgemeine zufällige Events
        if random.random() < 0.1:  # 10% Chance für seltene Events
            rare_events = [
                ("📺 Du wirst im Fernsehen erwähnt!", {'fame': 15, 'happiness': 10}),
                ("🎁 Ein Paket von einem Fan ist angekommen!", {'happiness': 12, 'money': 25}),
                ("🐉 Du fühlst dich besonders drachig heute!", {'energy': 20, 'happiness': 8}),
                ("📱 Dein Video geht viral!", {'fame': 30, 'money': 100}),
                ("🍺 Du findest eine vergessene Bierflasche!", {'happiness': 15}),
                ("💻 Dein PC läuft heute besonders gut!", {'energy': 10}),
                ("🎵 Du summst spontan ein Lied!", {'happiness': 5}),
                ("🌟 Du hast einen guten Tag!", {'happiness': 10, 'energy': 10})
            ]

            event_text, effects = random.choice(rare_events)
            events.append(event_text)

            for stat, value in effects.items():
                if stat == 'fame':
                    self.fame += value
                elif stat == 'happiness':
                    self.happiness = min(self.get_max_happiness(), self.happiness + value)
                elif stat == 'energy':
                    self.energy = min(self.get_max_energy(), self.energy + value)
                elif stat == 'money':
                    self.money += value
                elif stat == 'health':
                    self.health = min(self.get_max_health(), self.health + value)

        return events

class DrachigotchiManager:
    def __init__(self, file_path):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.drachigotchis = self.load()

    def load(self):
        if not os.path.exists(self.file_path):
            return {}
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                return {int(k): Drachigotchi.from_dict(v) for k, v in data.items()}
        except (json.JSONDecodeError, IOError):
            return {}

    def save(self):
        with open(self.file_path, 'w') as f:
            json.dump({k: v.to_dict() for k, v in self.drachigotchis.items()}, f, indent=4)

    def get_drachigotchi(self, user_id):
        return self.drachigotchis.get(user_id)

    def create_drachigotchi(self, user_id, name):
        if user_id in self.drachigotchis:
            return None
        drachigotchi = Drachigotchi(user_id, name)
        self.drachigotchis[user_id] = drachigotchi
        self.save()
        return drachigotchi

# --- DRACHIGOTCHI MANAGER INSTANCE --- #
drachigotchi_manager = None



def register_drachigotchi_commands(bot):
    """Registriert alle Drachigotchi Slash Commands"""
    global drachigotchi_manager
    drachigotchi_manager = DrachigotchiManager(DATA_FILE)

    # Import tasks for background loop
    from discord.ext import tasks

    @tasks.loop(minutes=LOOP_TIME_MINUTES)
    async def drachigotchi_background_task():
        """Background task that updates all drachigotchis every 15 minutes"""
        if not drachigotchi_manager:
            return

        try:
            updated_count = 0
            for user_id, drachi in drachigotchi_manager.drachigotchis.items():
                # Update stats and trigger events
                events = update_drachigotchi_stats(drachi)
                if events:  # If there were events, we updated something
                    updated_count += 1

            # Save all changes
            if updated_count > 0:
                drachigotchi_manager.save()
                print(f"🐉 Drachigotchi Background Task: {updated_count} Drachigotchis updated")

        except Exception as e:
            print(f"❌ Error in drachigotchi background task: {e}")

    # Store the background task on the bot instance so it can be started from main.py
    bot.drachigotchi_background_task = drachigotchi_background_task

    def is_admin(user_id: int) -> bool:
        """Prüft ob der User ein Admin ist"""
        return user_id == getattr(bot, 'admin_user_id', None)

    def update_drachigotchi_stats(drachi):
        """Update a single drachigotchi's stats (called on each interaction)"""
        now = datetime.now()

        # Clean expired buffs
        drachi.clean_expired_buffs()

        # Reset daily quests if needed
        drachi.reset_daily_quests()

        # Calculate time since last update
        time_diff = (now - drachi.last_update).total_seconds() / 3600  # hours

        if time_diff > 0.25:  # Only update if more than 15 minutes passed
            # Stats decay based on time passed
            decay_factor = min(time_diff / 4, 1)  # Max 1 hour of decay per update

            drachi.hunger = max(0, drachi.hunger - int(5 * decay_factor))
            drachi.happiness = max(0, drachi.happiness - int(4 * decay_factor))
            drachi.energy = min(drachi.get_max_energy(), drachi.energy + int(10 * decay_factor))

            # Health loss if hungry or unhappy
            if drachi.hunger == 0:
                drachi.health = max(0, drachi.health - int(5 * decay_factor))
            if drachi.happiness < 20:
                drachi.health = max(0, drachi.health - int(3 * decay_factor))

            # Trigger random events
            events = drachi.trigger_random_event()

            # Status Update & Aging
            drachi.age = (now - drachi.created_at).days
            drachi.update_status()
            drachi.last_update = now

            # Return events for potential display
            return events

        return []

    # Drachigotchi Command Group
    gotchi = app_commands.Group(name="gotchi", description="Dein persönliches Drachigotchi-Abenteuer!")

    # --- Core Commands ---
    @gotchi.command(name="hilfe", description="Zeigt eine Übersicht über das Drachigotchi-Spiel")
    async def hilfe(interaction: discord.Interaction):
        """Hilfe-Command für das Drachigotchi-Spiel"""
        embed = discord.Embed(
            title="🐉 Drachigotchi - Das ultimative Drachenlord-Abenteuer!",
            description="Erlebe das Leben als Drachenlord in diesem epischen Tamagotchi-Style Spiel!",
            color=0xffd700
        )

        embed.add_field(
            name="🎮 Grundlagen",
            value="• `/gotchi start <name>` - Erstelle dein Drachigotchi\n"
                  "• `/gotchi status` - Zeige deinen aktuellen Status\n"
                  "• `/gotchi inventar` - Schaue in dein Inventar\n"
                  "• Dein Drachigotchi braucht Essen, Schlaf und Aufmerksamkeit!",
            inline=False
        )

        embed.add_field(
            name="🍕 Überleben & Einkaufen",
            value="• `/gotchi essen` - Iss Essen aus deinem Inventar (Dropdown-Menü)\n"
                  "• `/gotchi kaufen` - Kaufe Items in lokalen Shops (Dropdown-Menü)\n"
                  "• `/gotchi shop` - Zeige verfügbare Items am aktuellen Ort\n"
                  "• Behalte Hunger, Gesundheit, Glück und Energie im Auge!",
            inline=False
        )

        embed.add_field(
            name="🗺️ Reisen & Abenteuer",
            value="• `/gotchi reisen` - Reise zu verschiedenen Orten (Dropdown-Menü)\n"
                  "• `/gotchi erkunden` - Erkunde deinen aktuellen Ort für Belohnungen\n"
                  "• `/gotchi hater_bekämpfen` - Kämpfe gegen Hater\n"
                  "• `/gotchi streamen` - Streame um Geld und Ruhm zu verdienen",
            inline=False
        )

        embed.add_field(
            name="📜 Quests & Fortschritt",
            value="• `/gotchi quests` - Zeige verfügbare und aktive Quests\n"
                  "• `/gotchi achievements` - Schaue deine Erfolge an\n"
                  "• `/gotchi arbeiten` - Arbeite in deinem Job um Geld zu verdienen\n"
                  "• `/gotchi craft` - Erstelle neue Items aus Materialien",
            inline=False
        )

        embed.add_field(
            name="🎯 Verwaltung & Sonstiges",
            value="• `/gotchi inventar` - Schaue in dein Inventar\n"
                  "• `/gotchi job` - Nimm Jobs an oder kündige\n"
                  "• `/gotchi ausrüsten` - Rüste Ausrüstung und Items aus\n"
                  "• `/gotchi freilassen` - Lass dein Drachigotchi frei (⚠️ permanent!)",
            inline=False
        )

        embed.add_field(
            name="🏆 Ziele & Erfolge",
            value="• Erreiche hohe Level und Skills\n"
                  "• Sammle Ruhm und werde berühmt\n"
                  "• Besiege legendäre Bosse wie Boneclinks\n"
                  "• Erreiche das große Comeback 2025!",
            inline=False
        )

        embed.add_field(
            name="💡 Tipps",
            value="• Dein Drachigotchi entwickelt sich auch wenn du offline bist\n"
                  "• Verschiedene Orte haben verschiedene Gefahren und Belohnungen\n"
                  "• Ausrüstung verbessert deine Stats erheblich\n"
                  "• Tägliche Quests geben extra Belohnungen",
            inline=False
        )

        embed.set_footer(text="Meddl Loide! Viel Spaß beim Drachigotchi-Abenteuer! 🐉")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @gotchi.command(name="start", description="Erstelle dein Drachigotchi.")
    async def start(interaction: discord.Interaction, name: str):
        if drachigotchi_manager.get_drachigotchi(interaction.user.id):
            return await interaction.response.send_message("Du hast bereits ein Drachigotchi!", ephemeral=True)
        drachigotchi_manager.create_drachigotchi(interaction.user.id, name)
        await interaction.response.send_message(f"🎉 Willkommen, {name}! Dein Abenteuer beginnt! Nutze `/gotchi hilfe` für eine Spielanleitung.", ephemeral=True)

    @gotchi.command(name="status", description="Zeigt den Status deines Drachigotchis.")
    async def status(interaction: discord.Interaction):
        drachi = drachigotchi_manager.get_drachigotchi(interaction.user.id)
        if not drachi: return await interaction.response.send_message("Starte erst mit `/gotchi start`.", ephemeral=True)

        # Update stats before showing status and get events
        events = update_drachigotchi_stats(drachi)

        # Get ASCII art for current status
        art = DRACHIGOTCHI_ART.get(drachi.status, DRACHIGOTCHI_ART['normal'])

        embed = discord.Embed(title=f"🐉 {drachi.name}", description=f"```{art}```", color=discord.Color.gold())
        embed.add_field(name="Level", value=f"{drachi.level} (EXP: {drachi.exp}/{drachi.level * 100})", inline=True)
        embed.add_field(name="Geld", value=f"{drachi.money}€", inline=True)
        embed.add_field(name="Ruhm", value=f"{drachi.fame}", inline=True)
        embed.add_field(name="Ort", value=LOCATIONS[drachi.location]['name'], inline=True)
        embed.add_field(name="Gesundheit", value=f"{drachi.health}/{drachi.get_max_health()}", inline=True)
        embed.add_field(name="Energie", value=f"{drachi.energy}/{drachi.get_max_energy()}", inline=True)
        embed.add_field(name="Hunger", value=f"{drachi.hunger}/100", inline=True)
        embed.add_field(name="Glück", value=f"{drachi.happiness}/{drachi.get_max_happiness()}", inline=True)
        embed.add_field(name="Alter", value=f"{drachi.age} Tage", inline=True)

        skills_text = "\n".join([f"{skill}: {level}" for skill, level in drachi.skills.items()])
        embed.add_field(name="Skills", value=skills_text, inline=False)

        # Show active buffs
        if drachi.buffs:
            buffs_text = "\n".join([f"{stat}: +{buff['value']}" for stat, buff in drachi.buffs.items()])
            embed.add_field(name="Aktive Buffs", value=buffs_text, inline=False)

        # Show equipment
        equipment_text = "\n".join([f"{slot}: {item or 'Nichts'}" for slot, item in drachi.equipment.items()])
        embed.add_field(name="Ausrüstung", value=equipment_text, inline=False)

        # Show recent events if any occurred
        if events:
            events_text = "\n".join(events[:3])  # Show max 3 events
            embed.add_field(name="📰 Aktuelle Ereignisse", value=events_text, inline=False)

        # Save after showing status
        drachigotchi_manager.save()

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @gotchi.command(name="inventar", description="Zeigt dein Inventar")
    async def inventar(interaction: discord.Interaction):
        drachi = drachigotchi_manager.get_drachigotchi(interaction.user.id)
        if not drachi:
            return await interaction.response.send_message("Starte erst mit `/gotchi start`.", ephemeral=True)

        if not drachi.inventory:
            return await interaction.response.send_message("Dein Inventar ist leer!", ephemeral=True)

        embed = discord.Embed(title=f"🎒 Inventar von {drachi.name}", color=0x0099ff)

        # Group items by type
        food_items = []
        tools_items = []
        resources_items = []
        other_items = []

        for item, count in drachi.inventory.items():
            if item in ITEMS:
                item_info = ITEMS[item]
                item_text = f"{item} x{count}"

                if item_info['type'] == 'food':
                    food_items.append(item_text)
                elif item_info['type'] in ['gear', 'tool']:
                    tools_items.append(item_text)
                elif item_info['type'] == 'resource':
                    resources_items.append(item_text)
                else:
                    other_items.append(item_text)

        if food_items:
            embed.add_field(name="🍕 Essen", value="\n".join(food_items), inline=True)
        if tools_items:
            embed.add_field(name="🔧 Werkzeuge", value="\n".join(tools_items), inline=True)
        if resources_items:
            embed.add_field(name="💎 Ressourcen", value="\n".join(resources_items), inline=True)
        if other_items:
            embed.add_field(name="📦 Sonstiges", value="\n".join(other_items), inline=True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @gotchi.command(name="essen", description="Eat food from your inventory")
    async def essen(interaction: discord.Interaction):
        drachi = drachigotchi_manager.get_drachigotchi(interaction.user.id)
        if not drachi:
            return await interaction.response.send_message("Start first with `/gotchi start`.", ephemeral=True)

        # Update stats before action
        update_drachigotchi_stats(drachi)

        # Get food items from inventory
        food_items = []
        for item, count in drachi.inventory.items():
            if item in ITEMS and ITEMS[item]['type'] == 'food' and count > 0:
                item_info = ITEMS[item]
                food_items.append((item, item_info, count))

        if not food_items:
            return await interaction.response.send_message("❌ You have no food in your inventory! Visit a shop to buy some.", ephemeral=True)

        # Create select menu for food items
        class FoodSelectView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)

            @discord.ui.select(
                placeholder="Choose food to eat...",
                min_values=1,
                max_values=1,
                options=[
                    discord.SelectOption(
                        label=f"{item_info.get('name', item)} (x{count})",
                        value=item,
                        description=f"🍽️ {item_info.get('description', 'No description')}",
                        emoji="🍕" if "pizza" in item else "🍺" if "bier" in item else "🥪"
                    ) for item, item_info, count in food_items[:25]  # Discord limit
                ]
            )
            async def food_select(self, select_interaction: discord.Interaction, select: discord.ui.Select):
                if select_interaction.user.id != interaction.user.id:
                    return await select_interaction.response.send_message("❌ This is not your menu!", ephemeral=True)

                selected_item = select.values[0]

                # Re-check inventory (in case it changed)
                if selected_item not in drachi.inventory or drachi.inventory[selected_item] <= 0:
                    return await select_interaction.response.send_message(f"❌ You no longer have {selected_item} in your inventory!")

                if selected_item not in ITEMS or ITEMS[selected_item]['type'] != 'food':
                    return await select_interaction.response.send_message(f"❌ {selected_item} is not edible!")

                item_info = ITEMS[selected_item]
                drachi.inventory[selected_item] -= 1
                if drachi.inventory[selected_item] <= 0:
                    del drachi.inventory[selected_item]

                # Apply food effects
                hunger_gain = item_info.get('hunger', 0)
                health_gain = item_info.get('health', 0)
                happiness_gain = item_info.get('happiness', 0)
                energy_gain = item_info.get('energy', 0)

                drachi.hunger = min(100, drachi.hunger + hunger_gain)
                drachi.health = min(drachi.get_max_health(), drachi.health + health_gain)
                drachi.happiness = min(drachi.get_max_happiness(), drachi.happiness + happiness_gain)
                drachi.energy = min(drachi.get_max_energy(), drachi.energy + energy_gain)

                # Special effects
                effects_text = []
                if 'effect' in item_info and 'drunk' in item_info['effect']:
                    drachi.add_buff('drunk', 1, 2)  # 2 hours drunk
                    effects_text.append("🍺 Du fühlst dich etwas beschwipst...")

                drachigotchi_manager.save()

                embed = discord.Embed(
                    title="🍽️ Mahlzeit!",
                    description=f"Du hast **{item_info.get('name', selected_item)}** gegessen!",
                    color=0x00ff00
                )

                stats_text = []
                if hunger_gain > 0:
                    stats_text.append(f"🍕 Hunger: +{hunger_gain}")
                if health_gain > 0:
                    stats_text.append(f"❤️ Gesundheit: +{health_gain}")
                if happiness_gain > 0:
                    stats_text.append(f"😊 Glück: +{happiness_gain}")
                if energy_gain > 0:
                    stats_text.append(f"⚡ Energie: +{energy_gain}")

                if stats_text:
                    embed.add_field(name="📊 Effekte", value="\n".join(stats_text), inline=False)

                if effects_text:
                    embed.add_field(name="✨ Spezialeffekte", value="\n".join(effects_text), inline=False)

                await select_interaction.response.edit_message(embed=embed, view=None)

        embed = discord.Embed(
            title="🍽️ Essen auswählen",
            description="Wähle ein Item aus deinem Inventar zum Verzehren:",
            color=0xffd700
        )

        view = FoodSelectView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @gotchi.command(name="quests", description="Zeigt verfügbare und aktive Quests")
    async def quests(interaction: discord.Interaction):
        drachi = drachigotchi_manager.get_drachigotchi(interaction.user.id)
        if not drachi:
            return await interaction.response.send_message("Starte erst mit `/gotchi start`.", ephemeral=True)

        drachi.reset_daily_quests()

        embed = discord.Embed(title=f"📜 Quests für {drachi.name}", color=0xffd700)

        # Active quests
        if drachi.active_quests:
            active_text = []
            for quest_id in drachi.active_quests:
                if quest_id in QUESTS:
                    quest = QUESTS[quest_id]
                    active_text.append(f"**{quest['name']}**\n{quest['description']}")
            if active_text:
                embed.add_field(name="🎯 Aktive Quests", value="\n\n".join(active_text), inline=False)

        # Available quests
        available_quests = []
        for quest_id, quest in QUESTS.items():
            if quest_id not in drachi.completed_quests and quest_id not in drachi.active_quests:
                # Check level requirement
                if quest.get('level_req', 0) <= drachi.level:
                    reward_text = f"Belohnung: {quest.get('exp', 0)} EXP, {quest.get('money', 0)}€"
                    if quest.get('item'):
                        reward_text += f", {quest['item']}"
                    available_quests.append(f"**{quest['name']}**\n{quest['description']}\n{reward_text}")

        if available_quests:
            embed.add_field(name="📋 Verfügbare Quests", value="\n\n".join(available_quests[:5]), inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @gotchi.command(name="quest_start", description="Starte eine Quest")
    async def quest_start(interaction: discord.Interaction, quest_name: str):
         drachi = drachigotchi_manager.get_drachigotchi(interaction.user.id)
         if not drachi:
             return await interaction.response.send_message("Starte erst mit `/gotchi start`.", ephemeral=True)

         # Find quest by name
         quest_id = None
         for qid, quest in QUESTS.items():
             if quest['name'].lower() == quest_name.lower():
                 quest_id = qid
                 break

         if not quest_id:
             return await interaction.response.send_message(f"Quest '{quest_name}' nicht gefunden!", ephemeral=True)

         quest = QUESTS[quest_id]

         # Check if already active or completed
         if quest_id in drachi.active_quests:
             return await interaction.response.send_message("Diese Quest ist bereits aktiv!", ephemeral=True)

         if quest_id in drachi.completed_quests:
             return await interaction.response.send_message("Diese Quest wurde bereits abgeschlossen!", ephemeral=True)

         # Check requirements
         if quest.get('level_req', 0) > drachi.level:
             return await interaction.response.send_message(f"Du brauchst Level {quest['level_req']} für diese Quest!", ephemeral=True)

         # Start quest
         drachi.active_quests.append(quest_id)
         drachigotchi_manager.save()

         embed = discord.Embed(title="📜 Quest gestartet!", description=f"**{quest['name']}**\n{quest['description']}", color=0x00ff00)
         await interaction.response.send_message(embed=embed, ephemeral=True)

    @gotchi.command(name="achievements", description="Zeigt deine Erfolge")
    async def achievements(interaction: discord.Interaction):
         drachi = drachigotchi_manager.get_drachigotchi(interaction.user.id)
         if not drachi:
             return await interaction.response.send_message("Starte erst mit `/gotchi start`.", ephemeral=True)

         embed = discord.Embed(title=f"🏆 Erfolge von {drachi.name}", color=0xffd700)

         if drachi.achievements:
             achievements_text = "\n".join([f"🏅 {achievement}" for achievement in drachi.achievements])
             embed.add_field(name="Errungene Erfolge", value=achievements_text, inline=False)
         else:
             embed.add_field(name="Errungene Erfolge", value="Noch keine Erfolge erzielt.", inline=False)

         # Show some stats
         embed.add_field(name="📊 Statistiken", value=f"Besiegte Hater: {drachi.total_haters_defeated}\nGecraftete Items: {drachi.total_items_crafted}\nStream-Stunden: {drachi.stream_hours}\nComeback-Fortschritt: {drachi.comeback_progress}%", inline=False)

         await interaction.response.send_message(embed=embed, ephemeral=True)

    @gotchi.command(name="streamen", description="Starte einen Stream")
    async def streamen(interaction: discord.Interaction, stunden: int = 1):
         drachi = drachigotchi_manager.get_drachigotchi(interaction.user.id)
         if not drachi:
             return await interaction.response.send_message("Starte erst mit `/gotchi start`.", ephemeral=True)

         if drachi.energy < stunden * 10:
             return await interaction.response.send_message(f"Du brauchst {stunden * 10} Energie zum Streamen!", ephemeral=True)

         if stunden > 8:
             return await interaction.response.send_message("Du kannst maximal 8 Stunden am Stück streamen!", ephemeral=True)

         # Stream effects
         drachi.energy -= stunden * 10
         drachi.hunger -= stunden * 5
         drachi.stream_hours += stunden

         # Income based on fame and skills
         base_income = stunden * 10
         fame_bonus = drachi.fame * 0.1
         skill_bonus = drachi.get_total_stat('charisma') * 2
         total_income = int(base_income + fame_bonus + skill_bonus)

         drachi.money += total_income
         drachi.fame += stunden * 2
         drachi.gain_exp(stunden * 15)

         # Random events during stream
         events = []
         if random.random() < 0.3:
             events.append("Ein Hater ist im Chat aufgetaucht!")
             drachi.happiness -= 5
         if random.random() < 0.2:
             donation = random.randint(5, 50)
             drachi.money += donation
             events.append(f"Du hast eine Spende von {donation}€ erhalten!")

         drachigotchi_manager.save()

         embed = discord.Embed(title=f"📺 {drachi.name} streamt {stunden} Stunden!", color=0xff6600)
         embed.add_field(name="Verdienst", value=f"{total_income}€", inline=True)
         embed.add_field(name="Ruhm", value=f"+{stunden * 2}", inline=True)
         embed.add_field(name="Erfahrung", value=f"+{stunden * 15}", inline=True)

         if events:
             embed.add_field(name="Stream-Events", value="\n".join(events), inline=False)

         await interaction.response.send_message(embed=embed, ephemeral=True)

    @gotchi.command(name="hater_bekämpfen", description="Bekämpfe einen Hater")
    async def hater_bekämpfen(interaction: discord.Interaction):
         drachi = drachigotchi_manager.get_drachigotchi(interaction.user.id)
         if not drachi:
             return await interaction.response.send_message("Starte erst mit `/gotchi start`.", ephemeral=True)

         if drachi.energy < 20:
             return await interaction.response.send_message("Du brauchst mindestens 20 Energie zum Kämpfen!", ephemeral=True)

         # Combat calculation
         player_power = drachi.get_total_stat('strength') + drachi.get_total_stat('charisma')
         hater_power = random.randint(10, 50)

         drachi.energy -= 20

         if player_power > hater_power:
             # Victory
             exp_gain = random.randint(20, 40)
             money_gain = random.randint(10, 30)
             fame_gain = random.randint(5, 15)

             drachi.gain_exp(exp_gain)
             drachi.money += money_gain
             drachi.fame += fame_gain
             drachi.total_haters_defeated += 1
             drachi.happiness += 10

             embed = discord.Embed(title="⚔️ Sieg gegen den Hater!", color=0x00ff00)
             embed.add_field(name="Belohnung", value=f"+{exp_gain} EXP\n+{money_gain}€\n+{fame_gain} Ruhm", inline=False)

             # Check for achievements
             if drachi.total_haters_defeated == 10 and "Hater-Schreck" not in drachi.achievements:
                 drachi.achievements.append("Hater-Schreck")
                 embed.add_field(name="🏆 Neuer Erfolg!", value="Hater-Schreck: 10 Hater besiegt!", inline=False)
         else:
             # Defeat
             health_loss = random.randint(10, 25)
             happiness_loss = random.randint(5, 15)

             drachi.health -= health_loss
             drachi.happiness -= happiness_loss

             embed = discord.Embed(title="💀 Niederlage gegen den Hater!", color=0xff0000)
             embed.add_field(name="Verluste", value=f"-{health_loss} Gesundheit\n-{happiness_loss} Glück", inline=False)

         drachigotchi_manager.save()
         await interaction.response.send_message(embed=embed, ephemeral=True)

     # --- Action Commands ---
    @gotchi.command(name="reisen", description="Reise zu einem neuen Ort.")
    @app_commands.describe(ort="Wähle dein Reiseziel")
    @app_commands.choices(ort=[
        app_commands.Choice(name="🏠 Die Schanze (Zuhause)", value="schanze"),
        app_commands.Choice(name="🌲 Emskirchener Wald", value="emskirchener_wald"),
        app_commands.Choice(name="🏪 Netto Markt", value="netto"),
        app_commands.Choice(name="🍺 Gasthof Sonne", value="gasthof_sonne"),
        app_commands.Choice(name="🏛️ Nürnberg", value="nürnberg"),
        app_commands.Choice(name="🚗 Autobahn A3", value="autobahn_a3"),
        app_commands.Choice(name="🍺 Bamberg", value="bamberg"),
        app_commands.Choice(name="🍷 Würzburg", value="würzburg"),
        app_commands.Choice(name="🏰 München", value="münchen"),
        app_commands.Choice(name="🌍 Tschechien", value="tschechei"),
        app_commands.Choice(name="💻 Internet", value="internet")
    ])
    async def reisen(interaction: discord.Interaction, ort: str):
        drachi = drachigotchi_manager.get_drachigotchi(interaction.user.id)
        if not drachi:
            return await interaction.response.send_message("Starte erst mit `/gotchi start`.", ephemeral=True)

        if ort not in LOCATIONS:
            return await interaction.response.send_message("Dieser Ort existiert nicht.", ephemeral=True)

        location_info = LOCATIONS[ort]

        # Check requirements
        if 'requirement' in location_info:
            req = location_info['requirement']
            if req == 'führerschein' and 'führerschein' not in drachi.inventory:
                return await interaction.response.send_message(f"❌ Du brauchst einen Führerschein um nach {location_info['name']} zu reisen!", ephemeral=True)

        # Travel costs energy
        travel_cost = 5 if ort != 'schanze' else 0
        if drachi.energy < travel_cost:
            return await interaction.response.send_message(f"❌ Du brauchst {travel_cost} Energie zum Reisen!", ephemeral=True)

        old_location = LOCATIONS[drachi.location]['name']
        drachi.location = ort
        drachi.energy = max(0, drachi.energy - travel_cost)

        drachigotchi_manager.save()

        embed = discord.Embed(
            title="🗺️ Reise abgeschlossen!",
            description=f"Du bist von **{old_location}** nach **{location_info['name']}** gereist",
            color=0x00ff00
        )
        embed.add_field(name="📍 Aktueller Ort", value=location_info['description'], inline=False)
        embed.add_field(name="⚡ Energiekosten", value=f"-{travel_cost} Energie", inline=True)
        embed.add_field(name="🎯 Verfügbare Aktionen", value=", ".join(location_info['actions']), inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @gotchi.command(name="erkunden", description="Erkunde deinen aktuellen Ort und finde Abenteuer!")
    async def erkunden(interaction: discord.Interaction):
        drachi = drachigotchi_manager.get_drachigotchi(interaction.user.id)
        if not drachi:
            return await interaction.response.send_message("Starte erst mit `/gotchi start`.", ephemeral=True)

        if drachi.energy < 10:
            return await interaction.response.send_message("❌ Du brauchst mindestens 10 Energie zum Erkunden!", ephemeral=True)

        location_info = LOCATIONS[drachi.location]
        drachi.energy -= 10

        # Base exploration results
        results = []
        rewards = {}

        # Location-specific exploration
        if drachi.location == 'schanze':
            events = [
                "Du findest alte Pizzakartons in der Ecke - klassische Schanze-Vibes!",
                "Du entdeckst einen versteckten Vorrat Energy Drinks hinter dem Sofa!",
                "Du räumst die Bulldoghalle auf und fühlst dich erfolgreich!",
                "Du checkst das Tor - alles scheint erstmal sicher zu sein.",
                "Du findest altes Streaming-Equipment das nützlich sein könnte."
            ]
            if random.random() < 0.3:
                rewards['energy_drink'] = 1
            if random.random() < 0.2:
                rewards['money'] = random.randint(5, 15)

        elif drachi.location == 'emskirchener_wald':
            events = [
                "Du findest Pilze die bei den Bäumen wachsen!",
                "Ein friedlicher Spaziergang durch die Natur stellt dein Glück wieder her.",
                "Du entdeckst eine versteckte Lichtung perfekt zum Meditieren.",
                "Du sammelst nützliche Kräuter und Pflanzen.",
                "Du siehst Wildtiere - die Natur ist wunderschön!"
            ]
            if random.random() < 0.4:
                rewards['pilze'] = random.randint(1, 3)
            if random.random() < 0.3:
                drachi.happiness += 10

        elif drachi.location == 'netto':
            events = [
                "Du durchstöberst die Gänge und findest gute Angebote!",
                "Die Kassiererin erkennt dich - lokaler Promi-Status!",
                "Du hilfst einer älteren Person beim Einkaufen.",
                "Du entdeckst ein neues Produkt das interessant aussieht.",
                "Du unterhältst dich mit anderen Kunden über lokale Neuigkeiten."
            ]
            if random.random() < 0.2:
                rewards['money'] = random.randint(2, 8)
            if random.random() < 0.3:
                drachi.fame += 1

        elif drachi.location == 'internet':
            events = [
                "Du entdeckst ein neues Meme-Format - virales Potenzial!",
                "Du interagierst mit deiner Community und gewinnst Follower!",
                "Du findest eine interessante Kollaborationsmöglichkeit.",
                "Du lernst neue Streaming-Techniken.",
                "Du wehrst erfolgreich einige Hater ab!"
            ]
            if random.random() < 0.4:
                drachi.fame += random.randint(2, 5)
            if random.random() < 0.2:
                rewards['money'] = random.randint(10, 25)

        else:
            # Generic exploration for other locations
            events = [
                f"Du erkundest {location_info['name']} und entdeckst etwas Interessantes!",
                "Du triffst freundliche Einheimische die Geschichten erzählen.",
                "Du findest einen malerischen Ort perfekt für Fotos.",
                "Du lernst etwas Neues über die lokale Kultur.",
                "Du erlebst ein kleines Abenteuer das deinen Tag erhellt!"
            ]
            if random.random() < 0.2:
                drachi.happiness += 5

        # Random skill-based bonuses
        if drachi.skills['gathering'] > 3 and random.random() < 0.3:
            bonus_items = ['bier', 'pizza', 'energy_drink']
            bonus_item = random.choice(bonus_items)
            rewards[bonus_item] = 1
            results.append(f"Deine Sammel-Skills haben dir geholfen {bonus_item} zu finden!")

        # Apply rewards
        for item, amount in rewards.items():
            if item == 'money':
                drachi.money += amount
                results.append(f"💰 {amount}€ gefunden!")
            else:
                drachi.inventory[item] = drachi.inventory.get(item, 0) + amount
                results.append(f"🎒 {amount}x {ITEMS.get(item, {}).get('name', item)} gefunden!")

        # Experience gain
        exp_gain = random.randint(5, 15)
        drachi.gain_exp(exp_gain)

        # Choose random event
        event_text = random.choice(events)

        drachigotchi_manager.save()

        embed = discord.Embed(
            title=f"🔍 Erkunde {location_info['name']}",
            description=event_text,
            color=0x00ff00
        )
        embed.add_field(name="⚡ Energiekosten", value="-10 Energie", inline=True)
        embed.add_field(name="✨ Erfahrung", value=f"+{exp_gain} EXP", inline=True)

        if results:
            embed.add_field(name="🎁 Belohnungen", value="\n".join(results), inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @gotchi.command(name="craft", description="Stelle neue Gegenstände her.")
    async def craft(interaction: discord.Interaction, gegenstand: str):
        drachi = drachigotchi_manager.get_drachigotchi(interaction.user.id)
        if not drachi or gegenstand not in CRAFTING_RECIPES:
            return await interaction.response.send_message("Dieses Rezept kennst du nicht.", ephemeral=True)

        rezept = CRAFTING_RECIPES[gegenstand]
        # Check materials
        for material, amount in rezept['materials'].items():
            if drachi.inventory.get(material, 0) < amount:
                return await interaction.response.send_message(f"Dir fehlt {amount - drachi.inventory.get(material, 0)}x {material}.", ephemeral=True)
        # Check skill
        for skill, level in rezept['skill_req'].items():
            if drachi.skills.get(skill, 0) < level:
                return await interaction.response.send_message(f"Dein {skill}-Skill ist zu niedrig (braucht {level}).", ephemeral=True)

        # Consume materials & grant item
        for material, amount in rezept['materials'].items():
            drachi.inventory[material] -= amount
        drachi.inventory[gegenstand] = drachi.inventory.get(gegenstand, 0) + 1
        drachi.gain_exp(25)
        drachigotchi_manager.save()
        await interaction.response.send_message(f"Du hast erfolgreich 1x {gegenstand} hergestellt!", ephemeral=True)

    # --- Economy Commands ---
    @gotchi.command(name="job", description="Nimm einen Job an oder kündige ihn.")
    async def job(interaction: discord.Interaction, aktion: str, job_name: str = None):
        drachi = drachigotchi_manager.get_drachigotchi(interaction.user.id)
        if not drachi: return await interaction.response.send_message("Starte erst mit `/gotchi start`.", ephemeral=True)

        if aktion == 'annehmen':
            if not job_name or job_name not in JOBS:
                return await interaction.response.send_message("Diesen Job gibt es nicht.", ephemeral=True)
            drachi.job = job_name
            drachigotchi_manager.save()
            await interaction.response.send_message(f"Du arbeitest jetzt als {JOBS[job_name]['name']}.", ephemeral=True)
        elif aktion == 'kündigen':
            drachi.job = None
            drachigotchi_manager.save()
            await interaction.response.send_message("Du bist jetzt arbeitslos.", ephemeral=True)
        else:
            await interaction.response.send_message("Ungültige Aktion. Wähle 'annehmen' oder 'kündigen'.", ephemeral=True)

    @gotchi.command(name="arbeiten", description="Gehe für 2 Stunden arbeiten.")
    async def arbeiten(interaction: discord.Interaction):
        drachi = drachigotchi_manager.get_drachigotchi(interaction.user.id)
        if not drachi or not drachi.job:
            return await interaction.response.send_message("Du hast keinen Job.", ephemeral=True)

        job_data = JOBS[drachi.job]
        skill_level = drachi.skills.get(job_data['skill'], 1)
        earnings = random.randint(*job_data['income']) + skill_level * 2

        drachi.money += earnings
        drachi.hunger = max(0, drachi.hunger - 10)
        drachi.happiness = max(0, drachi.happiness - 5)
        drachi.gain_exp(20)
        drachigotchi_manager.save()
        await interaction.response.send_message(f"Du hast 2 Stunden gearbeitet und {earnings}€ verdient.", ephemeral=True)



    
    @gotchi.command(name="ausrüsten")
    @app_commands.describe(item="Das Item, das du ausrüsten möchtest")
    async def ausrüsten(interaction: discord.Interaction, item: str):
        """Rüste ein Item aus deinem Inventar aus"""
        drachi = drachigotchi_manager.get_drachigotchi(interaction.user.id)
        if not drachi:
            await interaction.response.send_message("❌ Du hast noch keinen Drachigotchi! Nutze `/gotchi start`", ephemeral=True)
            return

        # Update stats before action
        update_drachigotchi_stats(drachi)

        if drachi.status == 'dead':
            await interaction.response.send_message("💀 Dein Drachigotchi ist tot!", ephemeral=True)
            return

        if item not in drachi.inventory or drachi.inventory[item] <= 0:
            await interaction.response.send_message(f"❌ Du hast kein {item} im Inventar!", ephemeral=True)
            return

        if item not in ITEMS:
            await interaction.response.send_message(f"❌ Unbekanntes Item: {item}", ephemeral=True)
            return

        item_info = ITEMS[item]
        if item_info['type'] not in ['gear', 'vehicle', 'license']:
            await interaction.response.send_message(f"❌ {item} kann nicht ausgerüstet werden!", ephemeral=True)
            return

        # Determine equipment slot
        if item_info['type'] == 'gear':
            slot = 'weapon' if 'strength' in item_info.get('stats', {}) else 'shield'
        elif item_info['type'] == 'vehicle':
            slot = 'vehicle'
        elif item_info['type'] == 'license':
            slot = 'license'
        else:
            slot = 'weapon'

        # Unequip current item if any
        if drachi.equipment.get(slot):
            old_item = drachi.equipment[slot]
            drachi.inventory[old_item] = drachi.inventory.get(old_item, 0) + 1

        # Equip new item
        drachi.equipment[slot] = item
        drachi.inventory[item] -= 1
        if drachi.inventory[item] <= 0:
            del drachi.inventory[item]

        # Special effects
        if item == 'führerschein':
            drachi.has_führerschein = True

        drachigotchi_manager.save()
        await interaction.response.send_message(
            f"⚔️ **{item} ausgerüstet!**\n"
            f"📊 Slot: {slot}\n"
            f"💪 Beschreibung: {item_info.get('description', 'Keine Beschreibung')}"
        )
    
    @gotchi.command(name="mpu")
    async def mpu(interaction: discord.Interaction):
        """Mache die MPU (Medizinisch-Psychologische Untersuchung)"""
        drachi = drachigotchi_manager.get_drachigotchi(interaction.user.id)
        if not drachi:
            await interaction.response.send_message("❌ Du hast noch keinen Drachigotchi! Nutze `/gotchi start`", ephemeral=True)
            return

        if drachi.status == 'dead':
            await interaction.response.send_message("💀 Dein Drachigotchi ist tot!", ephemeral=True)
            return

        if drachi.has_führerschein:
            await interaction.response.send_message("✅ Du hast bereits einen Führerschein!", ephemeral=True)
            return

        if drachi.location != 'nürnberg':
            await interaction.response.send_message("❌ Du musst in Nürnberg sein für die MPU!", ephemeral=True)
            return

        cost = 500 + (drachi.mpu_attempts * 200)  # Gets more expensive

        if drachi.money < cost:
            await interaction.response.send_message(f"❌ Du brauchst {cost}€ für die MPU!", ephemeral=True)
            return
        
        drachi.money -= cost
        drachi.mpu_attempts += 1
        
        # Success chance based on intelligence and charisma
        success_chance = min(0.8, 0.3 + (drachi.get_total_stat('intelligence') * 0.02) + (drachi.get_total_stat('charisma') * 0.01))
        
        if random.random() < success_chance:
            drachi.mpu_passed = True
            drachi.has_führerschein = True
            drachi.inventory['führerschein'] = drachi.inventory.get('führerschein', 0) + 1
            
            await interaction.response.send_message(
                f"🎉 **MPU bestanden!** 🎉\n"
                f"🚗 Du hast jetzt einen Führerschein!\n"
                f"💰 Kosten: {cost}€\n"
                f"📊 Versuch: {drachi.mpu_attempts}",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"❌ **MPU nicht bestanden!** ❌\n"
                f"💰 {cost}€ bezahlt\n"
                f"📊 Versuch: {drachi.mpu_attempts}\n"
                f"💡 Trainiere Intelligenz und Charisma für bessere Chancen!",
                ephemeral=True
            )
        
        drachigotchi_manager.save()
    
    @gotchi.command(name="shop")
    async def shop(interaction: discord.Interaction):
        """Zeige den Shop für deine aktuelle Location"""
        drachi = drachigotchi_manager.get_drachigotchi(interaction.user.id)
        if not drachi:
            await interaction.response.send_message("❌ Du hast noch keinen Drachigotchi! Nutze `/gotchi start`", ephemeral=True)
            return

        if drachi.status == 'dead':
            await interaction.response.send_message("💀 Dein Drachigotchi ist tot!", ephemeral=True)
            return

        location_info = LOCATIONS.get(drachi.location, {})
        shop_items = location_info.get('shop', [])

        if not shop_items:
            await interaction.response.send_message(f"🏪 Kein Shop in {drachi.location} verfügbar!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title=f"🏪 Shop - {drachi.location}",
            description=f"💰 Dein Geld: {drachi.money}€",
            color=0x00ff00
        )
        
        for item in shop_items:
            if item in ITEMS:
                item_info = ITEMS[item]
                price = item_info.get('price', 50)
                embed.add_field(
                    name=f"{item_info['name']} - {price}€",
                    value=f"{item_info.get('description', 'Kein Beschreibung')}\nTyp: {item_info['type']}",
                    inline=True
                )
        
        embed.set_footer(text="Nutze /gotchi kaufen <item> um zu kaufen")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @gotchi.command(name="kaufen", description="Buy items from the local shop")
    async def kaufen(interaction: discord.Interaction):
        """Buy items from the shop"""
        drachi = drachigotchi_manager.get_drachigotchi(interaction.user.id)
        if not drachi:
            await interaction.response.send_message("❌ Du hast noch kein Drachigotchi! Nutze `/gotchi start`", ephemeral=True)
            return

        if drachi.status == 'dead':
            await interaction.response.send_message("💀 Dein Drachigotchi ist tot!", ephemeral=True)
            return

        location_info = LOCATIONS.get(drachi.location, {})
        shop_items = location_info.get('shop', [])

        if not shop_items:
            await interaction.response.send_message(f"❌ Kein Shop verfügbar in {location_info.get('name', drachi.location)}!", ephemeral=True)
            return

        # Filter available items and create options
        available_items = []
        for item in shop_items:
            if item in ITEMS:
                item_info = ITEMS[item]
                price = item_info.get('price', 50)
                available_items.append((item, item_info, price))

        if not available_items:
            await interaction.response.send_message("❌ No items available in this shop!", ephemeral=True)
            return

        # Create select menu for shop items
        class ShopSelectView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)

            @discord.ui.select(
                placeholder="Choose item to buy...",
                min_values=1,
                max_values=1,
                options=[
                    discord.SelectOption(
                        label=f"{item_info.get('name', item)} - {price}€",
                        value=item,
                        description=f"💰 {price}€ | {item_info.get('description', 'No description')[:50]}",
                        emoji="🍕" if item_info['type'] == 'food' else "⚔️" if item_info['type'] == 'gear' else "🛠️"
                    ) for item, item_info, price in available_items[:25]  # Discord limit
                ]
            )
            async def shop_select(self, select_interaction: discord.Interaction, select: discord.ui.Select):
                if select_interaction.user.id != interaction.user.id:
                    return await select_interaction.response.send_message("❌ Das ist nicht dein Shop!", ephemeral=True)

                selected_item = select.values[0]

                # Re-check if item is still available
                if selected_item not in shop_items or selected_item not in ITEMS:
                    return await select_interaction.response.send_message(f"❌ {selected_item} ist nicht mehr verfügbar!", ephemeral=True)

                item_info = ITEMS[selected_item]
                price = item_info.get('price', 50)

                if drachi.money < price:
                    return await select_interaction.response.send_message(
                        f"❌ Du brauchst {price}€ für {item_info.get('name', selected_item)}! Du hast nur {drachi.money}€.", ephemeral=True
                    )

                drachi.money -= price
                drachi.inventory[selected_item] = drachi.inventory.get(selected_item, 0) + 1

                drachigotchi_manager.save()

                embed = discord.Embed(
                    title="🛒 Kauf abgeschlossen!",
                    description=f"Du hast **{item_info.get('name', selected_item)}** gekauft!",
                    color=0x00ff00
                )
                embed.add_field(name="💰 Bezahlter Preis", value=f"{price}€", inline=True)
                embed.add_field(name="💰 Verbleibendes Geld", value=f"{drachi.money}€", inline=True)
                embed.add_field(name="📦 Item-Typ", value=item_info['type'].title(), inline=True)
                embed.add_field(name="📝 Beschreibung", value=item_info.get('description', 'Keine Beschreibung'), inline=False)

                await select_interaction.response.edit_message(embed=embed, view=None)

        embed = discord.Embed(
            title=f"🏪 Shop - {location_info.get('name', drachi.location)}",
            description=f"💰 Dein Geld: {drachi.money}€\nWähle ein Item zum Kaufen:",
            color=0xffd700
        )

        view = ShopSelectView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @gotchi.command(name="freilassen", description="Lass dein Drachigotchi frei und beende das Spiel")
    async def freilassen(interaction: discord.Interaction):
        """Lass dein Drachigotchi frei - das löscht deine Speicherdaten!"""
        drachi = drachigotchi_manager.get_drachigotchi(interaction.user.id)
        if not drachi:
            await interaction.response.send_message("❌ Du hast kein Drachigotchi zum Freilassen!", ephemeral=True)
            return

        # Create confirmation view
        class ConfirmReleaseView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=30)

            @discord.ui.button(label="Ja, Freilassen", style=discord.ButtonStyle.danger, emoji="💔")
            async def confirm_release(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                if button_interaction.user.id != interaction.user.id:
                    return await button_interaction.response.send_message("❌ Das ist nicht deine Entscheidung!", ephemeral=True)

                # Delete the Drachigotchi
                del drachigotchi_manager.drachigotchis[interaction.user.id]
                drachigotchi_manager.save()

                farewell_messages = [
                    f"🌅 {drachi.name} spreads their wings and flies into the sunset...",
                    f"🚪 {drachi.name} walks through the portal to freedom, looking back one last time.",
                    f"🌟 {drachi.name} ascends to Drachigotchi heaven, finally at peace.",
                    f"🦋 {drachi.name} transforms into pure energy and becomes one with the universe.",
                    f"🏠 {drachi.name} returns to the Schanze in the sky, where all good Drachigotchis go."
                ]

                embed = discord.Embed(
                    title="💔 Lebewohl, lieber Freund",
                    description=random.choice(farewell_messages),
                    color=0x8b0000
                )
                embed.add_field(
                    name="📊 Finale Stats",
                    value=f"**Level:** {drachi.level}\n"
                          f"**Alter:** {drachi.age} Tage\n"
                          f"**Ruhm:** {drachi.fame}\n"
                          f"**Geld:** {drachi.money}€",
                    inline=True
                )
                embed.add_field(
                    name="🏆 Erfolge",
                    value=f"**Abgeschlossene Quests:** {len(drachi.completed_quests)}\n"
                          f"**Stream-Stunden:** {getattr(drachi, 'stream_hours', 0)}\n"
                          f"**Gewonnene Kämpfe:** {getattr(drachi, 'battles_won', 0)}",
                    inline=True
                )
                embed.set_footer(text="Danke fürs Spielen von Drachigotchi! Nutze /gotchi start für ein neues Abenteuer.")

                await button_interaction.response.edit_message(embed=embed, view=None)

            @discord.ui.button(label="Nein, Weiterspielen", style=discord.ButtonStyle.success, emoji="❤️")
            async def cancel_release(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                if button_interaction.user.id != interaction.user.id:
                    return await button_interaction.response.send_message("❌ Das ist nicht deine Entscheidung!", ephemeral=True)

                embed = discord.Embed(
                    title="❤️ Willkommen zurück!",
                    description=f"{drachi.name} freut sich, dass du bleiben möchtest! Das Abenteuer geht weiter...",
                    color=0x00ff00
                )
                embed.set_footer(text="Dein Drachigotchi ist sicher und gesund!")

                await button_interaction.response.edit_message(embed=embed, view=None)

        # Show confirmation dialog
        embed = discord.Embed(
            title="⚠️ Drachigotchi freilassen?",
            description=f"Bist du sicher, dass du **{drachi.name}** freilassen möchtest?\n\n"
                       "⚠️ **Diese Aktion kann nicht rückgängig gemacht werden!**\n"
                       "• Aller Fortschritt geht verloren\n"
                       "• Deine Speicherdaten werden gelöscht\n"
                       "• Du musst mit `/gotchi start` neu anfangen",
            color=0xff6b6b
        )
        embed.add_field(
            name="📊 Aktuelle Stats",
            value=f"**Level:** {drachi.level}\n"
                  f"**Alter:** {drachi.age} Tage\n"
                  f"**Geld:** {drachi.money}€",
            inline=True
        )

        view = ConfirmReleaseView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    # Add the gotchi group to the bot's command tree
    bot.tree.add_command(gotchi)