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

# Neofetch-Style System ASCII
NEOFETCH_ASCII = r"""
      ████████████████████████
    ██                      ██
  ██    ██████████████████      ██
██    ██              ██      ██
██  ██    ████████████  ██    ██
██  ██  ██          ██  ██    ██
██  ██  ██  ██████  ██  ██    ██
██  ██  ██  ██  ██  ██  ██    ██
██  ██  ██  ██████  ██  ██    ██
██  ██  ██          ██  ██    ██
██  ██    ████████████  ██    ██
██    ██              ██      ██
  ██    ████████████████      ██
    ██                      ██
      ████████████████████████

        BUTTERGOLEM SYSTEM
"""

# Minimalistisches ASCII für bessere Performance
MINIMAL_ASCII = r"""
        ╭─────────────────╮
    │  ◉   ◉   ◉   ◉  │
    │                 │
    │   BUTTERGOLEM   │
    │      STATS      │
    │                 │
    ╰─────────────────╯
"""

# Drachenlord Donkey Kong Style ASCII Frames (Verbessert)
DRACHENLORD_FRAMES = [
    # Frame 1: Drachenlord steht, Fass rollt von rechts
    """
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛    🧍                                          🛢️     ⬛
⬛  MEDDL                                              ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
    """,

    # Frame 2: Drachenlord bereitet sich auf Sprung vor, Fass rollt näher
    """
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛    🧍                                     🛢️          ⬛
⬛  MEDDL                                              ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
    """,

    # Frame 3: Drachenlord springt, Fass direkt unter ihm
    """
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛    🦘                                                ⬛
⬛  MEDDL                              🛢️               ⬛
⬛                                                      ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
    """,

    # Frame 4: Drachenlord landet, Fass rollt weiter
    """
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛      🧍                        🛢️                     ⬛
⬛    MEDDL                                            ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
    """,
    
    # Frame 5: Neues Fass erscheint, Drachenlord geht weiter
    """
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛        🧍                                      🛢️     ⬛
⬛      MEDDL                                          ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
    """,
    
    # Frame 6: Drachenlord bereitet sich auf nächsten Sprung vor
    """
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛                                                      ⬛
⬛        🧍                                 🛢️          ⬛
⬛      MEDDL                                          ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
    """
]

# Snake-Spiel mit Drachenlord und Brötchen
# Spielfeld ist 15x15 Zellen groß
SNAKE_FIELD = [
    "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛",
    "⬛                 ⬛",
    "⬛                 ⬛",
    "⬛                 ⬛",
    "⬛                 ⬛",
    "⬛                 ⬛",
    "⬛                 ⬛",
    "⬛                 ⬛",
    "⬛                 ⬛",
    "⬛                 ⬛",
    "⬛                 ⬛",
    "⬛                 ⬛",
    "⬛                 ⬛",
    "⬛                 ⬛",
    "⬛                 ⬛",
    "⬛                 ⬛",
    "⬛                 ⬛",
    "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛"
]

# Spielelemente
SNAKE_HEAD = "🧍"  # Drachenlord als Schlangenkopf
SNAKE_BODY = "👣"  # Fußspuren als Schlangenkörper
SNAKE_FOOD = "🥖"  # Brötchen als Futter
    

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

async def create_drachenlord_animation():
    """Erstellt eine Donkey Kong-ähnliche Animation mit Drachenlord und echten rollenden Fässern"""
    import copy
    import random
    frames = []
    # Spielfeldgröße
    width = 30
    height = 10  # Erhöht für bessere Darstellung
    # Startpositionen
    drache_x = 5
    drache_y = height - 2
    fass_start_x = width - 3
    fass_y = height - 2
    # Fässer-Logik: mehrere Fässer können gleichzeitig rollen
    fass_list = []
    fass_timer = 0
    max_frames = 30
    for frame_idx in range(max_frames):
        # Fässer generieren
        if fass_timer == 0 or (frame_idx % 7 == 0 and len(fass_list) < 3):
            fass_list.append({'x': fass_start_x, 'y': fass_y})
            fass_timer = 1
        # Fässer bewegen
        for fass in fass_list:
            fass['x'] -= 1
        # Entferne Fässer, die aus dem Bild sind
        fass_list = [f for f in fass_list if f['x'] > 0]
        # Drachenlord springt, wenn ein Fass in der Nähe ist
        drache_symbol = '🧍'
        for fass in fass_list:
            if abs(fass['x'] - drache_x) <= 2:  # Erhöhter Erkennungsbereich
                drache_symbol = '🦘'
                break
        # Zeichne das Spielfeld
        field = []
        field.append('⬛' * width)
        for y in range(1, height-1):
            row = ['⬛'] + [' ']*(width-2) + ['⬛']
            if y == drache_y:
                row[drache_x] = drache_symbol
            for fass in fass_list:
                if fass['y'] == y and 0 < fass['x'] < width-1:
                    row[fass['x']] = '🛢️'
            if y == drache_y+1 and drache_x >= 2:  # Sicherheitscheck für Index
                # Stelle sicher, dass wir nicht über die Grenzen hinausgehen
                start_idx = max(1, drache_x-1)
                end_idx = min(width-2, drache_x+2)
                # Füge 'MEDDL' ein, wenn genug Platz ist
                if end_idx - start_idx >= 3:
                    row[start_idx:start_idx+3] = list('MED')
            field.append(''.join(row))
        field.append('⬛' * width)
        # Farbiges Frame
        color = RAINBOW_COLORS[frame_idx % len(RAINBOW_COLORS)]
        color_code = color.replace('```ansi\n', '')
        frames.append(f"```ansi\n{color_code}" + '\n'.join(field) + "\n\u001b[0m```")
    # Endbild
    frames.append("```ansi\n\u001b[32;1mLEVEL GESCHAFFT! 🏆 Drachenlord hat alle Fässer übersprungen! MEDDL LEUDE! 🏆\u001b[0m```")
    return frames

async def create_snake_game(max_turns=30):
    """Erstellt eine Snake-Spiel Animation mit Drachenlord und Brötchen
    
    Args:
        max_turns (int): Maximale Anzahl der Spielzüge
        
    Returns:
        list: Liste mit Frames der Animation und Spielstatus
    """
    import random
    import copy
    
    # Spielfeld-Dimensionen (ohne Rand)
    width = 15
    height = 15
    
    # Initialisiere Schlange in der Mitte
    snake = [(height // 2, width // 2)]
    direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])  # (y, x) Format
    
    # Platziere erstes Brötchen
    food = None
    while food is None or food in snake:
        food = (random.randint(1, height-2), random.randint(1, width-2))
    
    # Spielstatus
    score = 0
    game_over = False
    frames = []
    
    # Erstelle Frames für jeden Spielzug
    for _ in range(max_turns):
        if game_over:
            break
            
        # Bewege Schlange
        head_y, head_x = snake[0]
        new_head = (head_y + direction[0], head_x + direction[1])
        
        # Prüfe Kollision mit Wand
        if (new_head[0] <= 0 or new_head[0] >= height-1 or 
            new_head[1] <= 0 or new_head[1] >= width-1):
            game_over = True
            break
            
        # Prüfe Kollision mit sich selbst
        if new_head in snake:
            game_over = True
            break
            
        # Füge neuen Kopf hinzu
        snake.insert(0, new_head)
        
        # Prüfe, ob Brötchen gefressen wurde
        if new_head == food:
            score += 1
            # Neues Brötchen platzieren
            food = None
            while food is None or food in snake:
                food = (random.randint(1, height-2), random.randint(1, width-2))
        else:
            # Entferne Schwanz, wenn kein Brötchen gefressen wurde
            snake.pop()
        
        # Ändere Richtung zufällig, aber nicht in die entgegengesetzte Richtung
        possible_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        opposite = (-direction[0], -direction[1])
        if opposite in possible_directions:  # Sicherheitscheck
            possible_directions.remove(opposite)
        
        # Mit 30% Wahrscheinlichkeit Richtung ändern
        if random.random() < 0.3 and possible_directions:  # Sicherheitscheck
            direction = random.choice(possible_directions)
        
        # Erstelle Frame
        field_copy = copy.deepcopy(SNAKE_FIELD)
        
        # Zeichne Schlange
        for i, (y, x) in enumerate(snake):
            # Stelle sicher, dass die Koordinaten im gültigen Bereich liegen
            if 0 <= y < len(field_copy) and 0 <= x < len(field_copy[y]):
                # Konvertiere Koordinaten zu Indizes im Spielfeld
                char = SNAKE_HEAD if i == 0 else SNAKE_BODY
                row = list(field_copy[y])
                row[x] = char
                field_copy[y] = ''.join(row)
        
        # Zeichne Brötchen
        if food:
            y, x = food
            # Stelle sicher, dass die Koordinaten im gültigen Bereich liegen
            if 0 <= y < len(field_copy) and 0 <= x < len(field_copy[y]):
                row = list(field_copy[y])
                row[x] = SNAKE_FOOD
                field_copy[y] = ''.join(row)
        
        # Füge Punktestand hinzu
        field_str = '\n'.join(field_copy)
        field_str += f"\n\nMEDDL LEUDE! Brötchen: {score}"
        
        # Färbe Frame
        color = RAINBOW_COLORS[len(frames) % len(RAINBOW_COLORS)]
        color_code = color.replace("```ansi\n", "")
        colored_frame = f"```ansi\n{color_code}{field_str}\u001b[0m```"
        
        frames.append(colored_frame)
    
    # Füge Game Over oder Gewonnen Frame hinzu
    final_frame = "```ansi\n"
    if game_over:
        final_frame += f"\u001b[31;1m🎮 GAME OVER! 🎮\n\nDrachenlord hat {score} Brötchen gesammelt!\u001b[0m"
    else:
        final_frame += f"\u001b[32;1m🎮 LEVEL GESCHAFFT! 🎮\n\nDrachenlord hat {score} Brötchen gesammelt!\u001b[0m"
    final_frame += "```"
    
    return frames + [final_frame]

async def create_train_animation(frames=20):
    """Erstellt eine einfache Drachenlord-Animation für /sl"""
    animation_frames = []
    train_length = 10
    max_width = 40
    
    for i in range(frames):
        position = i % (max_width - train_length)  # Bewegung über max_width Zeichen, dann Neustart
        
        # Erstelle Zug mit Drachenlord
        train = ' ' * position + 'ᕕ(ᐛ)ᕗ' + '=' * (train_length - 3) + '>'
        
        # Füge Rauch hinzu (mit Sicherheitscheck)
        smoke = ' ' * (position - 2) + '~' * 3 if position > 2 else ''
        
        # Stelle sicher, dass die Farbe gültig ist
        if RAINBOW_COLORS and len(RAINBOW_COLORS) > 0:
            color_index = i % len(RAINBOW_COLORS)
            color = RAINBOW_COLORS[color_index]
            # Entferne Markdown-Code-Block-Marker falls vorhanden
            color_code = color.replace("```ansi\n", "")
            
            frame = f"```ansi\n{color_code}{smoke}\n{train}\u001b[0m```"
        else:
            # Fallback ohne Farbe, falls RAINBOW_COLORS leer ist
            frame = f"```\n{smoke}\n{train}```"
            
        animation_frames.append(frame)
    
    return animation_frames

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
