import os
import aiohttp
import asyncio
import logging
import datetime
import discord

log = logging.getLogger("buttergolem.servercounter")

async def update_server_count(client):
    """Updates server count on discords.com every 60minutes"""
    await client.wait_until_ready()
    while True:
        await single_update(client)
        await asyncio.sleep(3600)  # 60 Minuten warten

async def update_member_counter(client):
    """Updates member counter channels every 5 minutes"""
    await client.wait_until_ready()
    while True:
        await update_counter_channels(client)
        await asyncio.sleep(300)  # 5 Minuten warten

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

async def update_counter_channels(client):
    """Aktualisiert die Counter-Kanäle für Member, Server und Uptime"""
    try:
        member_counter_server_id = os.environ.get('MEMBER_COUNTER_SERVER')
        if not member_counter_server_id:
            log.warning("MEMBER_COUNTER_SERVER nicht in Umgebungsvariablen gesetzt")
            return False
            
        guild = client.get_guild(int(member_counter_server_id))
        if not guild:
            log.error(f"Guild mit ID {member_counter_server_id} nicht gefunden")
            return False
            
        # Berechne Stats - Verwende member_count statt members (kein privileged intent nötig)
        total_members = sum(g.member_count for g in client.guilds)
        total_servers = len(client.guilds)
        uptime_hours = int((datetime.datetime.now() - client.start_time).total_seconds() / 3600) if hasattr(client, 'start_time') else 0
        
        # Finde oder erstelle Counter-Kanäle
        await ensure_counter_channel(guild, "📊 Member", f"📊 Member: {total_members:,}")
        await ensure_counter_channel(guild, "🌐 Server", f"🌐 Server: {total_servers:,}")
        await ensure_counter_channel(guild, "⏰ Uptime", f"⏰ Uptime: {uptime_hours}h")
        
        log.info(f"Counter-Kanäle aktualisiert: {total_members} Member, {total_servers} Server, {uptime_hours}h Uptime")
        return True
        
    except Exception as e:
        log.error(f"Fehler beim Aktualisieren der Counter-Kanäle: {str(e)}")
        return False

async def ensure_counter_channel(guild, channel_prefix, new_name):
    """Stellt sicher, dass ein Counter-Kanal existiert und aktualisiert ihn"""
    try:
        # Suche nach existierendem Kanal mit dem Präfix
        existing_channel = None
        for channel in guild.voice_channels:
            if channel.name.startswith(channel_prefix):
                existing_channel = channel
                break
                
        if existing_channel:
            # Aktualisiere den Namen wenn er sich geändert hat
            if existing_channel.name != new_name:
                await existing_channel.edit(name=new_name)
                log.info(f"Kanal '{existing_channel.name}' zu '{new_name}' umbenannt")
        else:
            # Erstelle neuen Voice-Kanal ganz oben
            new_channel = await guild.create_voice_channel(
                name=new_name,
                position=0,
                user_limit=0,  # Kein Limit
                overwrites={
                    guild.default_role: discord.PermissionOverwrite(connect=False),  # Niemand kann joinen
                    guild.me: discord.PermissionOverwrite(connect=True, manage_channels=True)
                }
            )
            log.info(f"Neuer Counter-Kanal erstellt: '{new_name}'")
            
    except Exception as e:
        log.error(f"Fehler beim Verwalten des Counter-Kanals '{channel_prefix}': {str(e)}")
