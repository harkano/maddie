import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from parse import slash_parse
import logging
from config_interactions import team_slash

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!!!!!!?", intents=intents)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")

@bot.tree.command(name="editlabels", description="Adjust your labels, one up, one down")
@app_commands.choices(
    labelup=[
        app_commands.Choice(name="danger", value="danger"),
        app_commands.Choice(name="freak", value="freak"),
        app_commands.Choice(name="superior", value="superior"),
        app_commands.Choice(name="savior", value="savior"),
        app_commands.Choice(name="mundane", value="mundane"),
        app_commands.Choice(name="soldier", value="soldier")
    ],
    labeldown=[
        app_commands.Choice(name="danger", value="danger"),
        app_commands.Choice(name="freak", value="freak"),
        app_commands.Choice(name="superior", value="superior"),
        app_commands.Choice(name="savior", value="savior"),
        app_commands.Choice(name="mundane", value="mundane"),
        app_commands.Choice(name="soldier", value="soldier")
    ]
)
async def editlabels(interaction: discord.Interaction, labelup: str, labeldown: str):
    from playbook_interactions import edit_labels_slash
    logger.info(f"{interaction.guild}|{interaction.user.display_name}|{interaction.data}")
    # Currently passing interaction as ctx equivalent
    result = edit_labels_slash(interaction, 'en', labelup, labeldown)
    await interaction.response.send_message(result)


@bot.tree.command(name="condition", description="Mark or clear a condition")
@app_commands.choices(
    condition=[
        app_commands.Choice(name="afraid", value="afraid"),
        app_commands.Choice(name="angry", value="angry"),
        app_commands.Choice(name="guilty", value="guilty"),
        app_commands.Choice(name="hopeless", value="hopeless"),
        app_commands.Choice(name="insecure", value="insecure"),
        app_commands.Choice(name="damaged", value="damaged")
    ],
    what=[
        app_commands.Choice(name="Mark", value="mark"),
        app_commands.Choice(name="Clear", value="clear")
    ]
)
async def condition(interaction: discord.Interaction, condition: str, what: str):
    from playbook_interactions import condition_slash
    logger.info(f"{interaction.guild}|{interaction.user.display_name}|{interaction.data}")
    result = condition_slash(interaction, 'en', condition, what)
    await interaction.response.send_message(result)


# --- Character Creation via Modal ---

class CreateCharacterModal(discord.ui.Modal, title='Create Character'):
    character_name = discord.ui.TextInput(
        label='Character Name',
        placeholder='What is your character called?',
    )
    player_name = discord.ui.TextInput(
        label='Player Name',
        placeholder="What is the player's name?",
    )

    def __init__(self, playbook_name: str, label_to_increase_og: str):
        super().__init__()
        self.playbook_name = playbook_name
        self.label_to_increase_og = label_to_increase_og

    async def on_submit(self, interaction: discord.Interaction):
        from playbook_interactions import create_character_slash
        logger.info(f"{interaction.guild}|{interaction.user.display_name}|{interaction.data}")
        result = create_character_slash(
            interaction, 'en',
            self.playbook_name,
            self.character_name.value,
            self.player_name.value,
            self.label_to_increase_og
        )
        await interaction.response.send_message(result)


@bot.tree.command(name="createcharacter", description="Create a character")
@app_commands.choices(
    playbook_name=[
        app_commands.Choice(name="beacon", value="beacon"),
        app_commands.Choice(name="brain", value="brain"),
        app_commands.Choice(name="bull", value="bull"),
        app_commands.Choice(name="delinquent", value="delinquent"),
        app_commands.Choice(name="doomed", value="doomed"),
        app_commands.Choice(name="harbinger", value="harbinger"),
        app_commands.Choice(name="innocent", value="innocent"),
        app_commands.Choice(name="janus", value="janus"),
        app_commands.Choice(name="joined", value="joined"),
        app_commands.Choice(name="legacy", value="legacy"),
        app_commands.Choice(name="newborn", value="newborn"),
        app_commands.Choice(name="nomad", value="nomad"),
        app_commands.Choice(name="nova", value="nova"),
        app_commands.Choice(name="outsider", value="outsider"),
        app_commands.Choice(name="protege", value="protege"),
        app_commands.Choice(name="reformed", value="reformed"),
        app_commands.Choice(name="scion", value="scion"),
        app_commands.Choice(name="soldier", value="soldier"),
        app_commands.Choice(name="star", value="star"),
        app_commands.Choice(name="transformed", value="transformed"),
        app_commands.Choice(name="ace", value="ace"),
        app_commands.Choice(name="inheritor", value="inheritor"),
        app_commands.Choice(name="persona", value="persona"),
        app_commands.Choice(name="ranger", value="ranger")
    ],
    label_to_increase_og=[
        app_commands.Choice(name="danger", value="danger"),
        app_commands.Choice(name="freak", value="freak"),
        app_commands.Choice(name="superior", value="superior"),
        app_commands.Choice(name="savior", value="savior"),
        app_commands.Choice(name="mundane", value="mundane"),
        app_commands.Choice(name="soldier", value="soldier")
    ]
)
async def createcharacter(interaction: discord.Interaction, playbook_name: str, label_to_increase_og: str):
    await interaction.response.send_modal(CreateCharacterModal(playbook_name, label_to_increase_og))


@bot.tree.command(name="createcharacter5p", description="Create a character using Five Points playbooks")
@app_commands.choices(
    playbook_name=[
        app_commands.Choice(name="ace", value="ace"),
        app_commands.Choice(name="inheritor", value="inheritor"),
        app_commands.Choice(name="persona", value="persona"),
        app_commands.Choice(name="ranger", value="ranger"),
        app_commands.Choice(name="relic", value="relic"),
        app_commands.Choice(name="ronin", value="ronin"),
        app_commands.Choice(name="royal", value="royal"),
        app_commands.Choice(name="transfer", value="transfer"),
        app_commands.Choice(name="witch", value="witch")
    ],
    label_to_increase_og=[
        app_commands.Choice(name="danger", value="danger"),
        app_commands.Choice(name="freak", value="freak"),
        app_commands.Choice(name="superior", value="superior"),
        app_commands.Choice(name="savior", value="savior"),
        app_commands.Choice(name="mundane", value="mundane")
    ]
)
async def createcharacter5p(interaction: discord.Interaction, playbook_name: str, label_to_increase_og: str):
    await interaction.response.send_modal(CreateCharacterModal(playbook_name, label_to_increase_og))


@bot.tree.command(name="deletecharacter", description="Delete your character from the current channel.")
async def delete_character(interaction: discord.Interaction):
    from playbook_interactions import delete_character_ctx
    logger.info(f"{interaction.guild}|{interaction.user.display_name}|{interaction.data}")
    result = delete_character_ctx(interaction, 'en')
    await interaction.response.send_message(result)


@bot.tree.command(name="team", description="Interact with Team Pool")
@app_commands.choices(
    action=[
        app_commands.Choice(name="Check team pool", value="check"),
        app_commands.Choice(name="Add to team pool", value="increase"),
        app_commands.Choice(name="Spend from team pool", value="decrease"),
        app_commands.Choice(name="Empty team pool", value="empty")
    ]
)
async def team(interaction: discord.Interaction, action: str):
    from config_interactions import team_slash
    logger.info(f"{interaction.guild}|{interaction.user.display_name}|{interaction.data}")
    result = team_slash(interaction, 'en', action)
    await interaction.response.send_message(result)


@bot.tree.command(name="playbooks", description="Playbook team moves, Moment of Truth etc.")
@app_commands.choices(
    choice=[
        app_commands.Choice(name='Share a triumphant celebration with someone', value='celebrate'),
        app_commands.Choice(name='Share a vulnerability or weakness with someone', value='weakness'),
        app_commands.Choice(name='Moment of Truth!', value='mot')
    ],
    playbook=[
        app_commands.Choice(name="beacon", value="beacon"),
        app_commands.Choice(name="brain", value="brain"),
        app_commands.Choice(name="bull", value="bull"),
        app_commands.Choice(name="delinquent", value="delinquent"),
        app_commands.Choice(name="doomed", value="doomed"),
        app_commands.Choice(name="harbinger", value="harbinger"),
        app_commands.Choice(name="innocent", value="innocent"),
        app_commands.Choice(name="janus", value="janus"),
        app_commands.Choice(name="joined", value="joined"),
        app_commands.Choice(name="legacy", value="legacy"),
        app_commands.Choice(name="newborn", value="newborn"),
        app_commands.Choice(name="nomad", value="nomad"),
        app_commands.Choice(name="nova", value="nova"),
        app_commands.Choice(name="outsider", value="outsider"),
        app_commands.Choice(name="protege", value="protege"),
        app_commands.Choice(name="reformed", value="reformed"),
        app_commands.Choice(name="scion", value="scion"),
        app_commands.Choice(name="soldier", value="soldier"),
        app_commands.Choice(name="star", value="star"),
        app_commands.Choice(name="transformed", value="transformed")
    ]
)
async def playbooks(interaction: discord.Interaction, choice: str, playbook: str = None):
    from playbooks import get_playbook_component_slash
    logger.info(f"{interaction.guild}|{interaction.user.display_name}|{interaction.data}")
    result = get_playbook_component_slash(choice, interaction, 'en', playbook)
    await interaction.response.send_message(embed=result)


@bot.tree.command(name="playbooks5p", description="Playbook team moves, Moment of Truth etc. for Five Points Playbooks")
@app_commands.choices(
    choice=[
        app_commands.Choice(name='Share a triumphant celebration with someone', value='celebrate'),
        app_commands.Choice(name='Share a vulnerability or weakness with someone', value='weakness'),
        app_commands.Choice(name='Moment of Truth!', value='mot')
    ],
    playbook=[
        app_commands.Choice(name="ace", value="ace"),
        app_commands.Choice(name="inheritor", value="inheritor"),
        app_commands.Choice(name="persona", value="persona"),
        app_commands.Choice(name="ranger", value="ranger"),
        app_commands.Choice(name="relic", value="relic"),
        app_commands.Choice(name="ronin", value="ronin"),
        app_commands.Choice(name="royal", value="royal"),
        app_commands.Choice(name="transfer", value="transfer"),
        app_commands.Choice(name="witch", value="witch")
    ]
)
async def playbooks5p(interaction: discord.Interaction, choice: str, playbook: str = None):
    from playbooks import get_playbook_component_slash
    logger.info(f"{interaction.guild}|{interaction.user.display_name}|{interaction.data}")
    result = get_playbook_component_slash(choice, interaction, 'en', playbook)
    await interaction.response.send_message(embed=result)


# --- Influence Buttons View ---
class InfluenceView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, char_info):
        super().__init__(timeout=None)
        self.original_interaction = interaction
        self.char_info = char_info
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        for char in self.char_info['influenceOver']:
            style = discord.ButtonStyle.green if char['hasInfluence'] else discord.ButtonStyle.grey
            button = discord.ui.Button(style=style, label=char['id'], custom_id=f"influence_{char['id']}")
            button.callback = self.make_callback(char['id'])
            self.add_item(button)

    def make_callback(self, character_name):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.original_interaction.user.id:
                await interaction.response.send_message("You are not authorized to change the influence status.", ephemeral=True)
                return

            from playbook_interactions import invert_influence
            invert_influence(interaction, character_name, self.char_info)
            self.update_buttons()
            await interaction.response.edit_message(content="Toggle influence over characters:", view=self)
        return callback


@bot.tree.command(name="me", description="Retrieve character information")
@app_commands.choices(
    choice=[
        app_commands.Choice(name='Print Character', value='print'),
        app_commands.Choice(name='Show Labels', value='labels'),
        app_commands.Choice(name='Show Conditions', value='conditions'),
        app_commands.Choice(name='Show Party', value='party'),
        app_commands.Choice(name='Show Influence', value='influence')
    ]
)
async def me(interaction: discord.Interaction, choice: str):
    from playbook_interactions import print_playbook_slash, get_conditions_slash, get_labels_slash, print_party, get_influence
    logger.info(f"{interaction.guild}|{interaction.user.display_name}|{interaction.data}")
    
    if choice == 'print':
        await interaction.response.send_message(print_playbook_slash(interaction, 'en'))
    elif choice == 'conditions':
        await interaction.response.send_message(get_conditions_slash(interaction, 'en'))
    elif choice == 'labels':
        await interaction.response.send_message(get_labels_slash(interaction, 'en'))
    elif choice == 'party':
        await interaction.response.send_message(print_party(interaction, 'en'))
    elif choice == 'influence':
        char_info = get_influence(interaction, 'en')
        if char_info in ["I'm sorry but it appears you have no character created", "No other players in the party."]:
            await interaction.response.send_message(char_info)
        elif len(char_info['influenceOver']) <= 1:
            await interaction.response.send_message("No other players in the party.")
        else:
            view = InfluenceView(interaction, char_info)
            await interaction.response.send_message("Toggle influence over characters:", view=view)


# --- Battle View ---
class BattleView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, team_stat, embed):
        super().__init__(timeout=None) # Or add a timeout if you want it to expire
        self.original_interaction = interaction
        self.team_stat = team_stat
        self.embed = embed

        self.button_states = {
            "add_2_team": False,
            "leader_influence": False,
            "same_purpose": False,
            "mistrust": False,
            "ill_prepared": False
        }
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        
        b1 = discord.ui.Button(style=discord.ButtonStyle.blurple if not self.button_states["add_2_team"] else discord.ButtonStyle.gray, label="Add 2 Team", custom_id="add_2_team")
        b2 = discord.ui.Button(style=discord.ButtonStyle.green if not self.button_states["leader_influence"] else discord.ButtonStyle.gray, label="Leader has influence?", custom_id="leader_influence")
        b3 = discord.ui.Button(style=discord.ButtonStyle.green if not self.button_states["same_purpose"] else discord.ButtonStyle.gray, label="Same purpose?", custom_id="same_purpose")
        b4 = discord.ui.Button(style=discord.ButtonStyle.red if not self.button_states["mistrust"] else discord.ButtonStyle.gray, label="Mistrust leader or team?", custom_id="mistrust")
        b5 = discord.ui.Button(style=discord.ButtonStyle.red if not self.button_states["ill_prepared"] else discord.ButtonStyle.gray, label="Ill-prepared/off balance?", custom_id="ill_prepared")

        for b in [b1, b2, b3, b4, b5]:
            b.callback = self.make_callback(b.custom_id)
            self.add_item(b)

    def make_callback(self, custom_id):
        async def callback(interaction: discord.Interaction):
            self.button_states[custom_id] = not self.button_states[custom_id]
            prev_team = self.team_stat

            if custom_id == "add_2_team":
                self.team_stat = team_slash(interaction, 'en', 'increase_twice') if self.button_states[custom_id] else None
            elif custom_id == "leader_influence":
                self.team_stat = team_slash(interaction, 'en', 'increase') if self.button_states[custom_id] else team_slash(interaction, 'en', 'decrease')
            elif custom_id == "same_purpose":
                self.team_stat = team_slash(interaction, 'en', 'increase') if self.button_states[custom_id] else team_slash(interaction, 'en', 'decrease')
            elif custom_id == "mistrust":
                self.team_stat = team_slash(interaction, 'en', 'decrease') if self.button_states[custom_id] else team_slash(interaction, 'en', 'increase')
            elif custom_id == "ill_prepared":
                self.team_stat = team_slash(interaction, 'en', 'decrease') if self.button_states[custom_id] else team_slash(interaction, 'en', 'increase')

            if prev_team != self.team_stat:
                self.embed.add_field(name=self.team_stat, value=f'\nTeam has been updated to {self.team_stat}.')
            
            self.update_buttons()
            await interaction.response.edit_message(content=self.team_stat, embed=self.embed, view=self)
        return callback

@bot.tree.command(name="battle", description="Enter Battle")
async def battle(interaction: discord.Interaction):
    embed, addendum = slash_parse(interaction, 153, 0)
    team_stat = team_slash(interaction, 'en', 'check')
    
    view = BattleView(interaction, team_stat, embed)
    await interaction.response.send_message(content=team_stat, embed=embed, view=view)


# include generated slash commands file as if it's written inside this one:
with open(os.path.join(os.path.normpath(os.path.join(os.path.realpath(__file__), os.pardir)), "generated_commands.py")) as generated_code:
    exec(generated_code.read())

bot.run(TOKEN)
