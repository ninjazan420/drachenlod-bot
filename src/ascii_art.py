#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ASCII-Art für den Buttergolem Bot
# Wird für den neofetch-ähnlichen Stats-Befehl verwendet
# Inspiriert von Drachenlord/Shrek

BUTTERGOLEM_ASCII = r"""

                 .--.
                |o_o |
                |:_/ |
               //   \ \
              (|     | )
             /'\_   _/`\
             \___)=(___/

          BUTTERGOLEM BOT
"""

# Drachenlord/Shrek-inspirierte ASCII-Art
DRACHENLORD_ASCII = r"""

                 .--.
                |ò_ó |
                |:_/ |
               //   \ \
              (|     | )
             /'\_   _/`\
             \___)=(___/

          BUTTERGOLEM MEDDL
"""

# Verbesserte Drachenlord/Shrek-ASCII-Art
DRACHENLORD_SHREK_ASCII = r"""

                 .--.
                /ò_ó  \
                |:_/  |
               //     \\
              (|MEDDL |)
             /'\_   _/`\
             \___)=(___/

          BUTTERGOLEM DRACHE
"""

# Neofetch-Style System ASCII - KORRIGIERT für konsistente Zeilenlängen
NEOFETCH_ASCII = r"""

 ████████████████████████
██                      ██
██  ██████████████████  ██
██  ██              ██  ██
██  ██  ████████████  ██
██  ██  ██      ██  ██  ██
██  ██  ██  ██  ██  ██  ██
██  ██  ██  ██  ██  ██  ██
██  ██  ██      ██  ██  ██
██  ██  ████████████  ██
██  ██              ██  ██
██  ██████████████████  ██
██                      ██
  ████████████████████████

    BUTTERGOLEM SYSTEM
"""

# Minimalistisches ASCII für bessere Performance - KORRIGIERT
MINIMAL_ASCII = r"""

    ╭─────────────────╮
    │  ◉   ◉   ◉   ◉  │
    │                 │
    │   BUTTERGOLEM   │
    │      STATS      │
    │                 │
    ╰─────────────────╯
"""


# Einfache Drachenlord Emojis für Animation
SIMPLE_DRACHENLORD_FRAMES = [
    "🐉💨                                                    ",
    "  🐉💨                                                  ",
    "    🐉💨                                                ",
    "      🐉💨                                              ",
    "        🐉💨                                            ",
    "          🐉💨                                          ",
    "            🐉💨                                        ",
    "              🐉💨                                      ",
    "                🐉💨                                    ",
    "                  🐉💨                                  ",
    "                    🐉💨                                ",
    "                      🐉💨                              ",
    "                        🐉💨                            ",
    "                          🐉💨                          ",
    "                            🐉💨                        ",
    "                              🐉💨                      ",
    "                                🐉💨                    ",
    "                                  🐉💨                  ",
    "                                    🐉💨                ",
    "                                      🐉💨              "
]

# ANSI Farbcodes für Discord-Markdown
BLACK = "```ansi\n\u001b[30m"
RED = "```ansi\n\u001b[31m"
GREEN = "```ansi\n\u001b[32m"
YELLOW = "```ansi\n\u001b[33m"
BLUE = "```ansi\n\u001b[34m"
MAGENTA = "```ansi\n\u001b[35m"
CYAN = "```ansi\n\u001b[36m"
WHITE = "```ansi\n\u001b[37m"

# Helle Varianten
BRIGHT_BLACK = "```ansi\n\u001b[30;1m"
BRIGHT_RED = "```ansi\n\u001b[31;1m"
BRIGHT_GREEN = "```ansi\n\u001b[32;1m"
BRIGHT_YELLOW = "```ansi\n\u001b[33;1m"
BRIGHT_BLUE = "```ansi\n\u001b[34;1m"
BRIGHT_MAGENTA = "```ansi\n\u001b[35;1m"
BRIGHT_CYAN = "```ansi\n\u001b[36;1m"
BRIGHT_WHITE = "```ansi\n\u001b[37;1m"

# Hintergrundfarben
BG_BLACK = "\u001b[40m"
BG_RED = "\u001b[41m"
BG_GREEN = "\u001b[42m"
BG_YELLOW = "\u001b[43m"
BG_BLUE = "\u001b[44m"
BG_MAGENTA = "\u001b[45m"
BG_CYAN = "\u001b[46m"
BG_WHITE = "\u001b[47m"

# Reset-Code
RESET = "\u001b[0m```"

# Erweiterte Farbpalette für bessere Neofetch-Experience
NEON_COLORS = {
    "neon_pink": "```ansi\n\u001b[38;5;201m",
    "neon_green": "```ansi\n\u001b[38;5;46m",
    "neon_blue": "```ansi\n\u001b[38;5;51m",
    "neon_orange": "```ansi\n\u001b[38;5;208m",
    "neon_purple": "```ansi\n\u001b[38;5;129m",
    "electric_blue": "```ansi\n\u001b[38;5;39m",
    "hot_pink": "```ansi\n\u001b[38;5;198m",
    "lime_green": "```ansi\n\u001b[38;5;118m"
}

# Gradient-Farben für Regenbogen-Effekte
RAINBOW_COLORS = [
    "```ansi\n\u001b[38;5;196m",  # Rot
    "```ansi\n\u001b[38;5;208m",  # Orange
    "```ansi\n\u001b[38;5;226m",  # Gelb
    "```ansi\n\u001b[38;5;46m",   # Grün
    "```ansi\n\u001b[38;5;51m",   # Cyan
    "```ansi\n\u001b[38;5;21m",   # Blau
    "```ansi\n\u001b[38;5;129m",  # Lila
    "```ansi\n\u001b[38;5;201m"   # Magenta
]

# Liste aller Vordergrundfarben für Animation
ALL_COLORS = [
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE,
    BRIGHT_BLACK, BRIGHT_RED, BRIGHT_GREEN, BRIGHT_YELLOW,
    BRIGHT_BLUE, BRIGHT_MAGENTA, BRIGHT_CYAN, BRIGHT_WHITE
] + list(NEON_COLORS.values()) + RAINBOW_COLORS

# Liste aller Hintergrundfarben für Animation
ALL_BG_COLORS = [
    BG_BLACK, BG_RED, BG_GREEN, BG_YELLOW,
    BG_BLUE, BG_MAGENTA, BG_CYAN, BG_WHITE
]

def get_colored_ascii(color="blue", style="buttergolem"):
    """Returns ASCII art with the specified color and style."""
    import random

    # Wähle ASCII-Art basierend auf Stil
    if style.lower() == "drachenlord":
        ascii_art = DRACHENLORD_ASCII
    elif style.lower() == "shrek":
        ascii_art = DRACHENLORD_SHREK_ASCII
    elif style.lower() == "neofetch" or style.lower() == "system":
        ascii_art = NEOFETCH_ASCII
    elif style.lower() == "minimal":
        ascii_art = MINIMAL_ASCII
    else:
        ascii_art = BUTTERGOLEM_ASCII

    # Erweiterte Farbauswahl
    color_lower = color.lower()

    # Spezielle Effekte
    if color_lower in ["drachenlord", "random", "rainbow"]:
        if color_lower == "rainbow":
            return get_rainbow_ascii(ascii_art)
        else:
            random_color = random.choice(RAINBOW_COLORS)
            return f"{random_color}{ascii_art}{RESET}"

    # Neon-Farben
    elif color_lower in NEON_COLORS:
        return f"{NEON_COLORS[color_lower]}{ascii_art}{RESET}"

    # Standard-Farben
    elif color_lower == "blue":
        return f"{BRIGHT_BLUE}{ascii_art}{RESET}"
    elif color_lower == "green":
        return f"{BRIGHT_GREEN}{ascii_art}{RESET}"
    elif color_lower == "yellow":
        return f"{BRIGHT_YELLOW}{ascii_art}{RESET}"
    elif color_lower == "red":
        return f"{BRIGHT_RED}{ascii_art}{RESET}"
    elif color_lower == "cyan":
        return f"{BRIGHT_CYAN}{ascii_art}{RESET}"
    elif color_lower == "magenta":
        return f"{BRIGHT_MAGENTA}{ascii_art}{RESET}"
    elif color_lower == "white":
        return f"{BRIGHT_WHITE}{ascii_art}{RESET}"
    elif color_lower in ["shrek", "bright_green"]:
        return f"{BRIGHT_GREEN}{ascii_art}{RESET}"
    elif color_lower == "gradient":
        return get_gradient_ascii(ascii_art)
    else:
        # Fallback: Verwende zufällige Neon-Farbe
        random_neon = random.choice(list(NEON_COLORS.values()))
        return f"{random_neon}{ascii_art}{RESET}"

def get_animated_frame(frame_num):
    """
    Gibt einen Frame der animierten ASCII-Art zurück
    """
    # Wähle Farben basierend auf dem Frame-Index
    fg_color = ALL_COLORS[frame_num % len(ALL_COLORS)]
    bg_color = ALL_BG_COLORS[(frame_num // 2) % len(ALL_BG_COLORS)]

    # Wechsle zwischen den ASCII-Arts basierend auf dem Frame
    if frame_num % 3 == 0:
        ascii_art = BUTTERGOLEM_ASCII
    elif frame_num % 3 == 1:
        ascii_art = DRACHENLORD_ASCII
    else:
        ascii_art = DRACHENLORD_SHREK_ASCII

    # Entferne den Markdown-Anfang vom Farbcode, da wir ihn nur einmal brauchen
    fg_color_code = fg_color.replace("```ansi\n", "")

    # Kombiniere Vordergrund- und Hintergrundfarbe
    return f"```ansi\n{fg_color_code}{bg_color}{ascii_art}{RESET}"

def get_gradient_ascii(ascii_art=None):
    """
    Erstellt eine ASCII-Art mit Farbverlauf für jede Zeile
    """
    if ascii_art is None:
        ascii_art = DRACHENLORD_SHREK_ASCII

    lines = ascii_art.strip().split('\n')
    gradient_colors = RAINBOW_COLORS

    # Erstelle den Farbverlauf
    colored_lines = []
    for i, line in enumerate(lines):
        color = gradient_colors[i % len(gradient_colors)]
        # Entferne den Markdown-Anfang vom Farbcode
        color_code = color.replace("```ansi\n", "")
        colored_lines.append(f"{color_code}{line}\n")

    # Füge alle Zeilen zusammen und stelle sicher, dass die Backticks korrekt gesetzt sind
    return f"```ansi\n{''.join(colored_lines)}\u001b[0m```"
    

def get_rainbow_ascii(ascii_art):
    """Erstellt eine ASCII-Art mit Regenbogen-Effekt"""
    lines = ascii_art.strip().split('\n')

    # Erstelle Regenbogen-Effekt
    colored_lines = []
    for i, line in enumerate(lines):
        color = RAINBOW_COLORS[i % len(RAINBOW_COLORS)]
        color_code = color.replace("```ansi\n", "")
        colored_lines.append(f"{color_code}{line}\n")

    return f"```ansi\n{''.join(colored_lines)}\u001b[0m```"

def get_animated_ascii_frame(frame_num, ascii_art=None):
    """Erstellt einen animierten Frame mit wechselnden Farben"""
    if ascii_art is None:
        ascii_art = BUTTERGOLEM_ASCII

    # Stelle sicher, dass RAINBOW_COLORS nicht leer ist
    if not RAINBOW_COLORS:
        return f"```\n{ascii_art}```"
        
    # Wähle Farbe basierend auf Frame-Nummer
    color = RAINBOW_COLORS[frame_num % len(RAINBOW_COLORS)]
    color_code = color.replace("```ansi\n", "")

    return f"```ansi\n{color_code}{ascii_art}\u001b[0m```"

def get_rainbow_animation_frames(num_frames=8):
    """Erstellt eine Liste von Frames für eine Regenbogen-Animation"""
    frames = []
    # Stelle sicher, dass num_frames positiv ist
    num_frames = max(1, num_frames)
    
    # Stelle sicher, dass RAINBOW_COLORS nicht leer ist
    if not RAINBOW_COLORS:
        # Fallback, falls RAINBOW_COLORS leer ist
        return ["```\nBUTTERGOLEM ANIMATION```" for _ in range(num_frames)]
        
    for i in range(num_frames):
        frames.append(get_animated_frame(i))
    return frames

def get_drachenlord_quote():
    """Gibt ein zufälliges Drachenlord-Zitat zurück"""
    import random
    quotes = [
        "Meddl Loide!",
        "Ich bin der Drache und ihr seid die kaschber!",
        "Ich hab nix gemacht, ich hab nur Selbstverteidigung gemacht!",
        "Ich bin der Buttergolem!",
        "Ich bin der Drachenlord von Altschauerberg!",
        "Ich bin nich derjeniche!",
        "Ich bin unbesigbar!",
        "Ich hab 53er IQ, ihr Kaggnazis!",
        "Ich bin viel intelligenter wie als ihr denkt!",
        "Ich bin ein Internetstar!",
        "Ich bin ein Schwerverbrecher!",
        "Ich bin ein Oger!",
        "Ich bin ein Kaschber!",
        "Ich bin ein Kagghaider!",
        "Ich bin ein Kaggduscher!",
        "Ich bin ein Kaggduschne!"
    ]
    return random.choice(quotes)

def get_system_info():
    """Gibt Systeminformationen für den Stats-Befehl zurück"""
    try:
        # Vereinfachte Version ohne Hardware-Informationen
        return {
            "uptime_days": 0  # Wird nicht mehr verwendet
        }
    except Exception as e:
        print(f"Fehler beim Abrufen der Systeminformationen: {e}")
        return {
            "uptime_days": 0  # Wird nicht mehr verwendet
        }

def format_stats_with_ascii(stats_text, animation_type="static"):
    """
    Formatiert die Statistiken mit ASCII-Art für den Stats-Befehl im neofetch-Stil
    mit ASCII-Art links und Statistiken rechts

    Args:
        stats_text (str): Der Text mit den Statistiken
        animation_type (str): Art der Animation ("gradient", "drachenlord", "shrek", "static")

    Returns:
        str: Formatierter Text mit ASCII-Art und Statistiken im neofetch-Stil
    """
    import random

    # Wähle die ASCII-Art basierend auf dem Animationstyp
    if animation_type == "gradient":
        ascii_art = get_gradient_ascii()
    elif animation_type == "drachenlord":
        # Für Drachenlord immer eine zufällige Farbe verwenden
        random_color = random.choice([BRIGHT_RED, BRIGHT_GREEN, BRIGHT_YELLOW, BRIGHT_BLUE, BRIGHT_MAGENTA, BRIGHT_CYAN])
        ascii_art = f"{random_color}{DRACHENLORD_SHREK_ASCII}{RESET}"
    elif animation_type == "shrek":
        ascii_art = f"{BRIGHT_GREEN}{DRACHENLORD_SHREK_ASCII}{RESET}"
    elif animation_type == "random":
        # Wähle eine zufällige Farbe und ASCII-Art
        random_color = random.choice([BRIGHT_RED, BRIGHT_GREEN, BRIGHT_YELLOW, BRIGHT_BLUE, BRIGHT_MAGENTA, BRIGHT_CYAN])
        ascii_art = f"{random_color}{DRACHENLORD_SHREK_ASCII}{RESET}"
    else:
        # Wähle eine zufällige Farbe für die Standard-Anzeige
        random_color = random.choice([BRIGHT_RED, BRIGHT_GREEN, BRIGHT_YELLOW, BRIGHT_BLUE, BRIGHT_MAGENTA, BRIGHT_CYAN])
        ascii_art = f"{random_color}{DRACHENLORD_SHREK_ASCII}{RESET}"

    # Extrahiere die ASCII-Art-Zeilen ohne die Backticks und ANSI-Codes
    if "```ansi" in ascii_art:
        # Entferne die Backticks und ANSI-Codes für die Verarbeitung
        clean_ascii = ascii_art.replace("```ansi\n", "")
        # Behalte den Farbcode am Anfang
        color_code = clean_ascii[:clean_ascii.find('m')+1]
        # Entferne den Farbcode vom Anfang
        clean_ascii = clean_ascii[clean_ascii.find('m')+1:]
        # Entferne den Reset-Code und die schließenden Backticks
        clean_ascii = clean_ascii.replace(RESET, "")
    else:
        # Falls keine ANSI-Codes vorhanden sind
        clean_ascii = ascii_art.replace("```", "")
        color_code = "\u001b[34;1m"  # Standard: Hellblau

    # Teile die ASCII-Art in Zeilen auf
    # Verwende split ohne strip, um die leere Zeile am Anfang zu behalten
    ascii_lines = clean_ascii.split('\n')

    # Teile die Statistiken in Zeilen auf
    stats_lines = stats_text.strip().split('\n')

    # Berechne die maximale Länge der ASCII-Art-Zeilen für die Ausrichtung
    # Ignoriere leere Zeilen bei der Berechnung der maximalen Länge
    max_ascii_length = max((len(line) for line in ascii_lines if line.strip()), default=0)

    # Füge Padding hinzu, um sicherzustellen, dass genug Platz zwischen ASCII und Stats ist
    padding = 4  # Anzahl der Leerzeichen zwischen ASCII und Stats

    # Erstelle die formatierte Ausgabe im neofetch-Stil
    formatted_output = "```ansi\n"  # Starte mit den Backticks

    # Bestimme die maximale Anzahl von Zeilen (entweder ASCII oder Stats)
    max_lines = max(len(ascii_lines), len(stats_lines))

    # Kombiniere ASCII-Art und Statistiken nebeneinander
    for i in range(max_lines):
        line = ""

        # Füge ASCII-Art hinzu, wenn verfügbar
        if i < len(ascii_lines):
            # Füge den Farbcode für die ASCII-Art hinzu
            ascii_line = f"{color_code}{ascii_lines[i]}"
            line += ascii_line

            # Füge Padding hinzu, um die Statistiken auszurichten
            padding_needed = max_ascii_length - len(ascii_lines[i]) + padding
            line += " " * padding_needed
        else:
            # Wenn keine ASCII-Art mehr vorhanden ist, füge Leerzeichen hinzu
            line += " " * (max_ascii_length + padding)

        # Füge Statistiken hinzu, wenn verfügbar
        if i < len(stats_lines):
            # Füge Cyan-Farbe für die Statistiken hinzu
            stats_line = f"\u001b[36;1m{stats_lines[i]}"
            line += stats_line

        formatted_output += f"{line}\n"

    # Füge den Reset-Code und die schließenden Backticks hinzu
    formatted_output += "\u001b[0m```"

    return formatted_output

def create_simple_neofetch(stats_text, color="blue"):
    """Erstellt eine einfache, funktionierende neofetch-style ausgabe"""
    import random

    # Einfache ASCII-Art
    simple_ascii = r"""
    ╭─────────────╮
    │  ◉   ◉   ◉  │
    │             │
    │ BUTTERGOLEM │
    │    STATS    │
    ╰─────────────╯
    """

    # Farbauswahl
    if color == "rainbow":
        color_code = random.choice(RAINBOW_COLORS).replace("```ansi\n", "")
    elif color in NEON_COLORS:
        color_code = NEON_COLORS[color].replace("```ansi\n", "")
    else:
        color_code = "\u001b[34;1m"  # Blau als fallback

    # Kombiniere ASCII und Stats
    ascii_lines = simple_ascii.strip().split('\n')
    stats_lines = stats_text.strip().split('\n')

    result = "```ansi\n"
    max_lines = max(len(ascii_lines), len(stats_lines))

    for i in range(max_lines):
        line = ""

        # ASCII-Art hinzufügen
        if i < len(ascii_lines):
            line += f"{color_code}{ascii_lines[i]:<20}"
        else:
            line += " " * 20

        # Stats hinzufügen
        if i < len(stats_lines):
            line += f"\u001b[36;1m{stats_lines[i]}"

        result += f"{line}\n"

    result += "\u001b[0m```"
    return result







def format_stats_with_ascii_color(stats_text, animation_type="static", color="blue"):
    """
    Formatiert die Statistiken mit ASCII-Art im neofetch-Stil mit Farbauswahl
    VEREINFACHT für bessere Funktionalität
    """
    # Stelle sicher, dass die Farbe gültig ist
    if color not in NEON_COLORS and color not in ["blue", "green", "yellow", "red", "cyan", "magenta", "white", "rainbow"]:
        color = "blue"  # Fallback auf Blau, wenn Farbe ungültig
        
    # Verwende die einfache, funktionierende Version
    return create_simple_neofetch(stats_text, color)

def get_animated_stats(stats_text):
    """
    Erstellt eine Liste mit einem statischen Frame (keine Animation mehr)

    Args:
        stats_text (str): Der Text mit den Statistiken

    Returns:
        list: Liste mit einem formatierten Text
    """
    # Erstelle nur einen Frame mit dem blauen Pinguin
    return [format_stats_with_ascii(stats_text, "static")]
