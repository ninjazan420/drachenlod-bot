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

# Liste aller Vordergrundfarben für Animation
ALL_COLORS = [
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE,
    BRIGHT_BLACK, BRIGHT_RED, BRIGHT_GREEN, BRIGHT_YELLOW,
    BRIGHT_BLUE, BRIGHT_MAGENTA, BRIGHT_CYAN, BRIGHT_WHITE
]

# Liste aller Hintergrundfarben für Animation
ALL_BG_COLORS = [
    BG_BLACK, BG_RED, BG_GREEN, BG_YELLOW,
    BG_BLUE, BG_MAGENTA, BG_CYAN, BG_WHITE
]

def get_colored_ascii(color="blue", style="buttergolem"):
    """Gibt die ASCII-Art mit der angegebenen Farbe und Stil zurück"""
    import random
    
    # Wähle ASCII-Art basierend auf Stil
    if style.lower() == "drachenlord":
        ascii_art = DRACHENLORD_ASCII
    elif style.lower() == "shrek":
        ascii_art = DRACHENLORD_SHREK_ASCII
    else:
        ascii_art = BUTTERGOLEM_ASCII

    # Wenn "drachenlord" oder "random" gewählt wurde, wähle eine zufällige Farbe
    if color.lower() == "drachenlord" or color.lower() == "random":
        random_color = random.choice(ALL_COLORS)
        return f"{random_color}{ascii_art}{RESET}"
    # Spezielle Farben
    elif color.lower() == "blue":
        return f"{BLUE}{ascii_art}{RESET}"
    elif color.lower() == "green":
        return f"{GREEN}{ascii_art}{RESET}"
    elif color.lower() == "yellow":
        return f"{YELLOW}{ascii_art}{RESET}"
    elif color.lower() == "red":
        return f"{RED}{ascii_art}{RESET}"
    elif color.lower() == "cyan":
        return f"{CYAN}{ascii_art}{RESET}"
    elif color.lower() == "magenta":
        return f"{MAGENTA}{ascii_art}{RESET}"
    elif color.lower() == "white":
        return f"{WHITE}{ascii_art}{RESET}"
    elif color.lower() == "bright_green" or color.lower() == "shrek":
        return f"{BRIGHT_GREEN}{ascii_art}{RESET}"
    elif color.lower() == "bright_red":
        return f"{BRIGHT_RED}{ascii_art}{RESET}"
    elif color.lower() == "bright_blue":
        return f"{BRIGHT_BLUE}{ascii_art}{RESET}"
    elif color.lower() == "bright_yellow":
        return f"{BRIGHT_YELLOW}{ascii_art}{RESET}"
    elif color.lower() == "gradient":
        return get_gradient_ascii()
    else:
        # Fallback: Verwende blaue ASCII-Art ohne ANSI-Farben
        return f"```{ascii_art}```"

def get_animated_frame(frame_num):
    """Gibt einen Frame der animierten ASCII-Art zurück"""
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

def get_gradient_ascii():
    """Erstellt eine ASCII-Art mit Farbverlauf für jede Zeile"""
    lines = DRACHENLORD_SHREK_ASCII.strip().split('\n')
    gradient_colors = [
        BRIGHT_RED, BRIGHT_YELLOW, BRIGHT_GREEN,
        BRIGHT_CYAN, BRIGHT_BLUE, BRIGHT_MAGENTA
    ]

    # Erstelle den Farbverlauf
    colored_lines = []
    for i, line in enumerate(lines):
        color = gradient_colors[i % len(gradient_colors)]
        # Entferne den Markdown-Anfang vom Farbcode
        color_code = color.replace("```ansi\n", "")
        colored_lines.append(f"{color_code}{line}\n")

    # Füge alle Zeilen zusammen und stelle sicher, dass die Backticks korrekt gesetzt sind
    return f"```ansi\n{''.join(colored_lines)}\u001b[0m```"

def get_rainbow_animation_frames(num_frames=8):
    """Erstellt eine Liste von Frames für eine Regenbogen-Animation"""
    frames = []
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
        "Ich bin ein Kagghaider!",
        "Ich bin ein Kaggduschne!",
        "Ich bin ein Kagghaider!",
        "Ich bin Kaggduschne!",
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

def format_stats_with_ascii_color(stats_text, animation_type="static", color="blue"):
    """
    Formatiert die Statistiken mit ASCII-Art im neofetch-Stil mit Farbauswahl

    Args:
        stats_text (str): Der Text mit den Statistiken
        animation_type (str): Art der Anzeige ("static", "gradient", "drachenlord", "shrek")
        color (str): Farbauswahl für die ASCII-Art

    Returns:
        str: Formatierte Nachricht mit ASCII-Art und Statistiken
    """
    import random
    
    # Farbmapping
    color_map = {
        "blue": BRIGHT_BLUE,
        "red": BRIGHT_RED,
        "green": BRIGHT_GREEN,
        "yellow": BRIGHT_YELLOW,
        "magenta": BRIGHT_MAGENTA,
        "cyan": BRIGHT_CYAN,
        "white": BRIGHT_WHITE,
        "random": random.choice([BRIGHT_RED, BRIGHT_GREEN, BRIGHT_YELLOW, BRIGHT_BLUE, BRIGHT_MAGENTA, BRIGHT_CYAN]),
        "gradient": "gradient"  # Spezialbehandlung für Gradient
    }
    
    # Wähle ASCII-Art basierend auf animation_type
    if animation_type == "drachenlord":
        ascii_art_base = DRACHENLORD_ASCII
    elif animation_type == "shrek":
        ascii_art_base = DRACHENLORD_SHREK_ASCII
    else:
        ascii_art_base = BUTTERGOLEM_ASCII
    
    # Wende Farbe an
    if color == "gradient":
        # Für Gradient verwende zufällige Farbe
        selected_color = random.choice([BRIGHT_RED, BRIGHT_GREEN, BRIGHT_YELLOW, BRIGHT_BLUE, BRIGHT_MAGENTA, BRIGHT_CYAN])
    else:
        selected_color = color_map.get(color, BRIGHT_BLUE)
    
    ascii_art = f"{selected_color}{ascii_art_base}{RESET}"
    
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
    ascii_lines = clean_ascii.split('\n')

    # Teile die Statistiken in Zeilen auf
    stats_lines = stats_text.strip().split('\n')

    # Berechne die maximale Länge der ASCII-Art-Zeilen für die Ausrichtung
    max_ascii_length = max((len(line) for line in ascii_lines if line.strip()), default=0)

    # Füge Padding hinzu
    padding = 4

    # Erstelle die formatierte Ausgabe im neofetch-Stil
    formatted_output = "```ansi\n"

    # Bestimme die maximale Anzahl von Zeilen
    max_lines = max(len(ascii_lines), len(stats_lines))

    # Kombiniere ASCII-Art und Statistiken nebeneinander
    for i in range(max_lines):
        line = ""

        # Füge ASCII-Art hinzu, wenn verfügbar
        if i < len(ascii_lines):
            ascii_line = f"{color_code}{ascii_lines[i]}"
            line += ascii_line
            padding_needed = max_ascii_length - len(ascii_lines[i]) + padding
            line += " " * padding_needed
        else:
            line += " " * (max_ascii_length + padding)

        # Füge Statistiken hinzu, wenn verfügbar
        if i < len(stats_lines):
            stats_line = f"\u001b[36;1m{stats_lines[i]}"
            line += stats_line

        formatted_output += f"{line}\n"

    # Füge den Reset-Code und die schließenden Backticks hinzu
    formatted_output += "\u001b[0m```"

    return formatted_output

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
