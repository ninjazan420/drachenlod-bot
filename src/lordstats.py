import discord
import random
from discord.ext import commands

async def create_lordstats_embed(target) -> discord.Embed:
    """Erstellt das Lordstats-Embed für einen User"""
    # Zufällige Werte generieren
    mettkonsum = random.randint(0, 100)
    hater_level = random.randint(0, 10)
    besuche = random.randint(0, 50)
    kaschber_rating = random.randint(0, 100)
    schanzentreue = random.randint(0, 100)
    mullen_index = random.randint(0, 1000)
    
    # Hater-Level als Sterne darstellen
    hater_stars = "⭐" * hater_level + "☆" * (10 - hater_level)
    
    # Zufälliges Zitat laden
    import os
    import json
    quote = "Meddl Leude!"
    try:
        quotes_paths = [
            os.path.join(os.path.dirname(__file__), 'data', 'quotes.json'),
            'src/data/quotes.json',
            'data/quotes.json'
        ]
        
        for quotes_path in quotes_paths:
            if os.path.exists(quotes_path):
                with open(quotes_path, 'r', encoding='utf-8') as f:
                    quotes = json.load(f)
                    if quotes:
                        quote = random.choice(quotes)
                break
    except Exception:
        pass

    embed = discord.Embed(
        title=f"🐷 Lordstats für {target.display_name}",
        description=f"*\"{quote}\"*",
        color=0xff9900
    )
    
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.add_field(name="🥓 Täglicher Mettkonsum", value=f"{mettkonsum}kg", inline=True)
    embed.add_field(name="😡 Hater-Level", value=hater_stars, inline=True)
    embed.add_field(name="🏠 Besuche in Altschauerberg", value=f"{besuche} Mal", inline=True)
    embed.add_field(name="🤪 Kaschber-Rating", value=f"{kaschber_rating}/100", inline=True)
    embed.add_field(name="⚔️ Schanzentreue", value=f"{schanzentreue}%", inline=True)
    embed.add_field(name="📊 Mullen-Index", value=f"{mullen_index} MU", inline=True)
    embed.set_footer(text="Alle Werte sind zu 100% echt und werden von der BLM überwacht")
    
    return embed

def register_lordstats_commands(bot):
    # lordstats befehl entfernt - nur !lord bleibt bestehen

    @bot.tree.command(name="lordstats", description="Zeigt lustige Drachenlord-Statistiken für einen Benutzer")
    async def lordstats_slash(interaction: discord.Interaction, member: discord.Member = None):
        target = member or interaction.user
        embed = await create_lordstats_embed(target)
        await interaction.response.send_message(embed=embed)