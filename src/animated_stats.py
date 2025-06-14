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
    """Sammelt alle relevanten Bot-Statistiken und gibt sie als formatierten Text zurück"""
    # Sammle Statistiken
    total_servers = len(bot.guilds)
    total_members = sum(g.member_count for g in bot.guilds)
    unique_users = len(bot.stats_manager.stats['unique_users']) if hasattr(bot, 'stats_manager') else 0
    commands_used = bot.stats_manager.stats['commands_executed'] if hasattr(bot, 'stats_manager') else 0
    sounds_played = bot.stats_manager.stats['sounds_played'] if hasattr(bot, 'stats_manager') else 0

    # Berechne Uptime - mit Fehlerbehandlung für datetime-Probleme
    try:
        import datetime
        # Stelle sicher, dass beide Zeitstempel im gleichen Format sind (aware oder naive)
        start_time = getattr(bot, 'start_time', datetime.datetime.now())

        # Wenn start_time ein naive datetime ist, verwende auch ein naive datetime für jetzt
        if start_time.tzinfo is None:
            current_time = datetime.datetime.now()
        else:
            # Sonst verwende ein aware datetime
            current_time = discord.utils.utcnow()

        uptime = current_time - start_time
        days, remainder = divmod(int(uptime.total_seconds()), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
    except Exception as e:
        print(f"Fehler bei der Uptime-Berechnung: {e}")
        uptime_str = "Nicht verfügbar"

    # KI-Version und Nachrichten mit Fehlerbehandlung
    try:
        ki_version = bot.ki_stats["version"] if hasattr(bot, 'ki_stats') else "N/A"
        ki_messages = bot.ki_stats["messageCount"] if hasattr(bot, 'ki_stats') else 0
    except Exception as e:
        print(f"Fehler beim Abrufen der KI-Statistiken: {e}")
        ki_version = "N/A"
        ki_messages = 0

    # Statistik-Text erstellen
    stats_text = (
        f"**Bot Uptime:** {uptime_str}\n"
        f"**Latenz:** {round(bot.latency * 1000)}ms\n"
        f"**KI-Version:** {ki_version}\n"
        f"**Discord Server:** {total_servers}\n"
        f"**Mitglieder:** {total_members}\n"
        f"**Eindeutige Nutzer:** {unique_users}\n"
        f"**Befehle ausgeführt:** {commands_used}\n"
        f"**Sounds abgespielt:** {sounds_played}\n"
        f"**KI-Nachrichten:** {ki_messages}"
    )

    return stats_text

def register_animated_stats_commands(bot):
    """Registriert die Befehle für animierte Statistiken"""
    # Drache command wurde zu slash commands migriert - siehe slash_commands.py
    pass

    # Alter prefix command - jetzt deaktiviert
    # @bot.command(name='drache')
    # @commands.is_owner()  # Nur für Bot-Besitzer
    # async def drache_command(ctx, action=None, animation_type="static"):
    #     """Hauptbefehl für alle Drache-Funktionen"""
    #     if action is None:
    #         # Zeige Hilfe
    #         help_text = (
    #             "**🐉 Drache-Befehle**\n\n"
    #             "**Verfügbare Aktionen:**\n"
    #             "• `!drache neofetch [style]` - Bot-Statistiken im neofetch-Stil\n"
    #             "• `!drache dragonlord` - Drachenlord-inspirierte Statistiken mit Zitaten\n"
    #             "• `!drache shrekfetch` - Shrek-inspirierte Statistiken\n"
    #             "• `!drache styles` - Zeigt alle verfügbaren ASCII-Art-Stile\n"
    #             "• `!drache hilfe` - Zeigt diese Hilfe\n\n"
    #             "**Verfügbare Stile:**\n"
    #             "• `static` - Blauer Pinguin (Standard)\n"
    #             "• `gradient` - Farbverlauf in der ASCII-Art\n"
    #             "• `drachenlord` - Drachenlord-ASCII-Art mit zufälliger Farbe\n"
    #             "• `shrek` - Shrek-inspirierte ASCII-Art\n\n"
    #             "**Beispiele:**\n"
    #             "• `!drache neofetch static`\n"
    #             "• `!drache neofetch gradient`\n"
    #         )
    #         await ctx.send(help_text)
    #         return
    # 
    #     elif action.lower() == 'neofetch':
    #         # Überprüfe, ob der Animationstyp gültig ist
    #         valid_types = ["static", "gradient", "drachenlord", "shrek"]
    #         if animation_type.lower() not in valid_types:
    #             await ctx.send(f"❌ Ungültiger Animationstyp! Gültige Typen: {', '.join(valid_types)}")
    #             return
    # 
    #         # Sammle Statistiken
    #         stats_text = collect_bot_stats(bot)
    # 
    #         # Sende die statische Statistik
    #         await send_animated_stats(ctx, bot, stats_text, animation_type, show_quotes=False)
    # 
    #         # Logge den Befehl
    #         if hasattr(bot, 'logging_channel'):
    #             channel = bot.get_channel(bot.logging_channel)
    #             if channel:
    #                 await channel.send(f"```\nAdmin-Befehl !drache neofetch {animation_type} wurde von {ctx.author.name} ausgeführt```")
    # 
    #     elif action.lower() == 'dragonlord':
    #         # Sammle Statistiken
    #         stats_text = collect_bot_stats(bot)
    # 
    #         # Sende die Drachenlord-Statistik
    #         await send_animated_stats(ctx, bot, stats_text, "drachenlord", show_quotes=True)
    # 
    #         # Logge den Befehl
    #         if hasattr(bot, 'logging_channel'):
    #             channel = bot.get_channel(bot.logging_channel)
    #             if channel:
    #                 await channel.send(f"```\nAdmin-Befehl !drache dragonlord wurde von {ctx.author.name} ausgeführt```")
    # 
    #     elif action.lower() == 'shrekfetch':
    #         # Sammle Statistiken
    #         stats_text = collect_bot_stats(bot)
    # 
    #         # Sende die Shrek-Statistik
    #         await send_animated_stats(ctx, bot, stats_text, "shrek", show_quotes=False)
    # 
    #         # Logge den Befehl
    #         if hasattr(bot, 'logging_channel'):
    #             channel = bot.get_channel(bot.logging_channel)
    #             if channel:
    #                 await channel.send(f"```\nAdmin-Befehl !drache shrekfetch wurde von {ctx.author.name} ausgeführt```")
    # 
    #     elif action.lower() in ['styles', 'asciistyles']:
    #         help_text = (
    #             "**🎨 Verfügbare ASCII-Art-Stile**\n\n"
    #             "**Befehle:**\n"
    #             "• `!drache neofetch [style]` - Bot-Statistiken im neofetch-Stil\n"
    #             "• `!drache dragonlord` - Drachenlord-inspirierte Statistiken mit Zitaten\n"
    #             "• `!drache shrekfetch` - Shrek-inspirierte Statistiken\n\n"
    #             "**Verfügbare Stile:**\n"
    #             "• `static` - Blauer Pinguin (Standard)\n"
    #             "• `gradient` - Farbverlauf in der ASCII-Art\n"
    #             "• `drachenlord` - Drachenlord-ASCII-Art mit zufälliger Farbe\n"
    #             "• `shrek` - Shrek-inspirierte ASCII-Art\n\n"
    #             "**Beispiele:**\n"
    #             "• `!drache neofetch static`\n"
    #             "• `!drache neofetch gradient`\n"
    #         )
    # 
    #         # Sende die Hilfe
    #         await ctx.send(help_text)
    # 
    #         # Logge den Befehl
    #         if hasattr(bot, 'logging_channel'):
    #             channel = bot.get_channel(bot.logging_channel)
    #             if channel:
    #                 await channel.send(f"```\nAdmin-Befehl !drache styles wurde von {ctx.author.name} ausgeführt```")
    # 
    #     elif action.lower() == 'hilfe':
    #         # Zeige die gleiche Hilfe wie bei keiner Aktion
    #         help_text = (
    #             "**🐉 Drache-Befehle**\n\n"
    #             "**Verfügbare Aktionen:**\n"
    #             "• `!drache neofetch [style]` - Bot-Statistiken im neofetch-Stil\n"
    #             "• `!drache dragonlord` - Drachenlord-inspirierte Statistiken mit Zitaten\n"
    #             "• `!drache shrekfetch` - Shrek-inspirierte Statistiken\n"
    #             "• `!drache styles` - Zeigt alle verfügbaren ASCII-Art-Stile\n"
    #             "• `!drache hilfe` - Zeigt diese Hilfe\n\n"
    #             "**Verfügbare Stile:**\n"
    #             "• `static` - Blauer Pinguin (Standard)\n"
    #             "• `gradient` - Farbverlauf in der ASCII-Art\n"
    #             "• `drachenlord` - Drachenlord-ASCII-Art mit zufälliger Farbe\n"
    #             "• `shrek` - Shrek-inspirierte ASCII-Art\n\n"
    #             "**Beispiele:**\n"
    #             "• `!drache neofetch static`\n"
    #             "• `!drache neofetch gradient`\n"
    #         )
    #         await ctx.send(help_text)

    #     else:
    #         await ctx.send(f"❌ Unbekannte Aktion: {action}\nVerwende `!drache hilfe` für eine Liste aller verfügbaren Befehle.")
