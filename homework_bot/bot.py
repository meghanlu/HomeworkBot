from discord.ext import commands
from mathjspy import MathJS
import re
import wolframalpha

appid = ""

with open("WA_APPID.txt", "r") as appid_file:
    appid = appid_file.read()

wa_client = wolframalpha.Client(appid)

mjs = MathJS()

todo_list = ['math', 'reading', 'Gym']

bot = commands.Bot(command_prefix=('homie ', '!'), case_insensitive=True)

@bot.event
async def on_message(message):
    if message.author.bot:
        if (message.author == bot.user and 
        re.match('^`\d+\.\s',message.content)):
            await message.add_reaction('✅')
        return

    if message.content.lower().startswith("solve"):
        try:
            await message.channel.send(mjs.eval(message.content[len("solve"):]))
        except:
            await message.channel.send("Sorry, we could not compute.")

    elif message.content.lower().startswith("add todo"):
        todo_list.append(message.content[len("add todo"):])
        message.content = "!todo"

    elif message.content.lower().startswith("ask"):
        async with message.channel.typing():
            res = wa_client.query(message.content[len("ask"):])
            answer = next(res.results).text
        await message.channel.send(answer)

    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    
    if reaction.emoji == '✅' and  reaction.message.author == bot.user:
        todo_item = re.sub('^`\d+\.\s', '', reaction.message.content)
        todo_item = todo_item[:len(todo_item) - 1]
        if todo_item != reaction.message.content and todo_item in todo_list:
            todo_list.remove(todo_item)
            await reaction.message.add_reaction('🎉')
            await reaction.message.channel.send(("Congrats on finishing " + 
            todo_item + "!!!"))


@bot.command(name = "todo", help = "Display TODO List")
async def todo(ctx):
    if not todo_list:
        await ctx.send("There is nothing on your todo list!")
    for num, item in enumerate(todo_list, 1):
        await ctx.send(make_codeblock(str(num) + ". " + item))

@bot.command(name = "lol")
async def help(ctx):
    await ctx.send("lol")

@bot.group(invoke_without_command = False, case_insensitive = True)
async def pomodoro(ctx):
    await ctx.send("Type pomodoro quit to exit.")

@pomodoro.command(name = "quit")
async def quit(ctx):
    await ctx.send("Successfully quit.")

def make_codeblock(string : str):
    return "`" + string + "`"

with open("BOT_TOKEN.txt", "r") as token_file:
    TOKEN = token_file.read()
    print("Token file read")
    bot.run(TOKEN)