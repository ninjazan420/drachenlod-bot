import discord
from discord.ext import commands
import datetime

def register_update_commands(bot):
    """Registriert den !lordupdate Befehl"""
    
    @bot.command(name='lordupdate')
    async def lordupdate(ctx):
        """Zeigt die neuesten Updates des Bots"""
        embed = discord.Embed(
            title="🔄 Bot Updates", 
            description="Die neuesten Änderungen und Verbesserungen", 
            color=0x3498db
        )
        
        embed.add_field(
            name="Version 4.4.3 (Aktuell)",
            value="• Statistiksystem hinzugefügt\n"
                  "• StatsManager-Klasse implementiert\n"
                  "• Fehlerbehebungen und Performance-Verbesserungen",
            inline=False
        )
        
        embed.add_field(
            name="Version 4.4.2",
            value="• Meme-Generator hinzugefügt (!lordmeme)\n"
                  "• Neue Zitate hinzugefügt\n"
                  "• Kontaktsystem verbessert",
            inline=False
        )
        
        embed.set_footer(text=f"Stand: {datetime.datetime.now().strftime('%d.%m.%Y')}")
        
        await ctx.send(embed=embed)

def setup(bot):
    register_update_commands(bot) 