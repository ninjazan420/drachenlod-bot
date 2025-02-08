import os
import json
import random
from PIL import Image, ImageDraw, ImageFont

class MemeGenerator:
    def __init__(self):
        self.image_folder = "/app/data/imgs/drache"  
        self.font_path = "/app/data/fonts/impact.ttf" 
        self.output_folder = "/tmp"
        self.quotes_file = "/app/data/quotes.json"  # Neu: Pfad zur quotes.json

        # Überprüfen der Pfade
        for path in [self.image_folder, self.font_path, self.quotes_file]:
            if not os.path.exists(path):
                raise RuntimeError(f"Datei/Ordner nicht gefunden: {path}")
        
        # Quotes laden
        with open(self.quotes_file, 'r', encoding='utf-8') as f:
            self.quotes = json.load(f)

    def get_random_quote(self):
        """Gibt ein zufälliges Zitat zurück"""
        return random.choice(self.quotes)

    def split_text(self, text):
        if "|" in text:
            top, bottom = text.split("|", 1)
            return top.strip(), bottom.strip()
        elif " " in text:  # Mehr als ein Wort
            words = text.split()
            mid = len(words) // 2
            return " ".join(words[:mid]), " ".join(words[mid:])
        else:  # Einzelnes Wort
            return text, ""

    def add_text_to_image(self, draw, text, x, y, font, width):
        """Fügt Text mit schwarzem Umriss hinzu"""
        outline_width = 3
        for offset_x in range(-outline_width, outline_width+1):
            for offset_y in range(-outline_width, outline_width+1):
                draw.text((x + offset_x, y + offset_y), text, font=font, fill='black')
        draw.text((x, y), text, font=font, fill='white')

    def generate_meme(self, text):
        # Text in oben/unten aufteilen
        top_text, bottom_text = self.split_text(text)
        top_text = top_text.upper()
        bottom_text = bottom_text.upper()
        
        # Zufälliges Zitat als zusätzlichen Text
        quote = self.get_random_quote()
        
        # Wähle zufälliges Bild aus dem Ordner
        image_files = [f for f in os.listdir(self.image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
        if not image_files:
            raise RuntimeError("Keine Bilder im Ordner gefunden")
        
        image_file = random.choice(image_files)
        image_path = os.path.join(self.image_folder, image_file)
        
        # Öffne das Bild
        with Image.open(image_path) as img:
            meme = img.copy()
            draw = ImageDraw.Draw(meme)
            
            # Berechne die Schriftgrößen
            title_size = int(meme.width * 0.08)  # 8% der Bildbreite für Haupt-Text
            quote_size = int(meme.width * 0.04)  # 4% der Bildbreite für Zitat
            
            title_font = ImageFont.truetype(self.font_path, title_size)
            quote_font = ImageFont.truetype(self.font_path, quote_size)
            
            # Oberer Text
            if top_text:
                bbox = title_font.getbbox(top_text)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                x = (meme.width - text_width) / 2
                y = 10
                self.add_text_to_image(draw, top_text, x, y, title_font, text_width)
            
            # Unterer Text
            if bottom_text:
                bbox = title_font.getbbox(bottom_text)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                x = (meme.width - text_width) / 2
                y = meme.height - text_height - 10
                self.add_text_to_image(draw, bottom_text, x, y, title_font, text_width)
            
            # Zitat hinzufügen
            bbox = quote_font.getbbox(quote)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (meme.width - text_width) / 2
            y = meme.height - text_height - 60  # Etwas über dem unteren Text
            self.add_text_to_image(draw, quote, x, y, quote_font, text_width)
            
            # Speichere das Meme
            output_path = os.path.join(self.output_folder, f"meme_{os.path.splitext(image_file)[0]}.png")
            meme.save(output_path)
            
            return output_path
