#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from ascii_art import get_animated_stats, get_drachenlord_quote

async def send_animated_stats(ctx, bot, stats_text, animation_type="static", show_quotes=False):
    """
    Sendet eine Statistik-Nachricht im neofetch-Stil mit der ASCII-Art auf der linken Seite
    und den Statistiken auf der rechten Seite

    Args:
        ctx: Der Kontext des Befehls
        bot: Die Bot-Instanz
        stats_text: Der Text mit den Statistiken
        animation_type: Art der Anzeige ("static", "gradient", "drachenlord", "shrek")
        show_quotes: Ob Drachenlord-Zitate angezeigt werden sollen
    """
    # Importiere die Formatierungsfunktion
    from ascii_art import format_stats_with_ascii
    import datetime

    # Erstelle die formatierte Nachricht im neofetch-Stil
    formatted_message = format_stats_with_ascii(stats_text, animation_type.lower())

    # Sende die Nachricht
    try:
        message = await ctx.send(formatted_message)
    except Exception as e:
        print(f"Fehler beim Senden der Nachricht: {e}")
        # Versuche es mit einer einfacheren Nachricht ohne Formatierung
        message = await ctx.send(f"```\n{stats_text}```")
        return message

    # Füge ein zufälliges Drachenlord-Zitat hinzu, wenn gewünscht
    if show_quotes:
        from ascii_art import get_drachenlord_quote
        quote = get_drachenlord_quote()
        await ctx.send(f"> *{quote}*", delete_after=5.0)

async def send_animated_stats_with_color(ctx, bot, stats_text, animation_type="static", color="blue", show_quotes=False):
    """
    Sendet eine Statistik-Nachricht im neofetch-Stil mit der ASCII-Art auf der linken Seite
    und den Statistiken auf der rechten Seite mit Farbauswahl

    Args:
        ctx: Der Kontext des Befehls
        bot: Die Bot-Instanz
        stats_text: Der Text mit den Statistiken
        animation_type: Art der Anzeige ("static", "gradient", "drachenlord", "shrek")
        color: Farbauswahl für die ASCII-Art
        show_quotes: Ob Drachenlord-Zitate angezeigt werden sollen
    """
    # Importiere die Formatierungsfunktion
    from ascii_art import format_stats_with_ascii_color
    import datetime

    # Wenn Zitate angezeigt werden sollen, füge sie direkt in die Stats ein
    if show_quotes:
        from ascii_art import get_drachenlord_quote
        quote = get_drachenlord_quote()
        stats_text += f"\n**KI-Nachrichten:** {quote}"

    # Erstelle die formatierte Nachricht im neofetch-Stil mit Farbe
    formatted_message = format_stats_with_ascii_color(stats_text, animation_type.lower(), color)

    # Sende die Nachricht
    try:
        message = await ctx.send(formatted_message)
    except Exception as e:
        print(f"Fehler beim Senden der Nachricht: {e}")
        # Versuche es mit einer einfacheren Nachricht ohne Formatierung
        message = await ctx.send(f"```\n{stats_text}```")
        return message

    return message

def collect_bot_stats(bot):
    """Sammelt alle relevanten Bot-Statistiken LIVE und gibt sie als formatierten Text zurück"""
    import datetime
    import psutil
    import os

    # === LIVE SERVER & MEMBER STATS ===
    total_servers = len(bot.guilds)
    total_members = sum(g.member_count for g in bot.guilds)

    # === VOICE CHANNEL STATS ===
    active_voice_connections = len(bot.voice_clients)
    total_voice_channels = sum(len(guild.voice_channels) for guild in bot.guilds)

    # === PERSISTENT STATS (aus stats.json) ===
    unique_users = len(bot.stats_manager.stats['unique_users']) if hasattr(bot, 'stats_manager') else 0
    commands_used = bot.stats_manager.stats['commands_executed'] if hasattr(bot, 'stats_manager') else 0
    sounds_played = bot.stats_manager.stats['sounds_played'] if hasattr(bot, 'stats_manager') else 0
    servers_joined_total = bot.stats_manager.stats['servers_joined'] if hasattr(bot, 'stats_manager') else 0

    # === UPTIME BERECHNUNG ===
    try:
        start_time = getattr(bot, 'start_time', datetime.datetime.now())
        if start_time.tzinfo is None:
            current_time = datetime.datetime.now()
        else:
            current_time = datetime.datetime.now(start_time.tzinfo)

        uptime = current_time - start_time
        days, remainder = divmod(int(uptime.total_seconds()), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{days}d {hours}h {minutes}m"
    except Exception as e:
        print(f"Fehler bei der Uptime-Berechnung: {e}")
        uptime_str = "Unbekannt"

    # === SYSTEM STATS ===
    try:
        memory_usage = psutil.virtual_memory().percent
        cpu_usage = psutil.cpu_percent(interval=0.1)
        disk_usage = psutil.disk_usage('/').percent if os.path.exists('/') else 0
    except Exception:
        memory_usage = cpu_usage = disk_usage = 0

    # === KI STATS ===
    try:
        ki_version = bot.ki_stats["version"] if hasattr(bot, 'ki_stats') else "6.2.0"
        ki_messages = bot.ki_stats["messageCount"] if hasattr(bot, 'ki_stats') else 0
    except Exception:
        ki_version = "6.2.0"
        ki_messages = 0 

    # === SOUND SYSTEM STATS ===
    try:
        sound_dir = "/app/data/clips"
        if os.path.exists(sound_dir):
            import glob
            sound_files = glob.glob(os.path.join(sound_dir, "*.mp3"))
            available_sounds = len(sound_files)
        else:
            available_sounds = 0
    except Exception:
        available_sounds = 0

    # === FORMATIERTER STATS TEXT ===
    stats_text = (
        f"**🤖 Bot:** Buttergolem v{ki_version}\n"
        f"**⏱️ Uptime:** {uptime_str}\n"
        f"**📡 Latenz:** {round(bot.latency * 1000)}ms\n"
        f"**🌐 Server:** {total_servers:,} (Total: {servers_joined_total:,})\n"
        f"**👥 Mitglieder:** {total_members:,}\n"
        f"**🎯 Unique Users:** {unique_users:,}\n"
        f"**🔊 Voice Channels:** {active_voice_connections}/{total_voice_channels}\n"
        f"**⚡ Befehle:** {commands_used:,}\n"
        f"**🎵 Sounds:** {sounds_played:,} ({available_sounds} verfügbar)\n"
        f"**🧠 KI Messages:** {ki_messages:,}\n"
        f"**💾 RAM:** {memory_usage:.1f}% | **🖥️ CPU:** {cpu_usage:.1f}%"
    )

    return stats_text

def register_animated_stats_commands(bot):
    """Registriert die Befehle für animierte Statistiken"""
    pass

