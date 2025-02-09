import os
import uuid
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
        # ...existing code for generate_meme...
        image_path = os.path.join(self.image_folder, random.choice(os.listdir(self.image_folder)))
        # ...rest of existing generate_meme code...
        return output_path

def register_meme_commands(bot):
    @bot.command(name='lordmeme')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def create_meme(ctx, *, text: str):
        """Erstellt ein Drachenlord Meme"""
        try:
            output_path = bot.meme_generator.generate_meme(text)
            await ctx.send(file=discord.File(output_path))
            os.remove(output_path)
        except Exception as e:
            if hasattr(bot, 'logging_channel'):
                channel = bot.get_channel(bot.logging_channel)
                await channel.send(f"Error in meme command: {str(e)}")
            await ctx.send("Ein Fehler ist aufgetreten beim Erstellen des Memes.")

def setup(bot):
    bot.meme_generator = MemeGenerator()
    register_meme_commands(bot)
