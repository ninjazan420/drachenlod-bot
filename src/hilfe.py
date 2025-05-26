import discord
from discord import app_commands

async def create_help_embed(user_id: int, is_server_admin: bool, admin_user_id: int) -> discord.Embed:
    """Erstellt das Help-Embed basierend auf den Berechtigungen"""
    # Prüfe, ob der Nutzer der Haupt-Admin ist
    is_admin = (user_id == admin_user_id)

    embed = discord.Embed(
        title="🤖 Buttergolem Bot Hilfe",
        description="Dieser Bot scheißt dir zufällige Zitate vom Arschgebirge aus der Schimmelschanze direkt in deinen Discord-Server.\n\nVersion: 5.2.0 (24.05.2025) | Created by: ninjazan420",
        color=0xf1c40f
    )

    # Basis-Befehle (erste Spalte)
    embed.add_field(
        name="📋 Basis-Befehle",
        value="• `!hilfe` - Zeigt diese Hilfe an\n"
              "• `!mett` - Zeigt den aktuellen Mett-Level 🥓\n"
              "• `!lordstats [@user]` - Drachenstats\n"
              "• `!zitat` - Zufälliges Zitat\n"
              "• `!lordmeme <text>` - Erstellt ein Meme\n"
              "• `!lordupdate` - Zeigt Updates",
        inline=True
    )

    # Sound-Befehle (zweite Spalte)
    embed.add_field(
        name="🔊 Sound-Befehle",
        value="• `!lord` - Zufälliges GESCHREI\n"
             "• `!cringe` - Oh no, cringe!\n"
              "• `!sounds` - Zeigt alle Sounds\n"
              "• `!sound <n>` - Spielt Sound ab\n"
              "• `!lordquiz` - Quiz-Informationen\n"
              "• `!lordquiz start <n>` - Startet Quiz",
        inline=True
    )

    # KI-Funktionen (dritte Spalte)
    embed.add_field(
        name="🤖 KI & Kontakt",
        value="• `@Bot <Nachricht>` - KI-Chat\n"
              "• `DM an Bot` - Privater KI-Chat\n"
              "• `!kontakt <Nachricht>` - Admin-Kontakt\n"
              "• Support: discord.gg/7J4mgSyB8n",
        inline=True
    )

    # Leerzeile für bessere Übersicht
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    # Admin-Befehle nur anzeigen wenn der Nutzer der Haupt-Admin ist
    if is_admin:
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
                  "• `!antwort <ID> <Text>` - Auf Kontaktnachrichten antworten\n"
                  "• `!butteriq disable/enable <ID>` - KI-Zugriff verwalten",
            inline=True
        )

        embed.add_field(
            name="\u200b",
            value="\u200b",
            inline=False
        )

        embed.add_field(
            name="⚙️ System-Befehle",
            value="• `!buttergolem stats` - Bot-Statistiken mit Neofetch-Style\n"
                  "• `!ping` - Bot-Latenz anzeigen\n"
                  "• `!servercount` - Manuelles Servercounter-Update",
            inline=True
        )

    embed.set_footer(text="Der Bot muss die Berechtigung besitzen, in den Voice zu joinen!")
    return embed

def register_help_commands(bot):
    @bot.command(name='hilfe')
    async def hilfe_command(ctx):
        """Zeigt die Hilfe für den Buttergolem Bot"""
        is_server_admin = ctx.author.guild_permissions.administrator
        embed = await create_help_embed(ctx.author.id, is_server_admin, bot.admin_user_id)
        await ctx.send(embed=embed)

    @bot.tree.command(name="hilfe", description="Zeigt die Hilfe für den Buttergolem Bot")
    async def hilfe_slash(interaction: discord.Interaction):
        """Zeigt die Hilfe für den Buttergolem Bot"""
        is_server_admin = interaction.user.guild_permissions.administrator
        embed = await create_help_embed(interaction.user.id, is_server_admin, bot.admin_user_id)
        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    register_help_commands(bot)