import discord
from discord.ext import commands
import datetime

def register_update_commands(bot):
    """Registriert den !lordupdate Befehl"""



    @bot.tree.command(name="changelog", description="Zeigt das Changelog für eine bestimmte Version")
    async def changelog_slash(interaction: discord.Interaction, version: str = None):
        """Zeigt das Changelog als Slash-Befehl"""
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