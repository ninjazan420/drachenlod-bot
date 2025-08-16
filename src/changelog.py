import discord
from discord.ext import commands
from datetime import datetime
import locale

# Setze deutsche Locale für Datumsformatierung
try:
    locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'German_Germany.1252')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'de_DE')
        except locale.Error:
            # Fallback auf Standard-Locale - robuste Datumsverarbeitung übernimmt
            print("Warning: Konnte deutsche Locale nicht setzen, verwende robuste Datumsverarbeitung")

class ChangelogCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Monatsnamen-Mapping für robuste Datumsverarbeitung
        self.month_mapping = {
            # Englische Monatsnamen
            'January': 'Januar', 'February': 'Februar', 'March': 'März',
            'April': 'April', 'May': 'Mai', 'June': 'Juni',
            'July': 'Juli', 'August': 'August', 'September': 'September',
            'October': 'Oktober', 'November': 'November', 'December': 'Dezember',
            # Deutsche Monatsnamen (für Konsistenz)
            'Januar': 'Januar', 'Februar': 'Februar', 'März': 'März',
            'Mai': 'Mai', 'Juni': 'Juni', 'Juli': 'Juli',
            'Oktober': 'Oktober', 'Dezember': 'Dezember'
        }

        # Changelog data - format: version: {date, features, fixes, notes}
        self.changelog_data = {
            "6.2.0": {
                "date": "16 August 2025",
                "title": "🎮 Gaming Update - Hangman & Snake + AI Memory System",
                "features": [
                    "Neues Hangman-Spiel mit rankings /hangman und /hangman_ranking",
                    "Snake-Spiel mit Highscore-System und verschiedenen Schwierigkeitsgraden",
                    "AI Memory System - KI kann sich jetzt an vorherige Gespräche erinnern",
                    "Verbesserte Stats-Anzeige mit optimierter Performance",
                    "Neue Gaming-Kategorie in der Hilfe mit allen verfügbaren Spielen",
                    "Persistente Speicherung von Spielständen und Highscores"
                ],
                "fixes": [
                    "Stats-System Performance deutlich verbessert",
                    "Memory-Leaks in der Statistik-Anzeige behoben",
                    "Stabilere Datenbank-Verbindungen für Spiele-Daten",
                    "Optimierte Embed-Generierung für bessere Ladezeiten",
                    "Verbesserte Error-Behandlung in allen Gaming-Modulen"
                ],
                "technical": [
                    "Implementierung des Hangman-Systems mit Kategorie-Management",
                    "Snake-Game Engine mit Collision-Detection und Score-Tracking",
                    "AI Memory Backend mit JSON-basierter Persistierung",
                    "Refactoring der Stats-Module für bessere Performance",
                    "Modulare Gaming-Architektur für zukünftige Spiele-Erweiterungen",
                    "Abhängigkeiten geupdated"
                ]
            },
             "6.1.1": {
                "date": "11 Juli 2025",
                "title": "Neues Sprachmodell",
                "fixes": [
                    "Das Sprachmodell von Meta: Llama 4 Maverick auf Meta: Llama 4 Scout umgestellt.",
                    "*Es handelt sich um eine Testphase, da Maverick derzeit zu häufig down ist. Feedback zur Qualität gerne über /kontakt*"
                ]
            },
            "6.1.0": {
                "date": "04 Juli 2025",
                "title": "🔒 Admin Command Visibility & Changelog System Fix",
                "features": [
                    "Fixed admin commands visibility - normal users no longer see admin commands in slash command list",
                    "Re-enabled changelog system with /changelog command",
                    "Removed redundant /lordupdate command - /changelog now handles all update information",
                    "Added proper permission checks using @app_commands.default_permissions(administrator=True)",
                    "Improved command organization and user experience",
                    "Updated bot version to 6.1.0 across all files"
                ],
                "fixes": [
                    "Admin commands now properly hidden from non-admin users",
                    "Changelog commands are now functional again",
                    "Fixed command registration issues",
                    "Improved permission handling for all admin functions",
                    "Updated version numbers throughout the codebase"
                ],
                "technical": [
                    "Added @app_commands.default_permissions(administrator=True) to all admin commands",
                    "Re-enabled register_update_commands in main.py",
                    "Added ChangelogCog registration in main.py",
                    "Removed redundant /lordupdate command from updates.py",
                    "Updated version strings in slash_commands.py and main.py",
                    "Fixed command visibility using Discord's permission system"
                ]
            },
            "6.0.0": {
                "date": "04 Juni 2025",
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
                "date": "02 Juni 2025",
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

    def parse_date_robust(self, date_string):
        """Robuste Datumsverarbeitung für deutsche und englische Monatsnamen"""
        try:
            # Versuche zuerst direktes Parsing
            return datetime.strptime(date_string, "%d %B %Y")
        except ValueError:
            # Falls das fehlschlägt, konvertiere englische zu deutschen Monatsnamen
            for eng_month, ger_month in self.month_mapping.items():
                if eng_month in date_string:
                    german_date = date_string.replace(eng_month, ger_month)
                    try:
                        return datetime.strptime(german_date, "%d %B %Y")
                    except ValueError:
                        continue

            # Fallback: Versuche ISO-Format
            try:
                return datetime.strptime(date_string, "%Y-%m-%d")
            except ValueError:
                # Letzter Fallback: aktuelles Datum
                return datetime.now()

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
            timestamp=self.parse_date_robust(data["date"])
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

        embed.set_footer(text=f"Buttergolem Bot v{version} | Released on {data['date']}")

        # Check if ctx is an Interaction or Context object
        if hasattr(ctx, 'response'):
            # It's an Interaction object
            await ctx.response.send_message(embed=embed, ephemeral=True)
        else:
            # It's a Context object
            await ctx.send(embed=embed)

    async def send_changelog_overview(self, ctx):
        """Send overview of all versions"""
        embed = discord.Embed(
            title="📋 Buttergolem Bot Changelog",
            description="Here's the complete version history of the Buttergolem Discord Bot.\n\nUse `/changelog <version>` for detailed information.",
            color=0xf1c40f
        )

        # Sort versions by date (newest first)
        sorted_versions = sorted(
            self.changelog_data.items(),
            key=lambda x: self.parse_date_robust(x[1]["date"]),
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
                      f"`/changelog {version}` for details",
                inline=True
            )

        embed.add_field(
            name="🔗 Links",
            value="[GitHub Repository](https://github.com/ninjazan420/buttergolem-bot)\n"
                  "[Report Issues](https://github.com/ninjazan420/buttergolem-bot/issues)",
            inline=False
        )

        embed.set_footer(text="Buttergolem | Made with ❤️ by ninjazan420")

        # Check if ctx is an Interaction or Context object
        if hasattr(ctx, 'response'):
            # It's an Interaction object
            await ctx.response.send_message(embed=embed, ephemeral=True)
        else:
            # It's a Context object
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