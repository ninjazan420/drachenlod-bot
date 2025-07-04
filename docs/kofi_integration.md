# Ko-fi Integration für Spenden

Diese Dokumentation beschreibt, wie die Ko-fi-Integration für Spenden des Buttergolem Discord Bots eingerichtet und verwendet wird.

## Übersicht

Der Bot unterstützt die Integration mit Ko-fi, um Spenden zu empfangen und zu loggen. **Wichtig: Spenden bieten keine Vorteile oder Premium-Funktionen - sie dienen nur zur Unterstützung des Bots!**

## Funktionsweise

1. Der Bot startet einen Webhook-Server, der Spendenbenachrichtigungen von Ko-fi empfängt.
2. Wenn eine Spende eingeht, wird sie geloggt und der Spender erhält eine Dankesnachricht.
3. **Keine Premium-Aktivierung oder Vorteile** - nur Unterstützung und Dankbarkeit! ❤️

## Einrichtung in Ko-fi

Um die Ko-fi-Integration einzurichten, müssen folgende Schritte durchgeführt werden:

### 1. Ko-fi-Konto einrichten

Falls noch nicht geschehen, erstelle ein Ko-fi-Konto unter [https://ko-fi.com/](https://ko-fi.com/) und richte deine Zahlungsmethoden ein.

### 2. Spenden-Optionen einrichten

Richte Spenden-Optionen ein (optional - Ko-fi unterstützt auch direkte Spenden):

- **Für regelmäßige Unterstützung:**
  - Gehe zu "Mitgliedschaften" in deinem Ko-fi-Dashboard
  - Erstelle eine Mitgliedschaft für regelmäßige Unterstützung
  - Setze einen aussagekräftigen Titel wie "Bot-Unterstützung" und erkläre, dass es keine Vorteile gibt

- **Für einmalige Spenden:**
  - Gehe zu "Shop" in deinem Ko-fi-Dashboard
  - Erstelle ein Produkt für einmalige Spenden
  - Betone in der Beschreibung, dass es sich um reine Unterstützung ohne Vorteile handelt

### 3. Webhook einrichten

1. Gehe zu "Einstellungen" > "API" in deinem Ko-fi-Dashboard
2. Aktiviere die Webhook-Funktion
3. Trage die URL deines Webhook-Servers ein: `http://deine-server-ip:5000/kofi-webhook`
4. Kopiere den Webhook-Verifizierungstoken

### 4. Bot-Konfiguration

Aktualisiere die Umgebungsvariablen in der `docker-compose.yml`-Datei:

```yaml
# Port-Freigabe für den Ko-fi Webhook-Server
ports:
  - "5000:5000" # Port für den Ko-fi Webhook-Server

# Ko-fi URLs für Spenden
KOFI_URL: "https://ko-fi.com/buttergolem"  # Hauptseite für Spenden
KOFI_TIP_URL: "https://ko-fi.com/buttergolem/tip"  # Direkte Spenden
KOFI_WEBHOOK_TOKEN: "dein-webhook-token" # Wird für die Verifizierung von Ko-fi Webhooks verwendet
KOFI_WEBHOOK_PORT: "5000" # Port für den Ko-fi Webhook-Server
```

**Wichtig:** Stelle sicher, dass der Port 5000 in deiner Firewall freigegeben ist, damit Ko-fi den Webhook-Server erreichen kann.

## Verwendung durch Benutzer

### Anleitung für Benutzer

Benutzer können den Bot über folgende Schritte unterstützen:

1. Verwende den Befehl `!hilfe` im Discord-Chat
2. Klicke auf den Ko-fi Spenden-Link im Hilfe-Embed
3. Spende einen beliebigen Betrag
4. **Keine Vorteile oder Premium-Funktionen** - nur Dankbarkeit! ❤️

### Discord-ID Übermittlung (Optional)

Falls du möchtest, dass der Bot weiß, wer gespendet hat, kannst du deine Discord-ID im Nachrichtenfeld bei der Spende angeben.

So findest du deine Discord-ID:

1. Aktiviere den Entwicklermodus in Discord (Einstellungen > Erweitert > Entwicklermodus)
2. Rechtsklick auf den eigenen Namen > "ID kopieren"
3. Füge die ID in das Nachrichtenfeld bei Ko-fi ein

## Fehlerbehebung

### Spende wird nicht erkannt

Wenn eine Spende nicht im Bot-Log erscheint:

1. Prüfe, ob der Webhook-Server läuft (Logging-Kanal sollte eine Meldung anzeigen)
2. Prüfe die Webhook-URL in den Ko-fi-Einstellungen
3. Prüfe den Webhook-Token in der Bot-Konfiguration

## Technische Details

### Webhook-Server

Der Webhook-Server läuft auf Port 5000 und empfängt POST-Anfragen auf dem Pfad `/kofi-webhook`. Er verifiziert die Anfragen mit dem Webhook-Token und loggt dann die Spenden.

Der Server bietet auch eine einfache Statusseite unter der Root-URL (`http://deine-server-ip:5000/`), die bestätigt, dass der Server läuft und korrekt konfiguriert ist.

#### Datenformat

Ko-fi sendet die Daten im Format `application/x-www-form-urlencoded` mit einem Feld namens `data`, das einen JSON-String enthält. Der Server kann sowohl dieses Format als auch direkte JSON-Anfragen verarbeiten.

### Spenden-Logging

Alle Spenden werden geloggt und der Spender erhält eine Dankesnachricht (falls Discord-ID angegeben). **Keine Premium-Aktivierung oder Vorteile!**

### Sicherheit

Der Webhook-Server verifiziert die Anfragen mit dem Webhook-Token, um sicherzustellen, dass nur legitime Anfragen von Ko-fi verarbeitet werden.

## Support

Bei Problemen mit der Ko-fi-Integration wende dich an den Bot-Entwickler oder erstelle ein Issue im GitHub-Repository.
5000