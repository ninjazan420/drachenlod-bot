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
            name="Version 4.5.0 (Aktuell)",
            value="• Befehle `!server` und `!user` wurden zu einem verbesserten `!user` Befehl zusammengeführt\n"
                  "• Verbesserte Fehlerbehandlung bei Slash-Befehlen hinzugefügt\n"
                  "• Übermäßige Log-Ausgaben bei Voice-Handshakes reduziert\n"
                  "• Besseres Nutzer-Feedback bei Berechtigungsfehlern",
            inline=False
        )
        
        embed.add_field(
            name="Version 4.4.3",
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
        
        embed.set_footer(text=f"Stand: {datetime.datetime.now().strftime('%d.%m.%Y')} | Support-Server: discord.gg/7J4mgSyB8n")
        
        await ctx.send(embed=embed)

    @bot.tree.command(name="lordupdate", description="Zeigt die neuesten Updates des Bots")
    async def lordupdate_slash(interaction: discord.Interaction):
        """Zeigt die neuesten Updates des Bots als Slash-Befehl"""
        try:
            embed = discord.Embed(
                title="🔄 Bot Updates", 
                description="Die neuesten Änderungen und Verbesserungen", 
                color=0x3498db
            )
            
            embed.add_field(
                name="Version 4.5.0 (Aktuell)",
                value="• Befehle `!server` und `!user` wurden zu einem verbesserten `!user` Befehl zusammengeführt\n"
                      "• Verbesserte Fehlerbehandlung bei Slash-Befehlen hinzugefügt\n"
                      "• Übermäßige Log-Ausgaben bei Voice-Handshakes reduziert\n"
                      "• Besseres Nutzer-Feedback bei Berechtigungsfehlern",
                inline=False
            )
            
            embed.add_field(
                name="Version 4.4.3",
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
            
            embed.set_footer(text=f"Stand: {datetime.datetime.now().strftime('%d.%m.%Y')} | Support-Server: discord.gg/7J4mgSyB8n")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(
                "❌ Bei der Ausführung des Befehls ist ein Fehler aufgetreten.",
                ephemeral=True
            )
            if hasattr(bot, 'logging_channel'):
                channel = bot.get_channel(bot.logging_channel)
                if channel:
                    await channel.send(f"```\nFehler beim Update-Befehl: {str(e)}```")

def setup(bot):
    register_update_commands(bot)

async def process_command(message, command_name):
    # ... existing code ...
    
    # Vor dem Senden der Logging-Nachricht überprüfen, ob der Benutzer ein Admin ist
    if not message.author.guild_permissions.administrator:
        logging_channel = client.get_channel(LOGGING_CHANNEL_ID)
        if logging_channel:
            await logging_channel.send(f"Benutzer {message.author.name} hat den Befehl `{command_name}` ausgeführt.")
    
    # ... existing code ... 