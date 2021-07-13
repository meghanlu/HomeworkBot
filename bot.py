from discord.ext import commands
from mathjspy import MathJS
import re
import wolframalpha
import datetime
import discord

appid = ""

with open("WA_APPID.txt", "r") as appid_file:
    appid = appid_file.read()

wa_client = wolframalpha.Client(appid)

mjs = MathJS()

todo_list = []

command_prefixes = ('homie ', '!')

bot = commands.Bot(command_prefix=command_prefixes, case_insensitive=True, help_command=None)

@bot.event
async def on_message(message):
    if message.author.bot:
        # Check if message is by another bot or itself
        if (message.author == bot.user and 
        re.match('^`\d+\.\s',message.content)):
            # Add reaction to todo list
            await message.add_reaction('✅')
        return

    content_without_prefix = message.content

    for command_prefix in command_prefixes:
        # Remove command prefix if applicable
        if content_without_prefix.lower().startswith(command_prefix):
            content_without_prefix = remove_prefix(message.content, command_prefix)
            break

    if content_without_prefix.lower().startswith("solve"):
        # Evaluate with mathjspy library
        try:
            await message.channel.send(mjs.eval(message.content[len("solve"):]))
        except:
            await message.channel.send("Sorry, we could not compute.")

    elif content_without_prefix.lower().startswith("ask"):
        # Query with wolframalpha library 
        async with message.channel.typing():
            res = wa_client.query(message.content[len("ask"):])
            answer = next(res.results).text
        await message.channel.send(answer)

    elif content_without_prefix.lower().startswith("add todo"):
        # Add to todo list
        todo_list.append(message.content[len("add todo"):])
        message.content = "!todo"

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

@bot.command(name = "todo")
async def todo(ctx):
    if not todo_list:
        await ctx.send("There is nothing on your todo list!")
    else:
        for num, item in enumerate(todo_list, 1):
            await ctx.send(make_codeblock(str(num) + ". " + item))
        await ctx.send(make_codeblock("React to check off a task!"))

@bot.command(name='info', aliases=['help', 'commands'])
async def await_info(ctx):
    desc = 'Command prefixes (homie or !) are optional ' \
        'on commands: solve, ask, and add todo. It is mandatory on all other commands.'
    embed = discord.Embed(title='Homie W. Commands', description=desc)

    embed.add_field(name='solve [equation]', value='Solve a math equation')
    embed.add_field(name='ask [question]', value='Ask any question')
    embed.add_field(name='todo', value='Display TODO List')
    embed.add_field(name='add todo [todo list item]', value='Add an item to the TODO List')
    embed.add_field(name='timer [seconds] [minutes] [hours] [days]', value='Set a timer')

    embed.set_footer(text='Have a nice day!')
    await ctx.send(embed=embed)

@bot.command(name = "timer")
async def timer(ctx, seconds: float, minutes: float=0, hours: float=0, days : float=0):
    target = (datetime.datetime.now() + datetime.timedelta(days=days, 
    seconds=seconds, minutes=minutes, hours=hours))

    timer_embed = discord.Embed(
        title = "Timer"
    )
    
    timer_embed.add_field(
        name = "Time Left:",
        value = str(1)
    )

    timer_embed_message = await ctx.send(embed=timer_embed)

    while datetime.datetime.now() < target:
        time_left = target - datetime.datetime.now()
        timer_embed.remove_field(0)
        timer_embed.add_field(
            name = "Time Left:",
            value = str(time_left)
        )
        await timer_embed_message.edit(embed=timer_embed)
    
    await ctx.send("Your timer is up!!", mention_author=True)
    await ctx.send(minutes)

def make_codeblock(string : str):
    return "`" + string + "`"

def remove_prefix(string:str, prefix:str):
    if string.startswith(prefix):
        return string[len(prefix):]

with open("BOT_TOKEN.txt", "r") as token_file:
    TOKEN = token_file.read()
    print("Token file read")
    bot.run(TOKEN)