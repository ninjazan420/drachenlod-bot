import discord
from discord.ext import commands
import datetime

def register_update_commands(bot):
    """Registriert den !lordupdate Befehl"""



    @bot.tree.command(name="lordupdate", description="Zeigt die neuesten Updates des Bots")
    async def lordupdate_slash(interaction: discord.Interaction, version: str = None):
        """Zeigt die neuesten Updates des Bots als Slash-Befehl mit Changelog-System"""
        # Changelog-System verwenden
        from changelog import ChangelogCog
        changelog_cog = ChangelogCog(bot)
        
        if version:
            # Spezifische Version anzeigen
            await changelog_cog.send_version_changelog(interaction, version)
        else:
            # Übersicht aller Versionen anzeigen
            await changelog_cog.send_changelog_overview(interaction)

def setup(bot):
    register_update_commands(bot)