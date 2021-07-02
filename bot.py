from discord.ext import commands
from mathjspy import MathJS
import re
import wolframalpha

appid = ""

with open("WA_APPID.txt", "r") as appid_file:
    appid = appid_file.read()

wa_client = wolframalpha.Client(appid)

mjs = MathJS()

bot = commands.Bot(command_prefix=('homie ', '!'), case_insensitive=True)

@bot.event
async def on_message(message):
    if message.author.bot:
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

def make_codeblock(string : str):
    return "`" + string + "`"

with open("BOT_TOKEN.txt", "r") as token_file:
    TOKEN = token_file.read()
    print("Token file read")
    bot.run(TOKEN)