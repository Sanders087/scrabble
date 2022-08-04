#!/usr/bin/python
# encoding: utf-8\


import discord
from discord.ext import commands
import random



#Bot configuration

TOKEN = "put your token here"

bot = commands.Bot(command_prefix='k!', intents = discord.Intents.all())



#Letter randomizer
def randomize_letters(string: str) -> str:
    letters = [c for c in string if c.isalpha()]
    random.shuffle(letters)

    randomized = [letters.pop() if c.isalpha() else c for c in string]
    return "".join(randomized)


@bot.command()
@commands.has_any_role("Events MC")
async def scrabble(ctx, phrase, scrnum, channel : discord.TextChannel, language):
    await ctx.message.delete()
    final_phrase = phrase
    def check(m):
        return m.content.lower() == final_phrase.lower() and m.channel.id == channel.id
    phrase = randomize_letters(phrase).split()
    ballsforquest = 0
    wordscount = len(phrase)
    if (wordscount == 2):
        bl_circle = random.randint(1, len(phrase[0])) 
        rd_circle = random.randint(1, len(phrase[1]))
        bl_circle = bl_circle-1
        rd_circle = rd_circle-1
        phrase[0] = phrase[0][:bl_circle] + "🔵" + phrase[0][bl_circle+1:]
        phrase[1] = phrase[1][:rd_circle] + "🔴" + phrase[1][rd_circle+1:]
        ballsforquest = 1
        wrdballsforquest = "балл"
        if language == "rus":
            lastPhrase = "🔵 - 🔴 пропуски букв, для соответствующих слов"
        elif language == "eng":
            lastPhrase = "**🔵 & 🔴 are blanks for the respective words**"
    elif (wordscount == 3):
        bl_circle = random.randint(1, len(phrase[0])) 
        rd_circle = random.randint(1, len(phrase[1]))
        grn_circle = random.randint(1, len(phrase[2]))
        bl_circle = bl_circle-1
        rd_circle = rd_circle-1
        grn_circle = grn_circle-1
        phrase[0] = phrase[0][:bl_circle] + "🔵" + phrase[0][bl_circle+1:]
        phrase[1] = phrase[1][:rd_circle] + "🔴" + phrase[1][rd_circle+1:]
        phrase[2] = phrase[2][:rd_circle] + "🟢" + phrase[2][rd_circle+1:]
        ballsforquest = 2
        wrdballsforquest = "балла"
        if language == "rus":
            lastPhrase = "🔵 - 🔴 - 🟢 пропуски букв, для соответствующих слов"
        elif language == "eng":
            lastPhrase = "**🔵 & 🔴 & 🟢 are blanks for the respective words**"
    phrase = " / ".join(phrase)
    phrase = phrase.upper()

    if language == "rus":
        await channel.send(f"__Скрэббл номер {scrnum}__\n{phrase}\n**{wordscount} слова**\n**{ballsforquest} {wrdballsforquest}**\n{lastPhrase}")
    elif language == "eng":
        await channel.send(f"**Scrabble - Round {scrnum}**\n**{phrase}**\n**Words: {wordscount}\nPoints: {ballsforquest}**\n{lastPhrase}")


    guess = await bot.wait_for("message", check=check, timeout=100000)
    gcu = guess.content
    if final_phrase.lower() == gcu.lower():
        athor = guess.author
        if wordscount == 2:
            if language == "rus":
                await channel.send(f"Правильный ответ: **{final_phrase.upper()}**\n{athor.mention}, +1 балл")
            elif language == "eng":
                await channel.send(f"__Correct answer:__ **{final_phrase.upper()}**\n**+1 point for {athor.mention}**")
        elif wordscount == 3:
            if language == "rus":
                await channel.send(f"Правильный ответ: **{final_phrase.upper()}**\n{athor.mention}, +2 балла")
            elif language == "eng":
                await channel.send(f"__Correct answer:__ **{final_phrase.upper()}**\n**+2 points for {athor.mention}**")




@bot.command()
@commands.has_any_role("Events MC")
async def question(ctx, question, answer, channel : discord.TextChannel, language):
    def check(m):
        return m.content.lower() == answer.lower() and m.channel.id == channel.id
    await ctx.message.delete()
    wordscount = len(answer.split())
    if len(answer.split()) == 3:
        endword = ""
        for i in range(0, len(answer.split()[0])):
            endword = endword + "🟡"
        endword = endword + " / "
        for i in range(0, len(answer.split()[1])):
            endword = endword + "🟡"
        endword = endword + " / "
        for i in range(0, len(answer.split()[2])):
            endword = endword + "🟡"
        ballsforquest = 2
        wrdballsforquest = "балла"
    elif len(answer.split()) == 2:
        endword = ""
        for i in range(0, len(answer.split()[0])):
            endword = endword + "🟡"
        endword = endword + " / "
        for i in range(0, len(answer.split()[1])):
            endword = endword + "🟡"
        ballsforquest = 1
        wrdballsforquest = "балл"
    if language == "rus":
        await channel.send(f"__Скрэббл вопрос__\n**Вопрос: **{question}\n{endword}\n**{wordscount} слова**\n**{ballsforquest} {wrdballsforquest}**\n🟡 - замена каждой буквы в словах")
    elif language == "eng":
        await channel.send(f"**__Plus question__** {question}\n**Scrabble:** {endword}\n**Pts. for trivia : {ballsforquest}**\n**To unlock the letters, someone must answer correctly to the trivia question!**")
    guess = await bot.wait_for("message", check=check, timeout=100000)
    gcu = guess.content
    if answer.lower() == gcu.lower():
        athor = guess.author
        if len(answer.split()) == 2:
            if language == "rus":
                await channel.send(f"Правильный ответ: **{answer.upper()}**\n{athor.mention}, +1 балл")
            elif language == "eng":
                await channel.send(f"__Correct answer:__ **{answer.upper()}\n+1 score for {athor.mention}**")
        elif len(answer.split()) == 3:
            if language == "rus":
                await channel.send(f"Правильный ответ: **{answer.upper()}**\n{athor.mention}, +2 балла")
            elif language == "eng":
                await channel.send(f"__Correct answer:__ **{answer.upper()}\n+2 scores for {athor.mention}**")


bot.run(TOKEN)