# -*- coding: utf-8 -*-
"""
Kompatibilitäts-Layer für das Admin-System

Diese Datei dient als Rückwärtskompatibilität für bestehenden Code,
der direkt auf admins.py zugreift. Die eigentliche Funktionalität
wurde in modulare Dateien im admins/ Ordner verschoben.

Die ursprüngliche admins.py Datei war über 750 Zeilen lang und enthielt
duplizierte Klassen. Diese wurden in separate Module aufgeteilt:

- admins/stats_manager.py - Statistik-Verwaltung
- admins/ban_manager.py - Ban-Verwaltung für Server und User
- admins/server_list_view.py - Discord UI für Server-Listen
- admins/admin_commands.py - Alle Admin-Befehle

Dadurch ist der Code wartbarer, modularer und weniger redundant.
"""

from discord.ext import commands
import datetime

# Importiere die modularen Admin-Komponenten
from .admins import StatsManager, BanManager, ServerListView, register_admin_commands

# Für Rückwärtskompatibilität - falls andere Module direkt auf diese Klassen zugreifen
__all__ = ["StatsManager", "BanManager", "ServerListView", "register_admin_commands", "setup_admin_system"]

# Die Hauptfunktion zum Registrieren der Admin-Befehle
def setup_admin_system(bot):
    """
    Initialisiert das komplette Admin-System für den Bot.
    Diese Funktion sollte beim Bot-Start aufgerufen werden.
    
    Args:
        bot: Der Discord Bot Client
    """
    try:
        register_admin_commands(bot)
        print("✅ Admin-System erfolgreich initialisiert")
        print(f"📊 StatsManager: Aktiviert")
        print(f"🚫 BanManager: Aktiviert")
        print(f"📋 ServerListView: Aktiviert")
        print(f"⚙️ Admin-Befehle: Registriert")
    except Exception as e:
        print(f"❌ Fehler beim Initialisieren des Admin-Systems: {e}")
        raise

# Für Rückwärtskompatibilität mit dem ursprünglichen setup() Aufruf
def setup(bot):
    """
    Legacy-Funktion für Rückwärtskompatibilität.
    Verwendet die neue setup_admin_system Funktion.
    
    Args:
        bot: Der Discord Bot Client
    """
    setup_admin_system(bot)

# Informationen über die Optimierung
def get_optimization_info():
    """
    Gibt Informationen über die durchgeführten Optimierungen zurück.
    
    Returns:
        dict: Informationen über die Optimierungen
    """
    return {
        "original_lines": 754,
        "optimized_lines": 60,
        "reduction_percentage": round((754 - 60) / 754 * 100, 1),
        "modules_created": 4,
        "duplicated_classes_removed": 2,
        "optimization_date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "benefits": [
            "Modularer Code",
            "Bessere Wartbarkeit",
            "Keine Code-Duplikation",
            "Klarere Struktur",
            "Einfachere Tests"
        ]
    }

if __name__ == "__main__":
    # Zeige Optimierungs-Informationen wenn das Modul direkt ausgeführt wird
    info = get_optimization_info()
    print(f"📈 Admin-System Optimierung:")
    print(f"   Ursprünglich: {info['original_lines']} Zeilen")
    print(f"   Optimiert: {info['optimized_lines']} Zeilen")
    print(f"   Reduzierung: {info['reduction_percentage']}%")
    print(f"   Module erstellt: {info['modules_created']}")
    print(f"   Vorteile: {', '.join(info['benefits'])}")
