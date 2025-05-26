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

    embed = discord.Embed(
        title=f"🐷 Lordstats für {target.display_name}",
        color=0xff9900,
        timestamp=discord.utils.utcnow()
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
    @bot.command(name='lordstats')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lordstats(ctx, member: discord.Member = None):
        """Zeigt lustige Drachenlord-Statistiken für einen Benutzer"""
        target = member or ctx.author
        embed = await create_lordstats_embed(target)
        await ctx.send(embed=embed)

    @bot.tree.command(name="lordstats", description="Zeigt lustige Drachenlord-Statistiken für einen Benutzer")
    async def lordstats_slash(interaction: discord.Interaction, member: discord.Member = None):
        target = member or interaction.user
        embed = await create_lordstats_embed(target)
        await interaction.response.send_message(embed=embed) 