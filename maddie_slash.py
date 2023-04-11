import os
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import wait_for_component, create_actionrow, create_button
from discord_slash.model import ButtonStyle
from config_interactions import team_slash
from discord.ext import commands
from dotenv import load_dotenv
from parse import slash_parse
import logging

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="!!!!!!?")
slash = SlashCommand(bot, sync_commands=True)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO) #set logging level to INFO, DEBUG if we want the full dump
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a') #open log file in append mode
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@slash.slash(
    name="editlabels",
    description="Adjust your labels, one up, one down",
    #guild_ids=[696999350726819931],
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
    logger.info(str(ctx.author.guild) + str(ctx.author.display_name) + str(ctx.data))
    await ctx.send(edit_labels_slash(ctx, 'en', labelup, labeldown))

@slash.slash(
    name="condition",
    description="Mark or clear a condition",
    #guild_ids=[696999350726819931],
    options=[
        create_option(name='condition', description="Condition", required=True, option_type=3, choices=[
            create_choice(name="afraid", value="afraid"),
            create_choice(name="angry", value="angry"),
            create_choice(name="guilty", value="guilty"),
            create_choice(name="hopeless", value="hopeless"),
            create_choice(name="insecure", value="insecure"),
            create_choice(name="damaged", value="damaged")
        ]),
        create_option(name='what', description="Mark or Clear", required=True, option_type=3, choices=[
            create_choice(name="Mark", value="mark"),
            create_choice(name="Clear", value="clear")
            ])
    ]
)
async def condition(ctx,condition:str,what:str):
    from playbook_interactions import condition_slash
    logger.info(str(ctx.author.guild) + str(ctx.author.display_name) + str(ctx.data))
    await ctx.send(condition_slash(ctx, 'en', condition, what))

# @slash.slash(
#     name="clearcondition",
#     description="Clear a condition",
#     guild_ids=[696999350726819931],
#     options=[
#         create_option(name='condition', description="Condition to mark", required=True, option_type=3, choices = [
#             create_choice(name="afraid", value="afraid"),
#             create_choice(name="angry", value="angry"),
#             create_choice(name="guilty", value="guilty"),
#             create_choice(name="hopeless", value="hopeless"),
#             create_choice(name="insecure", value="insecure"),
#             create_choice(name="damaged", value="damaged")
#         ])
#     ]
# )
# async def markcondition(ctx,condition:str):
#     from playbook_interactions import clear_condition_slash
#     await ctx.send(clear_condition_slash(ctx, 'en', condition))

@slash.slash(
    name="createcharacter",
    description="Create a character",
    #guild_ids=[696999350726819931],
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
            create_choice(name="ace", value="ace"),
            create_choice(name="inheritor", value="inheritor"),
            create_choice(name="persona", value="persona"),
            create_choice(name="ranger", value="ranger")
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
    logger.info(str(ctx.author.guild) + str(ctx.author.display_name) + str(ctx.data))
    await ctx.send(create_character_slash(ctx, 'en', playbook_name, character_name, player_name, label_to_increase_og))

@slash.slash(
    name = "deletecharacter",
    description = "Delete your character from the current channel."
)
async def delete_character(ctx):
    from playbook_interactions import delete_character_ctx
    logger.info(str(ctx.author.guild) + str(ctx.author.display_name) + str(ctx.data))
    await ctx.send(delete_character_ctx(ctx, 'en'))

@slash.slash(
    name="createcharacter5p",
    description="Create a character using Five Points playbooks",
    #guild_ids=[696999350726819931],
    options=[
        create_option(name='playbook_name', description='Choose a playbook', required=True, option_type=3, choices= [
            create_choice(name="ace", value="ace"),
            create_choice(name="inheritor", value="inheritor"),
            create_choice(name="persona", value="persona"),
            create_choice(name="ranger", value="ranger"),
            create_choice(name="relic", value="relic"),
            create_choice(name="ronin", value="ronin"),
            create_choice(name="royal", value="royal"),
            create_choice(name="transfer", value="transfer"),
            create_choice(name="witch", value="witch"),
        ]),
        create_option(name='character_name', description='What is your character called?', required=True, option_type=3),
        create_option(name='player_name', description="What is the player's name?", required=True, option_type=3),
        create_option(name='label_to_increase_og', description="What initial label would you like to increase?", required=True, option_type=3, choices=[
            create_choice(name="danger", value="danger"),
            create_choice(name="freak", value="freak"),
            create_choice(name="superior", value="superior"),
            create_choice(name="savior", value="savior"),
            create_choice(name="mundane", value="mundane")
        ])
    ]
)
async def createcharacter5p(ctx,playbook_name,character_name,player_name,label_to_increase_og):
    from playbook_interactions import create_character_slash
    logger.info(str(ctx.author.guild) + str(ctx.author.display_name) + str(ctx.data))
    await ctx.send(create_character_slash(ctx, 'en', playbook_name, character_name, player_name, label_to_increase_og))


@slash.slash(
    name="team",
    description="Interact with Team Pool",
    #guild_ids=[696999350726819931],
    options=[
        create_option(name='action', description="What's going on with team?", required=True, option_type=3, choices=[
            create_choice(name="Check team pool", value="check"),
            create_choice(name="Add to team pool", value="increase"),
            create_choice(name="Spend from team pool", value="decrease"),
            create_choice(name="Empty team pool", value="empty")
        ])
    ]
)
async def team(ctx, action):
    from config_interactions import team_slash
    logger.info(str(ctx.author.guild) + str(ctx.author.display_name) + str(ctx.data))
    await ctx.send(team_slash(ctx, 'en', action))


@slash.slash(
    name="playbooks",
    description="Playbook team moves, Moment of Truth etc.",
    #guild_ids=[696999350726819931],
    options=[
        create_option(name='choice', description='Which piece', required=True, option_type=3, choices=[
            create_choice(name='Share a triumphant celebration with someone', value='celebrate'),
            create_choice(name='Share a vulnerability or weakness with someone', value='weakness'),
            create_choice(name='Moment of Truth!', value='mot')
        ]),
        create_option(name='playbook', description="Playbook (optional)", required=False, option_type=3, choices=[
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
            create_choice(name="transformed", value="transformed")
        ])
    ]
)
async def playbooks(ctx, choice, playbook=None):
    from playbooks import get_playbook_component_slash
    logger.info(str(ctx.author.guild) + str(ctx.author.display_name) + str(ctx.data))
    await ctx.send(embed=get_playbook_component_slash(choice, ctx, 'en', playbook))

@slash.slash(
    name="playbooks5p",
    description="Playbook team moves, Moment of Truth etc. for Five Points Playbooks",
    #guild_ids=[696999350726819931],
    options=[
        create_option(name='choice', description='Which piece', required=True, option_type=3, choices=[
            create_choice(name='Share a triumphant celebration with someone', value='celebrate'),
            create_choice(name='Share a vulnerability or weakness with someone', value='weakness'),
            create_choice(name='Moment of Truth!', value='mot')
        ]),
        create_option(name='playbook', description="Playbook (optional)", required=False, option_type=3, choices=[
            create_choice(name="ace", value="ace"),
            create_choice(name="inheritor", value="inheritor"),
            create_choice(name="persona", value="persona"),
            create_choice(name="ranger", value="ranger"),
            create_choice(name="relic", value="relic"),
            create_choice(name="ronin", value="ronin"),
            create_choice(name="royal", value="royal"),
            create_choice(name="transfer", value="transfer"),
            create_choice(name="witch", value="witch")
        ])
    ]
)
async def playbooks5p(ctx, choice, playbook=None):
    from playbooks import get_playbook_component_slash
    logger.info(str(ctx.author.guild) + str(ctx.author.display_name) + str(ctx.data))
    await ctx.send(embed=get_playbook_component_slash(choice, ctx, 'en', playbook))


def create_updated_buttons(influence_over):
    updated_buttons = []
    for char in influence_over:
        button_style = ButtonStyle.green if char['hasInfluence'] else ButtonStyle.grey
        updated_buttons.append(create_button(style=button_style, label=char['id'], custom_id=f"influence_{char['id']}"))
    return create_actionrow(*updated_buttons)

@slash.slash(
    name="me",
    description="Retrieve character information",
    #guild_ids=[696999350726819931],
    options=[
        create_option(name='choice', description='Choose which one to display', required=True, option_type=3, choices=[
            create_choice(name='Print Character', value='print'),
            create_choice(name='Show Labels', value= 'labels'),
            create_choice(name='Show Conditions', value= 'conditions'),
            create_choice(name='Show Party', value= 'party'),
            create_choice(name='Show Influence', value= 'influence')
        ])
    ]
)
async def me(ctx, choice):
    from playbook_interactions import print_playbook_slash, get_conditions_slash, get_labels_slash, print_party, get_influence, invert_influence
    logger.info(str(ctx.author.guild) + str(ctx.author.display_name) + str(ctx.data))
    if choice == 'print':
        await ctx.send(print_playbook_slash(ctx, 'en'))
    if choice == 'conditions':
        await ctx.send(get_conditions_slash(ctx, 'en'))
    if choice == 'labels':
        await ctx.send(get_labels_slash(ctx, 'en'))
    if choice == 'party':
        await ctx.send(print_party(ctx, 'en'))
    if choice == 'influence':
        char_info = get_influence(ctx, 'en')
        if char_info == "I'm sorry but it appears you have no character created" or char_info == "No other players in the party.":
            await ctx.send(char_info)
        elif len(char_info['influenceOver']) <= 1:
            await ctx.send("No other players in the party.")
        else:
            action_row = create_updated_buttons(char_info['influenceOver'])
            await ctx.send("Toggle influence over characters:", components=[action_row])

            @bot.event
            async def on_component(ctx_button):
                custom_id = ctx_button.custom_id
                if custom_id.startswith("influence_"):
                    if ctx_button.author.id == ctx.author.id:
                        character_name = custom_id.split("_")[1]
                        # Call the invert_influence function to handle influence changes
                        invert_influence(ctx, character_name, char_info)

                        updated_action_row = create_updated_buttons(char_info['influenceOver'])
                        await ctx_button.edit_origin(content="Toggle influence over characters:",
                                                     components=[updated_action_row])
                    else:
                        await ctx_button.send("You are not authorized to change the influence status.", hidden=True)


def update_embed(embed, team):
    embed.add_field(name=team, value= f'\nTeam has been updated to {team}.')
    return embed

@slash.slash(
    name="battle",
    description="Enter Battle"
    )
async def battle(ctx):

    button_states = {
        "add_2_team": False,
        "leader_influence": False,
        "same_purpose": False,
        "mistrust": False,
        "ill_prepared": False
    }


    def create_updated_buttons():
        return [
            create_button(style=ButtonStyle.blurple if not button_states["add_2_team"] else ButtonStyle.gray,
                          label="Add 2 Team", custom_id="add_2_team"),
            create_button(style=ButtonStyle.green if not button_states["leader_influence"] else ButtonStyle.gray,
                          label="Leader has influence?", custom_id="leader_influence"),
            create_button(style=ButtonStyle.green if not button_states["same_purpose"] else ButtonStyle.gray,
                          label="Same purpose?", custom_id="same_purpose"),
            create_button(style=ButtonStyle.blue if not button_states["mistrust"] else ButtonStyle.gray,
                          label="Mistrust leader or team?", custom_id="mistrust"),
            create_button(style=ButtonStyle.blue if not button_states["ill_prepared"] else ButtonStyle.gray,
                          label="Ill-prepared/off balance?", custom_id="ill_prepared"),
        ]

    action_row = create_actionrow(*create_updated_buttons())
    embed, addendum = slash_parse(ctx, 153, 0)
    team = team_slash(ctx, 'en', 'check')
    message = await ctx.send(embed=embed, components=[action_row], content=team)

    while True:
        button_ctx = await wait_for_component(bot, components=action_row, timeout=3600)
        button_states[button_ctx.custom_id] = not button_states[button_ctx.custom_id]  # Toggle the button state
        prev_team = team
        if button_ctx.custom_id == "add_2_team":
            team = team_slash(ctx, 'en', 'increase_twice') if button_states[button_ctx.custom_id] else None
        if button_ctx.custom_id == "leader_influence":
            team = team_slash(ctx, 'en', 'increase') if button_states[button_ctx.custom_id] else team_slash(ctx, 'en', 'decrease')
        if button_ctx.custom_id == "same_purpose":
            team = team_slash(ctx, 'en', 'increase') if button_states[button_ctx.custom_id] else team_slash(ctx, 'en', 'decrease')
        if button_ctx.custom_id == "mistrust":
            team = team_slash(ctx, 'en', 'decrease') if button_states[button_ctx.custom_id] else team_slash(ctx, 'en', 'increase')
        if button_ctx.custom_id == "ill_prepared":
            team = team_slash(ctx, 'en', 'decrease') if button_states[button_ctx.custom_id] else team_slash(ctx, 'en', 'increase')
        if prev_team != team:  # Only update the embed if the team stat changed
            embed = update_embed(embed, team)
        # Handle other button interactions if needed
        await button_ctx.defer(edit_origin=True)  # Acknowledge the interaction
        action_row = create_actionrow(*create_updated_buttons())  # Update the buttons based on their new states
        await message.edit(content=team, components=[action_row])  # Update the message with the new 'team' stat
# @slash.slash(
#     name="character",
#     description="Character management functions",
#     guild_ids=[696999350726819931, 369149981782835200],
#     options=[
#         create_option(name='choice', description='Choose which one', required=True, option_type=3, choices=[
#             create_option(name='Delete Character  - this is permanent', value='delete'),
#             create_option(name='Replicate Character - please provide channel ID of original character', choices=[
#                 create_choice(name='Channel ID', value='chan_id')
#             ]
#             )
#
# )

async def character(ctx, choice):
    from playbook_interactions import delete_character_ctx, replicate_character
    if choice == 'delete':
        await ctx.send("Me", ctx, 'en')
    if choice == 'replicate':
        await ctx.send(replicate_character(ctx, 'en', chan_id))


# include generated slash commands file as if it's written inside this one:
with open(os.path.join(os.path.normpath(os.path.join(os.path.realpath(__file__), os.pardir)), "generated_commands.py")) as generated_code:
          exec(generated_code.read())

bot.run(TOKEN)