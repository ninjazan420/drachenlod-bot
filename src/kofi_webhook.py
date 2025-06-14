#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import logging
import datetime
import asyncio
import hmac
import hashlib
from aiohttp import web
import discord
import re

# Logging einrichten
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('kofi_webhook')

class KofiWebhookHandler:
    """
    Handler für Ko-fi Webhooks zur Verarbeitung von Spendenbenachrichtigungen.

    Diese Klasse startet einen einfachen Webserver, der Webhooks von Ko-fi empfängt
    und verarbeitet, um Spenden zu loggen (ohne Premium-Vorteile).
    """

    def __init__(self, client, webhook_token, port=5000):
        """
        Initialisiert den Ko-fi Webhook Handler.

        Args:
            client: Discord Bot Client
            webhook_token: Token zur Verifizierung von Ko-fi Webhooks
            port: Port, auf dem der Webserver laufen soll
        """
        self.client = client
        self.webhook_token = webhook_token
        self.port = port
        self.app = web.Application()

        # Routen hinzufügen
        self.app.add_routes([
            web.get('/', self.handle_root),  # Root-Route für einfache Tests
            web.get('/kofi-webhook', self.handle_root),  # GET für die Webhook-Route
            web.post('/kofi-webhook', self.handle_webhook)  # POST für die Webhook-Route
        ])

        self.runner = None
        self.site = None

    async def start(self):
        """Startet den Webhook-Server"""
        logger.info(f"Starte Ko-fi Webhook-Server auf Port {self.port}")
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, '0.0.0.0', self.port)
        await self.site.start()
        logger.info(f"Ko-fi Webhook-Server läuft auf http://0.0.0.0:{self.port}/kofi-webhook")

    async def handle_root(self, request):
        """
        Verarbeitet Anfragen an die Root-Route.
        Dient als einfache Statusseite und für Tests.

        Args:
            request: Die HTTP-Anfrage

        Returns:
            aiohttp.web.Response: Die HTTP-Antwort
        """
        logger.info(f"Root-Anfrage empfangen: {request.method} {request.path}")

        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ko-fi Webhook Server</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                h1 {{ color: #0066cc; }}
                .status {{ padding: 10px; background-color: #e6f7ff; border-left: 5px solid #0066cc; }}
                pre {{ background-color: #f5f5f5; padding: 10px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>Ko-fi Webhook Server</h1>
            <div class="status">
                <p><strong>Status:</strong> Aktiv und bereit für Webhook-Anfragen</p>
                <p>Der Server ist korrekt konfiguriert und wartet auf POST-Anfragen an <code>/kofi-webhook</code>.</p>
            </div>
            <h2>Konfiguration</h2>
            <p>Stelle sicher, dass in deinem Ko-fi-Dashboard die Webhook-URL korrekt eingerichtet ist:</p>
            <pre>http://deine-server-ip:{port}/kofi-webhook</pre>
            <p>Diese Seite dient nur zur Bestätigung, dass der Server läuft. Alle Zahlungsbenachrichtigungen müssen als POST-Anfragen an den Webhook-Endpunkt gesendet werden.</p>
        </body>
        </html>
        """.format(port=self.port)

        return web.Response(text=html, content_type='text/html')

    async def stop(self):
        """Stoppt den Webhook-Server"""
        if self.site:
            await self.site.stop()
        if self.runner:
            await self.runner.cleanup()
        logger.info("Ko-fi Webhook-Server gestoppt")

    def verify_signature(self, data, signature):
        """
        Verifiziert die Signatur der Ko-fi Webhook-Anfrage.

        Args:
            data: Die Daten der Anfrage
            signature: Die Signatur der Anfrage

        Returns:
            bool: True, wenn die Signatur gültig ist, sonst False
        """
        if not self.webhook_token:
            logger.warning("Kein Webhook-Token konfiguriert, Signatur kann nicht verifiziert werden")
            return True

        computed_signature = hmac.new(
            self.webhook_token.encode(),
            data,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(computed_signature, signature)

    async def handle_webhook(self, request):
        """
        Verarbeitet eingehende Ko-fi Webhook-Anfragen.

        Args:
            request: Die HTTP-Anfrage

        Returns:
            aiohttp.web.Response: Die HTTP-Antwort
        """
        try:
            # Logge die eingehende Anfrage
            logger.info(f"Ko-fi Webhook-Anfrage empfangen: {request.method} {request.path}")
            logger.info(f"Headers: {request.headers}")

            # Prüfe, ob es sich um eine POST-Anfrage handelt
            if request.method != 'POST':
                logger.warning(f"Ungültige Methode für Ko-fi Webhook: {request.method}")
                return web.Response(status=405, text="Methode nicht erlaubt. Verwende POST.")

            # Lese den Request-Body
            body = await request.read()
            logger.info(f"Request-Body: {body}")

            # Prüfe, ob der Body leer ist
            if not body:
                logger.warning("Leerer Request-Body für Ko-fi Webhook")
                return web.Response(status=400, text="Leerer Request-Body")

            # Hole die Signatur aus dem Header (falls vorhanden)
            signature = request.headers.get('X-Kofi-Signature', '')

            # Verifiziere die Signatur
            if not self.verify_signature(body, signature):
                logger.warning("Ungültige Signatur für Ko-fi Webhook")
                return web.Response(status=403, text="Ungültige Signatur")

            # Versuche, die Daten zu parsen
            try:
                # Ko-fi sendet die Daten als Form-Parameter mit einem 'data'-Feld, das JSON enthält
                if request.content_type == 'application/x-www-form-urlencoded':
                    form_data = await request.post()
                    if 'data' in form_data:
                        payload = json.loads(form_data['data'])
                    else:
                        # Versuche, den gesamten Body als JSON zu parsen
                        payload = json.loads(body)
                else:
                    # Versuche, den gesamten Body als JSON zu parsen
                    payload = json.loads(body)

                logger.info(f"Ko-fi Webhook-Daten erfolgreich geparst: {payload}")
            except json.JSONDecodeError as e:
                logger.error(f"Fehler beim Parsen der JSON-Daten: {str(e)}")
                # Versuche, die Daten als Form-Parameter zu parsen
                try:
                    form_data = await request.post()
                    logger.info(f"Form-Daten: {form_data}")
                    if 'data' in form_data:
                        payload = json.loads(form_data['data'])
                    else:
                        return web.Response(status=400, text=f"Ungültiges JSON-Format: {str(e)}")
                except Exception as form_error:
                    logger.error(f"Fehler beim Parsen der Form-Daten: {str(form_error)}")
                    return web.Response(status=400, text=f"Ungültiges Datenformat: {str(e)}")

            # Verarbeite die Zahlung
            await self.process_payment(payload)

            # Erfolgreiche Antwort
            return web.Response(status=200, text="OK")
        except Exception as e:
            logger.error(f"Fehler bei der Verarbeitung des Ko-fi Webhooks: {str(e)}")
            # Logge den Traceback für bessere Fehlerdiagnose
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return web.Response(status=500, text=f"Fehler: {str(e)}")

    async def process_payment(self, payload):
        """
        Verarbeitet eine Ko-fi Spende und loggt sie (ohne Premium-Aktivierung).

        Args:
            payload: Die Daten der Ko-fi Zahlung
        """
        try:
            logger.info(f"Verarbeite Ko-fi Spende: {payload}")

            # Extrahiere relevante Informationen aus dem Payload
            # Ko-fi kann die Daten in verschiedenen Formaten senden
            data = {}

            # Prüfe verschiedene mögliche Formate
            if isinstance(payload, dict):
                if 'data' in payload:
                    # Format: { "data": { ... } }
                    data = payload.get('data', {})
                else:
                    # Format: { ... } (direkte Daten)
                    data = payload

            logger.info(f"Extrahierte Daten: {data}")

            # Prüfe, ob es sich um eine Zahlung handelt
            payment_type = data.get('type', '')
            if payment_type not in ['Donation', 'Subscription', 'Shop Order', 'Commission']:
                logger.info(f"Ignoriere Ko-fi Event vom Typ: {payment_type}")
                # Logge trotzdem im Discord-Kanal für Testzwecke
                await self.log_payment_without_discord_id(data)
                return

            # Extrahiere Informationen
            kofi_transaction_id = data.get('kofi_transaction_id', '')
            email_addr = data.get('email', '')  # Umbenannt, um Konflikte zu vermeiden
            amount = data.get('amount', 0)
            currency = data.get('currency', 'EUR')
            tier_name = data.get('tier_name', '')
            message = data.get('message', '')

            # Logge die extrahierten Informationen
            logger.info(f"Transaktion: {kofi_transaction_id}, Betrag: {amount} {currency}, Tier: {tier_name}, Nachricht: {message}")

            # Suche nach einer Discord-ID im Nachrichtenfeld oder in den URL-Parametern
            discord_id = self.extract_discord_id(message, data)

            if not discord_id:
                logger.warning(f"Keine Discord-ID in der Nachricht oder URL-Parametern gefunden: {message}")
                # Logge die Zahlung im Discord-Kanal
                await self.log_payment_without_discord_id(data)
                return

            logger.info(f"Discord-ID gefunden: {discord_id}")

            # Logge die Spende (ohne Premium-Aktivierung)
            await self.log_donation(discord_id, amount, currency, kofi_transaction_id)

            # Logge die erfolgreiche Spende im Discord-Kanal
            await self.log_successful_donation(discord_id, amount, currency, kofi_transaction_id)

        except Exception as e:
            logger.error(f"Fehler bei der Verarbeitung der Ko-fi Spende: {str(e)}")
            # Logge den Traceback für bessere Fehlerdiagnose
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")

    def extract_discord_id(self, message, data=None):
        """
        Extrahiert eine Discord-ID aus einer Nachricht oder aus den Zahlungsdaten.

        Args:
            message: Die Nachricht, die die Discord-ID enthalten könnte
            data: Die Zahlungsdaten, die die Discord-ID als URL-Parameter enthalten könnten

        Returns:
            str: Die Discord-ID oder None, wenn keine gefunden wurde
        """
        # 1. Suche nach einer Discord-ID (18-stellige Zahl) in der Nachricht
        if message:
            match = re.search(r'(\d{17,20})', message)
            if match:
                return match.group(1)

        # 2. Suche nach einer Discord-ID im from_url Parameter (Ko-fi übergibt URL-Parameter)
        if data and 'from_url' in data:
            from_url = data.get('from_url', '')
            # Suche nach discord_id Parameter in der URL
            match = re.search(r'discord_id=(\d{17,20})', from_url)
            if match:
                return match.group(1)

        # 3. Suche nach einer Discord-ID in der URL-Referenz
        if data and 'url_referrer' in data:
            url_referrer = data.get('url_referrer', '')
            # Suche nach discord_id Parameter in der URL
            match = re.search(r'discord_id=(\d{17,20})', url_referrer)
            if match:
                return match.group(1)

        return None

    # Premium-Funktionalität entfernt - nur noch Spenden-Logging

    async def log_donation(self, discord_id, amount, currency, payment_id):
        """
        Loggt eine Spende ohne Premium-Aktivierung.

        Args:
            discord_id: Die Discord-ID des Spenders (optional)
            amount: Der gespendete Betrag
            currency: Die Währung
            payment_id: Die Zahlungs-ID von Ko-fi
        """
        try:
            logger.info(f"Spende erhalten: {amount} {currency} von Benutzer {discord_id or 'Unbekannt'} (Zahlung: {payment_id})")

            # Versuche, dem Benutzer eine Dankesnachricht zu senden (falls Discord-ID vorhanden)
            if discord_id:
                try:
                    user_id_int = int(discord_id)
                    user = await self.client.fetch_user(user_id_int)
                    if user:
                        await user.send(f"💖 Vielen herzlichen Dank für deine Spende von {amount} {currency}! Deine Unterstützung bedeutet uns sehr viel und hilft dabei, den Bot am Laufen zu halten. ❤️")
                except Exception as e:
                    logger.error(f"Fehler beim Senden der Dankesnachricht an Benutzer {discord_id}: {str(e)}")

        except Exception as e:
            logger.error(f"Fehler beim Loggen der Spende von Benutzer {discord_id}: {str(e)}")

    async def log_payment_without_discord_id(self, data):
        """
        Loggt eine Zahlung ohne Discord-ID im Logging-Kanal.

        Args:
            data: Die Daten der Ko-fi Zahlung
        """
        if not hasattr(self.client, 'logging_channel'):
            logger.warning("Kein Logging-Channel konfiguriert")
            return

        channel = self.client.get_channel(self.client.logging_channel)
        if not channel:
            logger.warning(f"Logging-Channel {self.client.logging_channel} nicht gefunden")
            return

        # Prüfe, ob es ein Test ist
        is_test = "test" in str(data.get('kofi_transaction_id', '')).lower() or "test" in str(data.get('message', '')).lower()

        # Erstelle einen Titel basierend auf dem Typ
        payment_type = data.get('type', 'Unbekannt')
        if payment_type:
            title = f"⚠️ Ko-fi {payment_type} ohne Discord-ID"
        else:
            title = "⚠️ Ko-fi Zahlung ohne Discord-ID"

        if is_test:
            title += " (TEST)"

        embed = discord.Embed(
            title=title,
            description="Eine Ko-fi Zahlung wurde empfangen, aber keine Discord-ID konnte in der Nachricht oder URL-Parametern gefunden werden.",
            color=discord.Color.orange() if not is_test else discord.Color.blue()
        )

        # Füge alle verfügbaren Felder hinzu
        for key, value in data.items():
            # Begrenze die Länge der Werte
            if isinstance(value, str) and len(value) > 1024:
                value = value[:1021] + "..."

            # Formatiere bestimmte Felder speziell
            if key == 'amount':
                currency = data.get('currency', 'EUR')
                embed.add_field(name="Betrag", value=f"{value} {currency}", inline=True)
            elif key in ['email', 'kofi_transaction_id', 'type', 'tier_name']:
                embed.add_field(name=key.capitalize(), value=str(value) or 'Unbekannt', inline=True)
            elif key == 'message':
                embed.add_field(name="Nachricht", value=str(value) or 'Keine Nachricht', inline=False)
            elif key in ['from_url', 'url_referrer']:
                embed.add_field(name=key.replace('_', ' ').capitalize(), value=str(value) or 'Unbekannt', inline=False)

        # Zeitstempel hinzufügen
        embed.set_footer(text=f"Zeitpunkt: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")

        try:
            await channel.send(embed=embed)
            logger.info(f"Zahlung ohne Discord-ID im Logging-Channel geloggt: {data.get('kofi_transaction_id', 'Unbekannt')}")
        except Exception as e:
            logger.error(f"Fehler beim Senden des Embeds: {str(e)}")
            # Versuche, eine einfache Nachricht zu senden
            try:
                await channel.send(f"⚠️ Ko-fi Zahlung ohne Discord-ID empfangen: {data}")
            except Exception as e2:
                logger.error(f"Fehler beim Senden der Fallback-Nachricht: {str(e2)}")

    async def log_successful_donation(self, discord_id, amount, currency, payment_id):
        """
        Loggt eine erfolgreiche Spende im Logging-Kanal.

        Args:
            discord_id: Die Discord-ID des Spenders (optional)
            amount: Der gespendete Betrag
            currency: Die Währung
            payment_id: Die Zahlungs-ID von Ko-fi
        """
        if not hasattr(self.client, 'logging_channel'):
            logger.warning("Kein Logging-Channel konfiguriert")
            return

        channel = self.client.get_channel(self.client.logging_channel)
        if not channel:
            logger.warning(f"Logging-Channel {self.client.logging_channel} nicht gefunden")
            return

        try:
            # Versuche, Benutzerinformationen zu erhalten (falls Discord-ID vorhanden)
            user_name = "Anonymer Spender"
            user_avatar = None
            
            if discord_id:
                try:
                    user = await self.client.fetch_user(int(discord_id))
                    user_name = user.name if user else f"Unbekannt ({discord_id})"
                    user_avatar = user.display_avatar.url if user else None
                except Exception as e:
                    logger.error(f"Fehler beim Abrufen des Benutzers {discord_id}: {str(e)}")
                    user_name = f"Unbekannt ({discord_id})"

            # Prüfe, ob es ein Test ist
            is_test = "test" in str(payment_id).lower() or (discord_id and "test" in user_name.lower())

            embed = discord.Embed(
                title="💖 Spende erhalten" + (" (TEST)" if is_test else ""),
                description=f"Eine Spende von {user_name} wurde erhalten. Vielen Dank für die Unterstützung!",
                color=discord.Color.green() if not is_test else discord.Color.blue()
            )

            if user_avatar:
                embed.set_thumbnail(url=user_avatar)

            embed.add_field(name="Spender", value=f"{user_name}" + (f" ({discord_id})" if discord_id else ""), inline=True)
            embed.add_field(name="Betrag", value=f"{amount} {currency}", inline=True)
            embed.add_field(name="Zahlung", value=payment_id, inline=True)
            embed.add_field(name="Empfangen am", value=datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), inline=True)
            embed.add_field(name="Hinweis", value="Keine Vorteile - nur Unterstützung! ❤️", inline=False)

            embed.set_footer(text=f"Zeitpunkt: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")

            await channel.send(embed=embed)
            logger.info(f"Erfolgreiche Spende im Logging-Channel geloggt: {discord_id or 'Anonym'}, {amount} {currency}, {payment_id}")
        except Exception as e:
            logger.error(f"Fehler beim Loggen der erfolgreichen Spende: {str(e)}")
            # Versuche, eine einfache Nachricht zu senden
            try:
                await channel.send(f"💖 Spende erhalten: {amount} {currency} von {discord_id or 'Anonymer Spender'} (Zahlung: {payment_id})")
            except Exception as e2:
                logger.error(f"Fehler beim Senden der Fallback-Nachricht: {str(e2)}")

def register_kofi_webhook(client):
    """
    Registriert den Ko-fi Webhook-Handler beim Bot.

    Args:
        client: Discord Bot Client
    """
    # Hole den Ko-fi Webhook-Token aus den Umgebungsvariablen
    webhook_token = os.environ.get('KOFI_WEBHOOK_TOKEN', '')
    port = int(os.environ.get('KOFI_WEBHOOK_PORT', '5000'))

    # Erstelle den Webhook-Handler
    webhook_handler = KofiWebhookHandler(client, webhook_token, port)

    # Speichere den Handler im Client
    client.kofi_webhook_handler = webhook_handler
