
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
from utils import get_modified_num
from moves import get_moves
from playbook_interactions import lock_label, edit_labels, mark_potential, mark_condition, clear_condition
from command_handler import plain_command_handler, embed_command_handler
from parse import mad_parse, add_result

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
    #list moves
    move_list = get_moves(message, json_array)
    if move_list:
        await message.channel.send(move_list)
        return
    # handle help and all of the playbook interactions
    response = plain_command_handler(message, 'en')

    if response:
        await message.channel.send(response)
        return

    response = embed_command_handler(message, 'en')

    if response:
        await message.channel.send(embed=response)
        return

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
