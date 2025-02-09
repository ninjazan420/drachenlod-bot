import discord
from discord import app_commands

async def create_help_embed(is_admin: bool) -> discord.Embed:
    """Erstellt das Help-Embed basierend auf den Berechtigungen"""
    embed = discord.Embed(
        title="🤖 Buttergolem Bot Hilfe",
        description="Dieser Bot scheißt dir zufällige Zitate vom Arschgebirge aus der Schimmelschanze direkt in deinen Discord-Server.\n\nVersion: 4.3.0 | Created by: ninjazan420",
        color=0xf1c40f
    )

    # Basis-Befehle
    embed.add_field(
        name="📋 Basis-Befehle",
        value="• `!hilfe` - Zeigt diese Hilfe an\n"
              "• `!mett` - Zeigt den aktuellen Mett-Level 🥓\n"
              "• `!zitat` - Zufälliges Zitat\n"
              "• `!lordmeme <text>` - Erstellt ein Drachenlord Meme (Nutze | für oben/unten)",
        inline=False
    )

    # Sound-Befehle
    embed.add_field(
        name="🔊 Sound-Befehle",
        value="• `!lord` - Zufälliges GESCHREI im Voice\n"
              "• `!cringe` - Oh no, cringe!\n"
              "• `!sounds` - Zeigt alle verfügbaren Sounds\n"
              "• `!sound <name>` - Spielt einen bestimmten Sound ab\n",
        inline=False
    )

    # Quiz-Befehle
    embed.add_field(
        name="❓ Quiz-Befehle",
        value="• `!lordquiz` - Quiz-Informationen\n"
              "• `!lordquiz start <Anzahl Runden (1-20)>` - Startet Quiz\n"
              "• `!lordquiz stop` - Beende Quiz",
        inline=False
    )

    # Kontakt-Befehle
    embed.add_field(
        name="📧 Kontakt",
        value="• `!kontakt <Nachricht>` - Sende eine Nachricht an den Admin\n",
        inline=False
    )

    # Admin-Befehle nur anzeigen wenn Admin
    if is_admin:
        embed.add_field(
            name="⚙️ Admin-Befehle",
            value="• `!server` - Server-Liste\n"
                  "• `!user` - Nutzerstatistiken\n"
                  "• `!ping` - Bot-Latenz\n"
                  "• `!antwort <ID> <Text>` - Auf Kontaktnachrichten antworten",
            inline=False
        )

    embed.set_footer(text="Der Bot muss die Berechtigung besitzen, in den Voice zu joinen!")
    return embed

def register_help_commands(bot):
    @bot.command(name='hilfe')
    async def hilfe_command(ctx):
        """Zeigt die Hilfe für den Buttergolem Bot"""
        is_admin = ctx.author.guild_permissions.administrator
        embed = await create_help_embed(is_admin)
        await ctx.send(embed=embed)

    @bot.tree.command(name="hilfe", description="Zeigt die Hilfe für den Buttergolem Bot")
    async def hilfe_slash(interaction: discord.Interaction):
        """Zeigt die Hilfe für den Buttergolem Bot"""
        is_admin = interaction.user.guild_permissions.administrator
        embed = await create_help_embed(is_admin)
        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    register_help_commands(bot)
