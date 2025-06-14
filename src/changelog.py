import discord
from discord.ext import commands
from datetime import datetime

class ChangelogCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # Changelog data - format: version: {date, features, fixes, notes}
        self.changelog_data = {
            "6.0.0": {
                "date": "15 December 2024",
                "title": "🎯 Command Restructuring & Changelog System",
                "features": [
                    "Renamed /help command to /hilfe for German localization",
                    "Added admin permission check for help commands - only shows relevant commands",
                    "Renamed /random command back to /lord for better clarity",
                    "Added !lord command back as traditional prefix command",
                    "Implemented comprehensive changelog system with version tracking",
                    "Added detailed version history with features, fixes, and technical changes"
                ],
                "fixes": [
                    "Fixed admin commands showing to non-admin users in help",
                    "Resolved command conflicts between slash and prefix commands",
                    "Improved command organization and user experience",
                    "Enhanced help system with proper permission filtering"
                ],
                "technical": [
                    "Modified slash_commands.py to rename /help to /hilfe",
                    "Updated /random back to /lord in slash commands",
                    "Added !lord prefix command in sounds.py",
                    "Implemented ChangelogCog with comprehensive version tracking",
                    "Added admin permission validation in help commands",
                    "Created modular changelog system for future updates"
                ]
            },
            "5.4.0": {
                "date": "06 June 2025",
                "title": "🤖 Previous Bot Version",
                "features": [
                    "Basic bot functionality with sound commands",
                    "Meme generation capabilities",
                    "Quiz system implementation",
                    "Stats and monitoring features"
                ],
                "fixes": [
                    "Various bug fixes and improvements",
                    "Performance optimizations",
                    "Discord.py compatibility updates"
                ],
                "technical": [
                    "Core bot architecture established",
                    "Sound system implementation",
                    "Database integration for stats"
                ]
            },

        }
    
    @commands.command(name='changelog')
    async def changelog_command(self, ctx, version=None):
        """Display changelog for specific version or latest versions"""
        
        if version:
            # Show specific version
            if version in self.changelog_data:
                await self.send_version_changelog(ctx, version)
            else:
                embed = discord.Embed(
                    title="❌ Version Not Found",
                    description=f"Version `{version}` not found in changelog.\n\nAvailable versions: {', '.join(self.changelog_data.keys())}",
                    color=0xff0000
                )
                await ctx.send(embed=embed)
        else:
            # Show overview of all versions
            await self.send_changelog_overview(ctx)
    
    async def send_version_changelog(self, ctx, version):
        """Send detailed changelog for a specific version"""
        data = self.changelog_data[version]
        
        embed = discord.Embed(
            title=f"📋 Changelog - Version {version}",
            description=data["title"],
            color=0x00ff00,
            timestamp=datetime.strptime(data["date"], "%d %B %Y")
        )
        
        # Features
        if data.get("features"):
            features_text = "\n".join([f"• {feature}" for feature in data["features"]])
            embed.add_field(
                name="✨ New Features",
                value=features_text[:1024],  # Discord field limit
                inline=False
            )
        
        # Fixes
        if data.get("fixes"):
            fixes_text = "\n".join([f"• {fix}" for fix in data["fixes"]])
            embed.add_field(
                name="🔧 Improvements & Fixes",
                value=fixes_text[:1024],
                inline=False
            )
        
        # Technical
        if data.get("technical"):
            technical_text = "\n".join([f"• {tech}" for tech in data["technical"]])
            embed.add_field(
                name="⚙️ Technical Changes",
                value=technical_text[:1024],
                inline=False
            )
        
        embed.set_footer(text=f"FCKR Bot v{version} | Released on {data['date']}")
        await ctx.send(embed=embed)
    
    async def send_changelog_overview(self, ctx):
        """Send overview of all versions"""
        embed = discord.Embed(
            title="📋 Buttergolem Bot Changelog",
            description="Here's the complete version history of the Buttergolem Discord Bot.\n\nUse `!drache changelog <version>` for detailed information.",
            color=0xf1c40f
        )
        
        # Sort versions by date (newest first)
        sorted_versions = sorted(
            self.changelog_data.items(),
            key=lambda x: datetime.strptime(x[1]["date"], "%d %B %Y"),
            reverse=True
        )
        
        for version, data in sorted_versions:
            feature_count = len(data.get("features", []))
            fix_count = len(data.get("fixes", []))
            
            embed.add_field(
                name=f"🏷️ Version {version}",
                value=f"**{data['title']}**\n"
                      f"📅 Released: {data['date']}\n"
                      f"✨ {feature_count} new features\n"
                      f"🔧 {fix_count} improvements\n"
                      f"`!fckr changelog {version}` for details",
                inline=True
            )
        
        embed.add_field(
            name="🔗 Links",
            value="[GitHub Repository](https://github.com/dermo69/buttergolem)\n"
                  "[Report Issues](https://github.com/dermo69/buttergolem/issues)",
            inline=False
        )
        
        embed.set_footer(text="FCKR Community Bot | Made with ❤️ by ninjazan420")
        await ctx.send(embed=embed)
    
    def add_version(self, version, date, title, features=None, fixes=None, technical=None):
        """Add a new version to changelog (for future updates)"""
        self.changelog_data[version] = {
            "date": date,
            "title": title,
            "features": features or [],
            "fixes": fixes or [],
            "technical": technical or []
        }

def setup(bot):
    bot.add_cog(ChangelogCog(bot))