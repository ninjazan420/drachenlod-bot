import json
import random
import asyncio
import discord
from discord.ext import commands

def load_questions():
    with open('/app/data/questions.json', 'r', encoding='utf-8') as file:
        return json.load(file)

class QuizParticipant:
    def __init__(self, user):
        self.user = user
        self.score = 0
        self.has_answered = False

class QuizGame:
    def __init__(self, rounds=5):
        self.participants = {}  # {user_id: QuizParticipant}
        self.current_question = None
        self.message = None
        self.active = True
        self.rounds = rounds
        self.current_round = 0

# Globale Variable für aktive Spiele
active_games = {}  # {channel_id: {user_id: QuizGame}}
emoji_numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
questions = load_questions()

async def show_quiz_help(ctx):
    help_text = (
        "**🎮 Drachenlord Quiz Hilfe 🎮**\n\n"
        "`!lordquiz start <anzahl>` - Startet ein neues Quiz mit gewünschter Rundenzahl\n"
        "`!lordquiz stop` - Beendet das aktuelle Quiz\n\n"
        "Beispiel: `!lordquiz start 5` für ein Quiz mit 5 Fragen"
    )
    await ctx.send(help_text)

async def collect_participants(ctx, game):
    """Sammelt Teilnehmer für das Quiz"""
    signup_msg = await ctx.send(
        "🎮 **Neue Quiz-Runde startet!**\n"
        "Reagiere mit ✅ um teilzunehmen!\n"
        "Start in 20 Sekunden..."
    )
    await signup_msg.add_reaction("✅")
    
    await asyncio.sleep(20)  # 20 Sekunden Wartezeit
    
    # Hole aktualisierte Nachricht um alle Reaktionen zu sehen
    signup_msg = await ctx.channel.fetch_message(signup_msg.id)
    reaction = discord.utils.get(signup_msg.reactions, emoji="✅")
    
    if reaction:
        async for user in reaction.users():
            if not user.bot:
                game.participants[user.id] = QuizParticipant(user)
    
    return len(game.participants) > 0

async def start_quiz(ctx, rounds: int = 5):
    if not 1 <= rounds <= 20:
        await ctx.send("Die Rundenzahl muss zwischen 1 und 20 liegen!")
        return

    channel_id = ctx.channel.id
    if channel_id in active_games:
        await ctx.send("Es läuft bereits ein Quiz in diesem Kanal!")
        return

    game = QuizGame(rounds)
    
    # Sammle Teilnehmer
    has_participants = await collect_participants(ctx, game)
    
    if not has_participants:
        await ctx.send("❌ Keine Teilnehmer gefunden. Quiz wird abgebrochen!")
        return
    
    active_games[channel_id] = game
    
    participant_mentions = " ".join([f"{p.user.mention}" for p in game.participants.values()])
    
    # Countdown vor Spielstart
    countdown_msg = await ctx.send(f"🎯 **Achtung {participant_mentions}!**\nDie Runde beginnt in...")
    for i in range(3, 0, -1):
        await countdown_msg.edit(content=f"🎯 **Achtung {participant_mentions}!**\nDie Runde beginnt in...\n**{i}**")
        await asyncio.sleep(1)
    await countdown_msg.edit(content=f"🎯 **Los geht's! {participant_mentions}**")
    
    await ctx.send(f"🎮 **Quiz startet mit folgenden Teilnehmern:** {participant_mentions}\n"
                  f"Anzahl Runden: {rounds}\n"
                  "Beantworte die Fragen durch Klicken auf die Emojis.\n"
                  "`!lordquiz stop` zum Abbrechen.")
    
    await ask_question(ctx)

async def format_answer_results(question, participant_answers):
    """Formatiert die Antwortauflösung mit Emojis und Teilnehmerergebnissen"""
    result = []
    for i, choice in enumerate(question['choices']):
        emoji = "✅" if i == question['answer'] else "❌"
        correct_participants = [p.user.mention for p in participant_answers if 
                              participant_answers[p]['answer'] == i and 
                              i == question['answer']]
        
        choice_text = f"{emoji} {choice}"
        if i == question['answer'] and correct_participants:
            choice_text += f"\n└ Richtig beantwortet von: {', '.join(correct_participants)}"
        
        result.append(choice_text)
    
    return "\n\n".join(result)

async def ask_question(ctx):
    game = active_games[ctx.channel.id]
    
    if not game.active or game.current_round >= game.rounds:
        await end_game(ctx, "Quiz beendet!")
        return

    game.current_round += 1
    
    # Setze has_answered für alle Teilnehmer zurück
    for participant in game.participants.values():
        participant.has_answered = False

    # Wähle eine zufällige Frage
    question = random.choice(questions)
    game.current_question = question

    # Erstelle die Nachricht mit Emojis
    choices_text = "\n".join([f"{emoji_numbers[i]} {c}" for i, c in enumerate(question['choices'])])
    
    # Erstelle Scoring-Board
    scores = "\n".join([f"{p.user.name}: {p.score}" for p in game.participants.values()])
    
    message = await ctx.send(
        f"🔍 **Frage {game.current_round}/{game.rounds}:**\n"
        f"{question['question']}\n\n"
        f"{choices_text}\n\n"
        f"**Punktestand:**\n{scores}\n\n"
        "Zeit zum Antworten: 15 Sekunden!"
    )
    game.message = message

    # Füge Reaktionen hinzu
    for i in range(len(question['choices'])):
        await message.add_reaction(emoji_numbers[i])

    participant_answers = {p: {'answered': False, 'answer': None} for p in game.participants.values()}
    
    try:
        # Warte auf Reaktionen (15 Sekunden)
        end_time = asyncio.get_event_loop().time() + 15
        while asyncio.get_event_loop().time() < end_time:
            try:
                reaction, user = await ctx.bot.wait_for(
                    'reaction_add',
                    timeout=end_time - asyncio.get_event_loop().time(),
                    check=lambda reaction, user: (
                        user.id in game.participants and
                        not game.participants[user.id].has_answered and
                        str(reaction.emoji) in emoji_numbers and
                        reaction.message.id == message.id
                    )
                )
                
                participant = game.participants[user.id]
                participant.has_answered = True
                selected_answer = emoji_numbers.index(str(reaction.emoji))
                
                participant_answers[participant]['answered'] = True
                participant_answers[participant]['answer'] = selected_answer
                
                if selected_answer == question['answer']:
                    participant.score += 1
                
            except asyncio.TimeoutError:
                continue

        # Zeige Auflösung
        results = await format_answer_results(question, participant_answers)
        
        # Aktualisiere Punktestand
        scores = "\n".join([f"{p.user.name}: {p.score} Punkte" for p in game.participants.values()])
        
        await ctx.send(
            "⏰ **Zeit abgelaufen! Hier ist die Auflösung:**\n\n"
            f"{results}\n\n"
            f"**Aktueller Punktestand:**\n{scores}"
        )
        
        await asyncio.sleep(3)
        await ask_question(ctx)

    except Exception as e:
        print(f"Error in ask_question: {e}")
        await end_game(ctx, "Ein Fehler ist aufgetreten!")

async def stop_quiz(ctx):
    """Beendet das aktive Quiz."""
    if ctx.channel.id in active_games:
        await end_game(ctx, "Quiz wurde manuell beendet!")
    else:
        await ctx.send("Du hast kein aktives Quiz!")

async def end_game(ctx, reason):
    """Beendet das Spiel und zeigt den finalen Score."""
    if ctx.channel.id in active_games:
        game = active_games[ctx.channel.id]
        game.active = False
        
        # Erstelle Rangliste
        rankings = sorted(
            game.participants.values(),
            key=lambda p: p.score,
            reverse=True
        )
        
        if reason == "Quiz wurde manuell beendet!":
            message = "😡 **BUUUUUH!** Das Spiel wurde vorzeitig abgebrochen!"
        else:
            message = "🎮 **Quiz beendet!**"
            
            # Prüfe ob alle 0 Punkte haben
            if all(p.score == 0 for p in rankings):
                message += "\n\n😡 **BUUUUUH!** Niemand hat auch nur eine Frage richtig beantwortet! **SCHWACHE LEISTUNG!**"
            
            # Prüfe auf Gewinner
            elif rankings:
                top_score = rankings[0].score
                winners = [p for p in rankings if p.score == top_score]
                
                if len(winners) == 1:
                    winner = winners[0]
                    message += f"\n\n👑 **HERZLICHEN GLÜCKWUNSCH!**\n{winner.user.mention} ist der neue **Ehrendrachi**!"
                    
                    # Top 3 Celebration
                    if len(rankings) >= 2:
                        message += f"\n🥈 Zweiter Platz: {rankings[1].user.mention}"
                    if len(rankings) >= 3:
                        message += f"\n🥉 Dritter Platz: {rankings[2].user.mention}"
                else:
                    # Mehrere Gewinner mit gleichem Score
                    winners_mentions = ", ".join(w.user.mention for w in winners)
                    message += f"\n\n👥 **UNENTSCHIEDEN!**\n{winners_mentions} haben jeweils **{top_score} Punkte**!"
                    message += "\n\n🤪 **Zeit für ein Grubbeseggs um den wahren Champion zu ermitteln!**"
        
        rankings_text = "\n".join([
            f"{idx + 1}. {p.user.mention}: **{p.score} Punkte**"
            for idx, p in enumerate(rankings)
        ])
        
        # Cleanup
        del active_games[ctx.channel.id]

        # Sende Endergebnis
        embed = discord.Embed(
            title="🎮 Spielende!",
            description=f"{message}\n\n**Endstand:**\n{rankings_text}",
            color=0x00ff00
        )
        await ctx.send(embed=embed)

def register_quiz_commands(bot):
    @bot.command(name='lordquiz')
    async def lordquiz(ctx, cmd: str = None, rounds: int = 5):
        if cmd is None:
            await show_quiz_help(ctx)
        elif cmd.lower() == 'start':
            await start_quiz(ctx, rounds)
        elif cmd.lower() == 'stop':
            await stop_quiz(ctx)
        else:
            await show_quiz_help(ctx)

def setup(bot):
    register_quiz_commands(bot)
