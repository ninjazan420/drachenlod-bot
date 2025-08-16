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

    def add_watermark(self, image, draw):
        """Fügt ein dezentes Wasserzeichen hinzu"""
        watermark_text = "@Buttergolem"

        # Kleine Schriftgröße für das Wasserzeichen (2% der Bildbreite)
        watermark_font_size = max(12, int(image.width * 0.02))

        try:
            watermark_font = ImageFont.truetype(self.font_path, watermark_font_size)
        except:
            # Fallback auf Standard-Font falls Impact nicht verfügbar
            watermark_font = ImageFont.load_default()

        # Position: Unten rechts mit kleinem Abstand
        bbox = watermark_font.getbbox(watermark_text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = image.width - text_width - 10  # 10px Abstand vom rechten Rand
        y = image.height - text_height - 10  # 10px Abstand vom unteren Rand

        # Halbtransparenter Hintergrund für bessere Lesbarkeit
        overlay = Image.new('RGBA', (text_width + 8, text_height + 4), (0, 0, 0, 128))
        image.paste(overlay, (x - 4, y - 2), overlay)

        # Wasserzeichen-Text in weiß mit leichtem Schatten
        draw.text((x + 1, y + 1), watermark_text, font=watermark_font, fill=(0, 0, 0, 180))  # Schatten
        draw.text((x, y), watermark_text, font=watermark_font, fill=(255, 255, 255, 200))  # Text

    def generate_meme(self, text, position="top"):
        """Erstellt ein Meme mit dem gegebenen Text"""
        # Wähle ein zufälliges Bild aus
        image_path = os.path.join(self.image_folder, random.choice(os.listdir(self.image_folder)))
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        # Initiale Schriftgröße (8% der Bildbreite)
        initial_font_size = int(image.width * 0.08)
        
        # Maximale Breite und Höhe für Text
        max_width = int(image.width * 0.9)
        max_height_top = int(image.height * 0.15)    # 25% der Bildhöhe für oberen Text
        max_height_bottom = int(image.height * 0.15)  # 25% der Bildhöhe für unteren Text

        # Text aufteilen und in Großbuchstaben umwandeln basierend auf Position
        if position == "both":
            if "|" in text:
                top_text, bottom_text = text.split("|", 1)
                top_text = top_text.strip().upper()
                bottom_text = bottom_text.strip().upper()
            else:
                # Wenn kein | vorhanden, Text auf beide Positionen
                top_text = text.strip().upper()
                bottom_text = ""
        elif position == "top":
            top_text = text.strip().upper()
            bottom_text = ""
        elif position == "bottom":
            top_text = ""
            bottom_text = text.strip().upper()
        else:
            # Fallback auf oben
            top_text = text.strip().upper()
            bottom_text = ""

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

        # Wasserzeichen hinzufügen
        self.add_watermark(image, draw)

        # Bild speichern
        output_path = os.path.join(self.output_folder, f"meme_{uuid.uuid4().hex}.png")
        image.save(output_path)
        return output_path

def register_meme_commands(bot):
    # lordmeme befehl entfernt - nur !lord bleibt bestehen
    # Error handler entfernt da kein create_meme command mehr existiert
    pass

def setup(bot):
    # Remove MemeGenerator creation from here
    register_meme_commands(bot)
