
# bot.py
import os
import discord
import random
import json
import parse
import logging

from dotenv import load_dotenv
from utils import get_modified_num
from moves import get_moves

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO) #set logging level to INFO, DEBUG if we want the full dump
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a') #open log file in append mode
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
print (__file__)
if __file__ == 'maddie.py':TOKEN = os.getenv('DISCORD_TOKEN_DEV')
else:TOKEN = os.getenv('DISCORD_TOKEN')
logger.info (TOKEN)
client = discord.Client()

##Load in the existing moves
input_file = open ('data.json')
json_array = json.load(input_file)


def add_result (embed, num_calc, mod, num):
    #do dice rolling
    result1 = random.randrange(1,6) ##first d6
    result2 = random.randrange(1,6) ##second d6
    result_tot = result1 + result2 + num_calc #2 d6 + mod
    embed.add_field(name="Calculation", value=f"Dice **{result1}** + **{result2}**, Label {mod} **{num}**", inline=False)
    embed.add_field(name="Result", value=f"**{result_tot}**")



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
    if message.author == client.user:
        return
    #answer a call for help
    elif message.content.startswith("!help"):
        log_line = message.guild.name + "|" + message.channel.name + "|" + message.author.name + "|" + message.content
        logger.info(log_line)
        help_file = open("help", "r")
        response = help_file.read()
        await message.channel.send(response)
    #list moves
    move_list = get_moves(message, json_array)
    if move_list:
        await message.channel.send(move_list)
    elif message.content.startswith("!help"):
        log_line = message.guild.name + "|" + message.channel.name + "|" + message.author.name + "|" + message.content
        logger.info(log_line)
        help_file = open("help","r")
        response = help_file.read() 
        await message.channel.send(response)
    #remember generic ! should always be last in the tree
    elif message.content.startswith("!"):
        log_line = message.guild.name + "|" + message.channel.name + "|" + message.author.name + "|" + message.content
        logger.info(log_line)
        response =  mad_parse(message.content, message.author.display_name)
        if response: 
            logger.info(response)
            await message.channel.send(embed=response)
client.run(TOKEN)
