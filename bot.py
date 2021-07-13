from discord.ext import commands
from mathjspy import MathJS
import re
import wolframalpha

appid = ""

with open("WA_APPID.txt", "r") as appid_file:
    appid = appid_file.read()

wa_client = wolframalpha.Client(appid)

mjs = MathJS()

todo_list = []

bot = commands.Bot(command_prefix=('homie ', '!'), case_insensitive=True)

@bot.event
async def on_message(message):
    if message.author.bot:
        # Check if message is by another bot or itself
        if (message.author == bot.user and 
        re.match('^`\d+\.\s',message.content)):
            # Add reaction to todo list
            await message.add_reaction('✅')
        return

    if message.content.lower().startswith("solve"):
        try:
            await message.channel.send(mjs.eval(message.content[len("solve"):]))
        except:
            await message.channel.send("Sorry, we could not compute.")

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
        # If someone checked something off of the todo list
        todo_item = re.sub('^`\d+\.\s', '', reaction.message.content)
        todo_item = todo_item[:len(todo_item) - 1]
        if todo_item != reaction.message.content and todo_item in todo_list:
            todo_list.remove(todo_item)
            await reaction.message.add_reaction('🎉')
            await reaction.message.channel.send(("Congrats on finishing " + 
            todo_item + "!!!"))

def make_codeblock(string : str):
    return "`" + string + "`"

with open("BOT_TOKEN.txt", "r") as token_file:
    TOKEN = token_file.read()
    print("Token file read")
    bot.run(TOKEN)