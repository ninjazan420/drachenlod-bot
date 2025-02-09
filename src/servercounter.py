import os
import aiohttp
import asyncio
import logging
import datetime

log = logging.getLogger("buttergolem.servercounter")

async def update_server_count(client):
    """Updates server count on discords.com every 30 minutes"""
    await client.wait_until_ready()
    while True:
        await single_update(client)
        await asyncio.sleep(3600)  # 60 Minuten warten

async def single_update(client):
    """Führt ein einzelnes Servercount Update durch"""
    try:
        api_token = os.environ.get('DISCORDS_KEY')
        if not api_token:
            if hasattr(client, 'logging_channel'):
                channel = client.get_channel(client.logging_channel)
                await channel.send("```\n⚠️ DISCORDS_KEY nicht gesetzt in Umgebungsvariablen```")
            return False

        async with aiohttp.ClientSession() as session:
            # Korrigierte URL mit /setservers
            url = f"https://discords.com/bots/api/bot/1329104199794954240/setservers"
            headers = {
                "Authorization": api_token,
                "Content-Type": "application/json"
            }
            data = {"server_count": len(client.guilds)}
            
            async with session.post(url, headers=headers, json=data) as resp:
                if resp.status == 200:
                    log.info(f"Server count erfolgreich aktualisiert: {len(client.guilds)}")
                    if hasattr(client, 'logging_channel'):
                        channel = client.get_channel(client.logging_channel)
                        if channel:
                            await channel.send(f"```\n{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} # ✅ Servercount Update erfolgreich! Aktuelle Server: {len(client.guilds)}```")
                    return True
                else:
                    error_text = await resp.text()
                    log.error(f"Fehler beim Aktualisieren des Server counts: Status {resp.status}, Response: {error_text}")
                    if hasattr(client, 'logging_channel'):
                        channel = client.get_channel(client.logging_channel)
                        await channel.send(f"```\n❌ Fehler beim Servercount Update: Status {resp.status}\nAntwort: {error_text}```")
                    return False
                    
    except Exception as e:
        log.error(f"Fehler beim Server count Update: {str(e)}")
        if hasattr(client, 'logging_channel'):
            channel = client.get_channel(client.logging_channel)
            await channel.send(f"```\n❌ Fehler beim Servercount Update: {str(e)}```")
        return False
