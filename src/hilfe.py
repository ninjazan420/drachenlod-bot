import discord
from discord import app_commands

async def create_help_embed(user_id: int, is_server_admin: bool, admin_user_id: int) -> discord.Embed:
    """Erstellt das Help-Embed basierend auf den Berechtigungen"""
    # Prüfe, ob der Nutzer der Bot-Owner ist (nicht Server-Admin!)
    is_bot_owner = (user_id == admin_user_id)

    embed = discord.Embed(
        title="🤖 Buttergolem Bot Hilfe",
        description=f"Dieser Bot scheißt dir zufällige Zitate vom Arschgebirge aus der Schimmelschanze direkt in deinen Discord-Server.\n\n**Bot Version:** 5.4.0 (06.06.2025)\n**Discord.py Version:** {discord.__version__}\n**Owner:** ninjazan420",
        color=0xf1c40f
    )
    
    # Bot-Informationen hinzufügen
    embed.add_field(
        name="📋 Bot-Informationen",
        value=f"**Owner:** ninjazan420\n**Bot-Version:** 5.4.0\n**Discord.py-Version:** {discord.__version__}",
        inline=False
    )

    # Basis-Befehle (erste Spalte)
    embed.add_field(
        name="📋 Basis-Befehle",
        value="• `!drache hilfe` - Zeigt diese Hilfe an\n"
              "• `!drache mett` - Zeigt den aktuellen Mett-Level 🥓\n"
              "• `!drache stats [@user]` - Drachenstats\n"
              "• `!drache zitat` - Zufälliges Zitat\n"
              "• `!drache meme <text>` - Erstellt ein Meme\n"
              "• `!drache update` - Zeigt Updates\n"
              "• `/kontakt <nachricht>` - Admin kontaktieren",
        inline=True
    )

    # Sound-Befehle (zweite Spalte)
    embed.add_field(
        name="🔊 Sound-Befehle",
        value="• `!drache lord` - Zufälliges GESCHREI\n"
             "• `!drache cringe` - Oh no, cringe!\n"
              "• `!drache sounds` - Zeigt alle Sounds\n"
              "• `!drache sound <n>` - Spielt Sound ab\n"
              "• `!drache quiz` - Quiz-Informationen\n"
              "• `!drache quiz start <n>` - Startet Quiz",
        inline=True
    )

    # KI-Funktionen (dritte Spalte)
    embed.add_field(
        name="🤖 KI & Kontakt",
        value="• `@Bot <Nachricht>` - KI-Chat\n"
              "• `DM an Bot` - Privater KI-Chat\n"
              "• `!kontakt <Nachricht>` - Admin-Kontakt\n"
              "• `!drache privacy` - Datenschutzerklärung\n"
              "• Bot Support: discord.gg/7J4mgSyB8n\n"
              "• `/kontakt` - Kontakt zum Admin",
        inline=True
    )
    
    # Slash-Befehle Sektion
    embed.add_field(
        name="⚡ Slash-Befehle",
        value="• `/mett` - Mett-Level anzeigen\n"
              "• `/zitat` - Zufälliges Zitat\n"
              "• `/lordmeme <text>` - Meme erstellen\n"
              "• `/drache ping` - Bot-Latenz\n"
              "• `/drache stats` - Bot-Statistiken\n"
              "• `/drache neofetch` - Neofetch-Style Stats\n"
              "• `/drache drachenlord` - Drachenlord-Zitat\n"
              "• `/drache hilfe` - Diese Hilfe anzeigen\n"
              "• `/kontakt <nachricht>` - Admin kontaktieren",
        inline=True
    )

    # Spenden- und Support-Bereich
    embed.add_field(
        name="💰 Spenden & Support",
        value="💰 `/spende` - Bot mit Monero unterstützen\n[🔧 Support-Server](https://support.f0ck.org)",
        inline=False
    )

    # Leerzeile für bessere Übersicht
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    # Admin-Befehle nur anzeigen wenn der Nutzer der Bot-Owner ist
    if is_bot_owner:
        embed.add_field(
            name="⚙️ Server-Verwaltung",
            value="• `!drache server [page]` - Server-Liste & Statistiken\n"
                  "• `!drache leave <ID> [message_id] [grund...]` - Server verlassen\n"
                  "• `!drache ban server <ID> [grund...]` - Server bannen\n"
                  "• `!drache unban server <ban_id>` - Server-Ban aufheben\n"
                  "• `!drache bans server` - Gebannte Server anzeigen",
            inline=True
        )

        embed.add_field(
            name="⚙️ User-Verwaltung",
            value="• `!drache ban user <ID> [server_id] [grund...]` - User bannen\n"
                  "• `!drache unban user <ban_id>` - User-Ban aufheben\n"
                  "• `!drache bans user` - Gebannte User anzeigen\n"
                  "• `!drache antwort <ID> <Text>` - Auf Kontaktnachrichten antworten\n"
                  "• `!drache butteriq disable/enable <ID>` - KI-Zugriff verwalten",
            inline=True
        )

        embed.add_field(
            name="\u200b",
            value="\u200b",
            inline=False
        )

        embed.add_field(
            name="⚙️ System-Befehle",
            value="• `!drache neofetch [style]` - Bot-Statistiken mit ASCII-Art\n"
                  "• `!drache butteriq [action]` - ButterIQ-Verwaltung\n"
                  "• `!drache ping` - Bot-Latenz anzeigen\n"
                  "• `!drache servercount` - Manuelles Servercounter-Update",
            inline=True
        )
        
        embed.add_field(
            name="⚡ Admin Slash-Befehle",
            value="• `/drache ban <typ> <id> [grund]` - Server/User bannen\n"
                  "• `/drache leave <server_id> [grund]` - Server verlassen\n"
                  "• `/server [page]` - Server-Liste & Statistiken\n"
                  "• `/servercount` - Manuelles Servercounter-Update",
            inline=True
        )

    embed.set_footer(text="Der Bot muss die Berechtigung besitzen, in den Voice zu joinen!")
    return embed

def register_help_commands(bot):
    # hilfe befehl entfernt - nur !lord bleibt bestehen
    # alle befehle wurden zu slash commands migriert
    pass

def setup(bot):
    register_help_commands(bot)