import discord
import math
from datetime import datetime

class ServerListView(discord.ui.View):
    def __init__(self, ctx, guilds, admin_user_id, logging_channel, server_id_map):
        super().__init__(timeout=300)  # 5 Minuten Timeout
        self.ctx = ctx
        self.guilds = guilds
        self.admin_user_id = admin_user_id
        self.logging_channel = logging_channel
        self.server_id_map = server_id_map
        self.current_page = 1
        self.items_per_page = 10
        self.total_pages = math.ceil(len(guilds) / self.items_per_page)
        self.sort_by = "name"  # "name", "members", "id"
        self.sort_reverse = False
        self.message = None
        
        # Sortiere die Server initial nach Namen
        self._sort_guilds()
        
        # Update button states
        self._update_buttons()

    def _sort_guilds(self):
        """Sortiert die Server-Liste basierend auf dem aktuellen Sortierkriterium"""
        if self.sort_by == "name":
            self.guilds.sort(key=lambda g: g.name.lower(), reverse=self.sort_reverse)
        elif self.sort_by == "members":
            self.guilds.sort(key=lambda g: g.member_count or 0, reverse=self.sort_reverse)
        elif self.sort_by == "id":
            self.guilds.sort(key=lambda g: g.id, reverse=self.sort_reverse)
        
        # Aktualisiere die total_pages nach dem Sortieren
        self.total_pages = math.ceil(len(self.guilds) / self.items_per_page)
        
        # Stelle sicher, dass current_page gültig ist
        if self.current_page > self.total_pages:
            self.current_page = max(1, self.total_pages)

    def _update_buttons(self):
        """Aktualisiert den Status der Buttons basierend auf der aktuellen Seite"""
        # Previous button
        self.previous_button.disabled = self.current_page <= 1
        
        # Next button
        self.next_button.disabled = self.current_page >= self.total_pages
        
        # Page info button
        self.page_info.label = f"Seite {self.current_page}/{self.total_pages}"

    def create_embed(self):
        """Erstellt das Embed für die aktuelle Seite"""
        embed = discord.Embed(
            title="🖥️ Server-Liste",
            description=f"Sortiert nach: {self.sort_by} ({'absteigend' if self.sort_reverse else 'aufsteigend'})",
            color=0x3498db,
            timestamp=datetime.now()
        )
        
        # Berechne Start- und End-Index für die aktuelle Seite
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.guilds))
        
        # Füge Server-Informationen hinzu (kompakt, ein Server pro Zeile)
        server_list = []
        for i in range(start_idx, end_idx):
            guild = self.guilds[i]
            
            # Finde die fortlaufende ID für diesen Server
            seq_id = None
            for sid, gid in self.server_id_map.items():
                if gid == guild.id:
                    seq_id = sid
                    break
            
            # Server-Name kürzen falls zu lang
            server_name = guild.name[:25] + "..." if len(guild.name) > 25 else guild.name
            member_count = guild.member_count or 0
            
            # Kompakte Zeile pro Server
            server_line = f"`{i + 1:2}.` **{server_name}** | ID: `{guild.id}` | Seq: `{seq_id or 'N/A'}` | 👥 {member_count} | 📝 {len(guild.text_channels)} | 🔊 {len(guild.voice_channels)}"
            server_list.append(server_line)
        
        # Alle Server in einem Feld zusammenfassen
        if server_list:
            embed.add_field(
                name="📋 Server-Übersicht",
                value="\n".join(server_list),
                inline=False
            )
        
        # Footer mit Gesamtinformationen
        embed.set_footer(
            text=f"Gesamt: {len(self.guilds)} Server | Seite {self.current_page}/{self.total_pages}"
        )
        
        return embed

    @discord.ui.button(label="◀️ Zurück", style=discord.ButtonStyle.secondary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.admin_user_id:
            await interaction.response.send_message("❌ Nur der Administrator kann diese Buttons verwenden!", ephemeral=True)
            return
        
        if self.current_page > 1:
            self.current_page -= 1
            self._update_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="Seite 1/1", style=discord.ButtonStyle.primary, disabled=True)
    async def page_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

    @discord.ui.button(label="Weiter ▶️", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.admin_user_id:
            await interaction.response.send_message("❌ Nur der Administrator kann diese Buttons verwenden!", ephemeral=True)
            return
        
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._update_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="📝 Nach Name", style=discord.ButtonStyle.success)
    async def sort_by_name(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.admin_user_id:
            await interaction.response.send_message("❌ Nur der Administrator kann diese Buttons verwenden!", ephemeral=True)
            return
        
        if self.sort_by == "name":
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_by = "name"
            self.sort_reverse = False
        
        self._sort_guilds()
        self.current_page = 1
        self._update_buttons()
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

    @discord.ui.button(label="👥 Nach Mitgliedern", style=discord.ButtonStyle.success)
    async def sort_by_members(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.admin_user_id:
            await interaction.response.send_message("❌ Nur der Administrator kann diese Buttons verwenden!", ephemeral=True)
            return
        
        if self.sort_by == "members":
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_by = "members"
            self.sort_reverse = True  # Standard: Höchste Mitgliederzahl zuerst
        
        self._sort_guilds()
        self.current_page = 1
        self._update_buttons()
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

    async def on_timeout(self):
        """Wird aufgerufen, wenn die View das Timeout erreicht"""
        # Deaktiviere alle Buttons
        for item in self.children:
            item.disabled = True
        
        # Aktualisiere die Nachricht, falls sie noch existiert
        if self.message:
            try:
                await self.message.edit(view=self)
            except:
                pass  # Nachricht wurde möglicherweise gelöscht