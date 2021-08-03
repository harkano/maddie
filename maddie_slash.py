import os
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="!!!!!!?")
slash = SlashCommand(bot, sync_commands=True)

@slash.slash(
    name="editlabels",
    description="Adjust your labels, one up, one down",
    guild_ids=[696999350726819931],
    options=[
        create_option(name='labelup', description="Label to increase", required=True, option_type=3, choices = [
            create_choice(name="danger", value="danger"),
            create_choice(name="freak", value="freak"),
            create_choice(name="superior", value = "superior"),
            create_choice(name="savior", value = "savior"),
            create_choice(name="mundane", value = "mundane"),
            create_choice(name="soldier", value = "soldier")
        ]),
        create_option(name='labeldown', description="Label to decrease", required=True, option_type=3, choices = [
            create_choice(name="danger", value="danger"),
            create_choice(name="freak", value="freak"),
            create_choice(name="superior", value = "superior"),
            create_choice(name="savior", value = "savior"),
            create_choice(name="mundane", value = "mundane"),
            create_choice(name="soldier", value = "soldier")
        ])
    ]
)
async def editlabels(ctx, labelup: str, labeldown: str):
    from playbook_interactions import edit_labels_slash
    await ctx.send(edit_labels_slash(ctx, 'en', labelup, labeldown))

@slash.slash(
    name="markcondition",
    description="Mark a condition",
    guild_ids=[696999350726819931],
    options=[
        create_option(name='condition', description="Condition to mark", required=True, option_type=3, choices=[
            create_choice(name="afraid", value="afraid"),
            create_choice(name="angry", value="angry"),
            create_choice(name="guilty", value="guilty"),
            create_choice(name="hopeless", value="hopeless"),
            create_choice(name="insecure", value="insecure"),
            create_choice(name="damaged", value="damaged")
        ])
    ]
)
async def clearcondition(ctx,condition:str):
    from playbook_interactions import clear_condition_slash
    await ctx.send(clear_condition_slash(ctx, 'en', condition))

@slash.slash(
    name="clearcondition",
    description="Clear a condition",
    guild_ids=[696999350726819931],
    options=[
        create_option(name='condition', description="Condition to mark", required=True, option_type=3, choices = [
            create_choice(name="afraid", value="afraid"),
            create_choice(name="angry", value="angry"),
            create_choice(name="guilty", value="guilty"),
            create_choice(name="hopeless", value="hopeless"),
            create_choice(name="insecure", value="insecure"),
            create_choice(name="damaged", value="damaged")
        ])
    ]
)
async def markcondition(ctx,condition:str):
    from playbook_interactions import clear_condition_slash
    await ctx.send(clear_condition_slash(ctx, 'en', condition))

@slash.slash(
    name="createcharacter",
    description="Create a character",
    guild_ids=[696999350726819931],
    options=[
        create_option(name='playbook_name', description='Choose a playbook', required=True, option_type=3, choices= [
            create_choice(name="beacon", value="beacon"),
            create_choice(name="brain", value="brain"),
            create_choice(name="bull", value="bull"),
            create_choice(name="delinquent", value="delinquent"),
            create_choice(name="doomed", value="doomed"),
            create_choice(name="harbinger", value="harbinger"),
            create_choice(name="innocent", value="innocent"),
            create_choice(name="janus", value="janus"),
            create_choice(name="joined", value="joined"),
            create_choice(name="legacy", value="legacy"),
            create_choice(name="newborn", value="newborn"),
            create_choice(name="nomad", value="nomad"),
            create_choice(name="nova", value="nova"),
            create_choice(name="outsider", value="outsider"),
            create_choice(name="protege", value="protege"),
            create_choice(name="reformed", value="reformed"),
            create_choice(name="scion", value="scion"),
            create_choice(name="soldier", value="soldier"),
            create_choice(name="star", value="star"),
            create_choice(name="transformed", value="transformed"),
        ]),
        create_option(name='character_name', description='What is your character called?', required=True, option_type=3),
        create_option(name='player_name', description="What is the player's name?", required=True, option_type=3),
        create_option(name='label_to_increase_og', description="What initial label would you like to increase?", required=True, option_type=3, choices=[
            create_choice(name="danger", value="danger"),
            create_choice(name="freak", value="freak"),
            create_choice(name="superior", value="superior"),
            create_choice(name="savior", value="savior"),
            create_choice(name="mundane", value="mundane"),
            create_choice(name="soldier", value="soldier")
        ])
    ]
)
async def createcharacter(ctx,playbook_name,character_name,player_name,label_to_increase_og):
    from playbook_interactions import create_character_slash
    await ctx.send(create_character_slash(ctx, 'en', playbook_name, character_name, player_name, label_to_increase_og))

@slash.slash(
    name="team",
    description="Interact with Team Pool",
    guild_ids=[696999350726819931],
    options=[
        create_option(name='action', description="What's going on with team?", required=True, option_type=3, choices=[
            create_choice(name="Check team pool", value="check"),
            create_choice(name="Add to team pool", value="increase"),
            create_choice(name="Spend from team pool", value="decrease"),
            create_choice(name="Empty team pool", value="empty"),
        ])
    ]
)
async def team(ctx, action):
    from config_interactions import team_slash
    await ctx.send(team_slash(ctx, 'en', action))

# include generated slash commands file as if it's written inside this one:
with open(os.path.join(os.normpath(os.path.join(os.path.realpath(__file__), os.pardir)), "generated_slash_commands.py") as generated_code:
          exec(generated_code.read())

bot.run(TOKEN)
