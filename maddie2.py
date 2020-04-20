
# bot.py
import os
import discord
from discord.ext import commands
import random
import json
import re
import logging
#import owner

from dotenv import load_dotenv

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO) #set logging level to INFO, DEBUG if we want the full dump
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a') #open log file in append mode
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
print (os.path.basename(__file__))
if os.path.basename(__file__) == 'maddie2.py':TOKEN = os.getenv('DISCORD_TOKEN_DEV')
else:TOKEN = os.getenv('DISCORD_TOKEN')
print (TOKEN)
def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or("!")(bot, message)
    with open("prefixes.json", 'r') as f:
        prefixes = json.load(f)

    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or("!")(bot, message)

    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(bot,message)

logger.info (TOKEN)
#client = discord.Client()
client = commands.Bot(command_prefix=get_prefix)

async def is_guild_owner(ctx):
    return ctx.author.id == ctx.guild.owner.id
    print (ctx.author_id, ctx.guild.owner.id)


async def prefix(self, ctx, *, pre):
    with open(r"prefixes.json", 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = pre
    await ctx.send(f"New prefix is `{pre}`")

    with open(r"prefixes.json", 'r') as f:
        json.dump(prefixes, f, indent=4)

##Load in the existing moves
input_file = open ('data.json')
json_array = json.load(input_file)

moves_list = []
for p in json_array['moves']:
    moves_list.append(p['shortName'])
print (moves_list)

def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or("!")(bot, message)
    with open("prefixes.json", 'r') as f:
        prefixes = json.load(f)
    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or("!")(bot, message)
    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(bot, message)

        
##Setup the big sub
def mad_parse(msg,user):
    blob = ""
    capital = ""
    phrase = ""
    word = ""
    mod = ""
    num = int(0)
    quiet = 0
    match = 0
    # parse command into parts
    msg = msg.lower()
    searchStr1 = r'[a-z]+'
    searchStr2 = r'[\+\-]'
    searchStr3 = r'[123456]'
    log_line = ''
    result1 = re.search(searchStr1, msg)
    if result1:
        log_line = log_line + result1.group(0)
        word = result1.group(0)
    else: log_line = log_line + "no cmd "
    result2 = re.search(searchStr2, msg)
    if result2:
        log_line = log_line + result2.group()
        mod = result2.group(0)
    else: log_line = log_line + "no mod "
    result3 = re.search(searchStr3, msg)
    if result3:
        log_line = log_line + result3.group(0)
        num = int(result3.group(0))
    else: log_line = log_line + "no num "
    logger.info (msg + log_line)
 # figure out which type of modifier it is
    num_calc = int(0)
    if mod == '+': num_calc  = num 
    elif mod == '-' : num_calc = -1 * num
    else : num_calc = num
 # lookup a table for the big blob of text and a wee blob
    for p in json_array['moves']:
        if p['shortName'] == word:
            blob = p['blob']
            capital = p['capital']
            phrase = p['phrase']
            img = p['img']
            match = 1
    #Quiet mode
    searchStr4 = r'!!'
    result4 = re.search(searchStr4, msg)
    if result4: quiet = 1
#do dice rolling
    result1 = random.randrange(1,6) ##first d6
    result2 = random.randrange(1,6) ##second d6
    result_tot = result1 + result2 + num_calc #2 d6 + mod
#Ugly format blob!
    if match == 1 : #lets us ignore ! prefix commands that aren't in our list
        embed=discord.Embed(title=f"{capital}")
        embed.set_author(name=f"{user} {phrase}")
        embed.set_thumbnail(url=img)
        if quiet == 0: embed.add_field(name="Description", value=f"{blob}") # don't include the blob if we're in quiet mode (!!)
        embed.add_field(name="Calculation", value=f"Dice **{result1}** + **{result2}**, Label {mod} **{num}**", inline=False)
        embed.add_field(name="Result", value=f"**{result_tot}**")
        embed.set_footer(text=" ")

        return embed

    else:return 0


@client.event
async def on_ready():
    logger.info(f'{client.user} has connected to Discord!')
    servers = list(client.guilds)
    logger.info("Connected on "+str(len(client.guilds))+" servers:")
    for x in range(len(servers)):
        logger.info('   ' + servers[x-1].name)


#Listen for messages
@client.event
async def on_message(message):
    pre = get_prefix
    print (pre)
    if message.author == client.user:
        return
    #answer a call for help
    elif message.content.startswith("!help"):
        log_line = message.guild.name + "|" + message.channel.name + "|" + message.author.name + "|" + message.content
        logger.info(log_line)
        help_file = open("../../aws/help", "r")
        response = help_file.read()
        await message.channel.send(response)
    #list moves
    elif message.content.startswith("!moves+"):
        response = '**Name - description, keyword, label**\n'
        for p in json_array['moves']:
            response = response + p['capital'].capitalize() + " - " + p['description'] + ", " + p['shortName'] + ", " + p['label'] + "\n "
        await message.channel.send(response)
    elif message.content.startswith("!moves"):
        response = ''
        for p in json_array['moves']:
            response = response + p['shortName'] + ", "
        await message.channel.send(response)
#remember generic ! should always be last in the tree
    elif message.content.startswith("!"):
        log_line = message.guild.name + "|" + message.channel.name + "|" + message.author.name + "|" + message.content
        logger.info(log_line)
        response =  mad_parse(message.content, message.author.display_name)
        if response: await message.channel.send(embed=response)

    await client.process_commands(message)

@client.command()
async def ping(ctx):
    await ctx.send("Pong!")

@client.command()
async def test(ctx, arg):
    await ctx.send(arg)

@client.command()
async def moves(ctx):
    response = ''
    for p in json_array['moves']:
        response = response + p['shortName'] + ", "
    await ctx.send(response)

#Leaving this out for now as i like the message regex match for being more flexible, but this would be the right way to do it
#@client.command(aliases=moves_list)
#async def move(ctx, *, words):
#    print (words, ctx)
#    await ctx.send(embed=mad_parse(ctx.c, ctx.author.display_name))

@client.command()
@commands.is_owner()
async def prefix(ctx, *, pre):
    with open(r"prefixes.json", 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = pre
    await ctx.send(f"New prefix is `{pre}`")

    with open(r"prefixes.json", 'w') as f:
        json.dump(prefixes, f, indent=4)


#runs the bot!
client.run(TOKEN)
