import os
import uuid
import random
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

class MemeGenerator:
    def __init__(self):
        self.image_folder = "/app/data/imgs/drache"  
        self.font_path = "/app/data/fonts/impact.ttf" 
        self.output_folder = "/tmp"

        # Überprüfen der Pfade
        for path in [self.image_folder, self.font_path]:
            if not os.path.exists(path):
                raise RuntimeError(f"Datei/Ordner nicht gefunden: {path}")

    def wrap_text(self, text, font, max_width):
        """Bricht Text um, wenn er zu lang ist"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

    def calculate_font_size(self, text, max_width, max_height, initial_size, font_path):
        """Berechnet die optimale Schriftgröße für den gegebenen Text"""
        font_size = initial_size
        min_font_size = 20  # Minimale Schriftgröße
        
        while font_size > min_font_size:
            font = ImageFont.truetype(font_path, font_size)
            lines = self.wrap_text(text, font, max_width)
            
            bbox = font.getbbox("Ag")
            line_height = bbox[3] - bbox[1] + 10
            total_height = line_height * len(lines)
            
            if total_height <= max_height:
                break
                
            font_size -= 2
            
        return font_size

    def generate_meme(self, text):
        """Erstellt ein Meme mit dem gegebenen Text"""
        # Wähle ein zufälliges Bild aus
        image_path = os.path.join(self.image_folder, random.choice(os.listdir(self.image_folder)))
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        # Initiale Schriftgröße (8% der Bildbreite)
        initial_font_size = int(image.width * 0.08)
        
        # Maximale Breite und Höhe für Text
        max_width = int(image.width * 0.9)
        max_height_top = int(image.height * 0.25)    # 25% der Bildhöhe für oberen Text
        max_height_bottom = int(image.height * 0.25)  # 25% der Bildhöhe für unteren Text

        # Text aufteilen und in Großbuchstaben umwandeln
        if "|" in text:
            top_text, bottom_text = text.split("|", 1)
            top_text = top_text.strip().upper()
            bottom_text = bottom_text.strip().upper()
        else:
            top_text = ""
            bottom_text = text.strip().upper()

        # Berechne optimale Schriftgrößen
        top_font_size = self.calculate_font_size(top_text, max_width, max_height_top, 
                                               initial_font_size, self.font_path) if top_text else initial_font_size
        bottom_font_size = self.calculate_font_size(bottom_text, max_width, max_height_bottom, 
                                                  initial_font_size, self.font_path)

        # Margins
        top_margin = int(image.height * 0.06)
        bottom_margin = int(image.height * 0.12)

        # Zeichne oberen Text
        if top_text:
            font = ImageFont.truetype(self.font_path, top_font_size)
            lines = self.wrap_text(top_text, font, max_width)
            bbox = font.getbbox("Ag")
            line_height = bbox[3] - bbox[1] + 10
            y = top_margin

            for line in lines:
                bbox = font.getbbox(line)
                text_width = bbox[2] - bbox[0]
                x = (image.width - text_width) / 2
                
                # Outline-Effekt
                for adj in range(-3, 4):
                    for adj2 in range(-3, 4):
                        draw.text((x+adj, y+adj2), line, font=font, fill="black")
                draw.text((x, y), line, font=font, fill="white")
                y += line_height

        # Zeichne unteren Text
        if bottom_text:
            font = ImageFont.truetype(self.font_path, bottom_font_size)
            lines = self.wrap_text(bottom_text, font, max_width)
            bbox = font.getbbox("Ag")
            line_height = bbox[3] - bbox[1] + 10
            total_height = line_height * len(lines)
            y = image.height - bottom_margin - total_height

            for line in lines:
                bbox = font.getbbox(line)
                text_width = bbox[2] - bbox[0]
                x = (image.width - text_width) / 2
                
                # Outline-Effekt
                for adj in range(-3, 4):
                    for adj2 in range(-3, 4):
                        draw.text((x+adj, y+adj2), line, font=font, fill="black")
                draw.text((x, y), line, font=font, fill="white")
                y += line_height

        # Bild speichern
        output_path = os.path.join(self.output_folder, f"meme_{uuid.uuid4().hex}.png")
        image.save(output_path)
        return output_path

def register_meme_commands(bot):
    @bot.command(name='lordmeme')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def create_meme(ctx, *, text: str = None):
        """Erstellt ein Drachenlord Meme"""
        if text is None:
            await ctx.send("❌ Du musst einen Text für das Meme angeben!\n"
                          "Beispiel: `!lordmeme Das ist lustig`\n"
                          "Für Text oben und unten: `!lordmeme Oben | Unten`")
            return
            
        try:
            output_path = bot.meme_generator.generate_meme(text)
            await ctx.send(file=discord.File(output_path))
            os.remove(output_path)
        except Exception as e:
            if hasattr(bot, 'logging_channel'):
                channel = bot.get_channel(bot.logging_channel)
                await channel.send(f"Error in meme command: {str(e)}")
            await ctx.send("Ein Fehler ist aufgetreten beim Erstellen des Memes.")

    @create_meme.error
    async def meme_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Du musst einen Text für das Meme angeben!\n"
                          "Beispiel: `!lordmeme Das ist lustig`\n"
                          "Für Text oben und unten: `!lordmeme Oben | Unten`")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏱️ Bitte warte noch {error.retry_after:.1f} Sekunden bis zum nächsten Meme!")
        else:
            await ctx.send("❌ Ein Fehler ist aufgetreten. Überprüfe deine Eingabe.")
            if hasattr(bot, 'logging_channel'):
                channel = bot.get_channel(bot.logging_channel)
                await channel.send(f"Error in lordmeme command: {str(error)}")

def setup(bot):
    # Remove MemeGenerator creation from here
    register_meme_commands(bot)
