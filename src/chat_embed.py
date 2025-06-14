import discord
from discord.ui import View, Button

class ChatPaginationView(View):
    """
    Eine View-Klasse für die Paginierung von Chat-Nachrichten.
    Zeigt Anfrage und Antwort in einem Embed mit Blätter-Buttons an.
    """
    def __init__(self, user, bot_user, prompt, response, context=None):
        super().__init__(timeout=300)  # 5 Minuten Timeout
        self.user = user
        self.bot_user = bot_user
        self.prompt = prompt
        self.response = response
        self.context = context or {}
        self.current_page = 1
        self.total_pages = 2  # Anfrage und Antwort

        # Buttons hinzufügen
        self.add_navigation_buttons()

    def add_navigation_buttons(self):
        """Fügt die Navigationsbuttons zur View hinzu."""
        # Zurück-Button
        back_button = Button(
            style=discord.ButtonStyle.secondary,
            emoji="◀️",
            custom_id="previous_page",
            disabled=(self.current_page == 1)
        )
        back_button.callback = self.previous_page
        self.add_item(back_button)

        # Weiter-Button
        next_button = Button(
            style=discord.ButtonStyle.secondary,
            emoji="▶️",
            custom_id="next_page",
            disabled=(self.current_page == self.total_pages)
        )
        next_button.callback = self.next_page
        self.add_item(next_button)

    async def previous_page(self, interaction):
        """Callback für den Zurück-Button."""
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("Du kannst nur deine eigenen Nachrichten durchblättern!", ephemeral=True)
            return

        if self.current_page > 1:
            self.current_page -= 1
            # View aktualisieren (Buttons neu erstellen)
            self.clear_items()
            self.add_navigation_buttons()
            # Embed aktualisieren
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
        else:
            await interaction.response.defer()

    async def next_page(self, interaction):
        """Callback für den Weiter-Button."""
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("Du kannst nur deine eigenen Nachrichten durchblättern!", ephemeral=True)
            return

        if self.current_page < self.total_pages:
            self.current_page += 1
            # View aktualisieren (Buttons neu erstellen)
            self.clear_items()
            self.add_navigation_buttons()
            # Embed aktualisieren
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
        else:
            await interaction.response.defer()

    def create_embed(self):
        """Erstellt das Embed basierend auf der aktuellen Seite."""
        # Zeitstempel für das Embed
        timestamp = discord.utils.utcnow()

        if self.current_page == 1:
            # Anfrage-Seite
            title = "🤖 KI-Anfrage"
            color = 0x3498db  # Blau
            content = self.prompt
            author = self.user
            footer_text = f"Anfrage • Seite {self.current_page}/{self.total_pages}"
        else:
            # Antwort-Seite
            title = "🤖 KI-Antwort"
            color = 0x2ecc71  # Grün
            content = self.response
            author = self.bot_user
            footer_text = f"Antwort • Seite {self.current_page}/{self.total_pages}"

        # Nachricht auf 4000 Zeichen begrenzen (Discord-Limit für Embed-Beschreibungen)
        if len(content) > 4000:
            description = f"{content[:3997]}..."
        else:
            description = content

        # Embed erstellen
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=timestamp
        )

        # Autor-Informationen hinzufügen
        embed.set_author(
            name=f"{author.display_name} ({author.id})",
            icon_url=author.display_avatar.url
        )

        # Server- und Kanalinformationen hinzufügen, falls vorhanden
        if "channel_name" in self.context:
            embed.add_field(name="Kanal", value=self.context["channel_name"], inline=True)
        if "guild_name" in self.context:
            embed.add_field(name="Server", value=self.context["guild_name"], inline=True)

        # Footer mit Seitenzahl
        embed.set_footer(text=footer_text)

        return embed

async def send_chat_embed(message, prompt, response):
    """
    Sendet ein Chat-Embed mit Paginierung.

    Args:
        message: Die Discord-Nachricht
        prompt: Der Prompt/die Anfrage des Benutzers
        response: Die Antwort des Bots
    """
    # Kontext für das Embed
    context = {
        "channel_name": "Direktnachricht" if isinstance(message.channel, discord.DMChannel) else f"#{message.channel.name} ({message.channel.id})",
        "guild_name": "DM" if isinstance(message.channel, discord.DMChannel) else f"{message.guild.name} ({message.guild.id})"
    }

    # View erstellen
    view = ChatPaginationView(
        user=message.author,
        bot_user=message.guild.me if message.guild else message.channel.me,
        prompt=prompt,
        response=response,
        context=context
    )

    # Embed erstellen und senden
    embed = view.create_embed()
    await message.reply(embed=embed, view=view)

# Funktion zum Protokollieren von KI-Interaktionen im Logging-Channel mit Pagination
async def log_ki_interaction_paginated(client, message, prompt, response):
    """
    Protokolliert KI-Interaktionen im Logging-Channel als blätterbares Embed.

    Args:
        client: Der Discord-Bot-Client
        message: Die Discord-Nachricht
        prompt: Der Prompt/die Anfrage des Benutzers
        response: Die Antwort des Bots
    """
    # Logging-Channel abrufen
    logging_channel = client.get_channel(client.logging_channel)
    if not logging_channel:
        return

    # Kontext für das Embed
    context = {
        "channel_name": "Direktnachricht" if isinstance(message.channel, discord.DMChannel) else f"#{message.channel.name} ({message.channel.id})",
        "guild_name": "DM" if isinstance(message.channel, discord.DMChannel) else f"{message.guild.name} ({message.guild.id})"
    }

    # View erstellen
    view = ChatPaginationView(
        user=message.author,
        bot_user=client.user,
        prompt=prompt,
        response=response,
        context=context
    )

    # Embed erstellen und senden
    embed = view.create_embed()
    await logging_channel.send(embed=embed, view=view)

# Alte Funktion für Abwärtskompatibilität beibehalten
async def log_ki_interaction(client, message, prompt, response=None, is_request=True):
    """
    Protokolliert KI-Interaktionen im Logging-Channel als Embed.
    Diese Funktion ist veraltet und wird nur für Abwärtskompatibilität beibehalten.
    Bitte verwende stattdessen log_ki_interaction_paginated.

    Args:
        client: Der Discord-Bot-Client
        message: Die Discord-Nachricht
        prompt: Der Prompt/die Anfrage des Benutzers
        response: Die Antwort des Bots (nur für Antwort-Embeds)
        is_request: True für Anfrage-Embeds, False für Antwort-Embeds
    """
    # Wenn es eine Antwort gibt, verwende die neue paginierte Funktion
    if not is_request and response:
        await log_ki_interaction_paginated(client, message, prompt, response)
        return

    # Ansonsten verwende die alte Methode für Anfragen ohne Antwort
    # Logging-Channel abrufen
    logging_channel = client.get_channel(client.logging_channel)
    if not logging_channel:
        return

    # Zeitstempel für das Embed
    timestamp = discord.utils.utcnow()

    # Farbe basierend auf Anfrage oder Antwort
    color = 0x3498db if is_request else 0x2ecc71  # Blau für Anfragen, Grün für Antworten

    # Titel und Beschreibung basierend auf Anfrage oder Antwort
    if is_request:
        title = "🤖 KI-Anfrage"
        # Nachricht auf 4000 Zeichen begrenzen (Discord-Limit für Embed-Beschreibungen)
        if len(prompt) > 4000:
            description = f"**Nachricht:**\n{prompt[:3997]}..."
        else:
            description = f"**Nachricht:**\n{prompt}"
    else:
        title = "🤖 KI-Antwort"
        # Antwort auf 4000 Zeichen begrenzen (Discord-Limit für Embed-Beschreibungen)
        if len(response) > 4000:
            description = f"**Antwort:**\n{response[:3997]}..."
        else:
            description = f"**Antwort:**\n{response}"

    # Embed erstellen
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=timestamp
    )

    # Benutzerinformationen hinzufügen
    if is_request:
        embed.set_author(
            name=f"{message.author.display_name} ({message.author.id})",
            icon_url=message.author.display_avatar.url
        )
    else:
        embed.set_author(
            name=f"{client.user.name} ({client.user.id})",
            icon_url=client.user.display_avatar.url
        )

    # Server- und Kanalinformationen hinzufügen
    if isinstance(message.channel, discord.DMChannel):
        embed.add_field(name="Kanal", value="Direktnachricht", inline=True)
        embed.add_field(name="Server", value="DM", inline=True)
    else:
        embed.add_field(name="Kanal", value=f"#{message.channel.name} ({message.channel.id})", inline=True)
        embed.add_field(name="Server", value=f"{message.guild.name} ({message.guild.id})", inline=True)

    # Zeitstempel und Typ der Interaktion hinzufügen
    interaction_type = "Anfrage" if is_request else "Antwort"
    embed.set_footer(text=f"{interaction_type} • {timestamp.strftime('%d.%m.%Y %H:%M:%S')}")

    # Embed senden
    await logging_channel.send(embed=embed)
