import os
import discord
from discord import app_commands
import logging
from parse import slash_parse
from config_interactions import team_slash
from storage import info_from_s3, get_s3_client, TOP_DIR

logger = logging.getLogger('discord')

async def setup(bot):
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

    class MarkConditionView(discord.ui.View):
        def __init__(self, original_interaction):
            super().__init__()
            self.original_interaction = original_interaction

        @discord.ui.select(placeholder="Select a condition to mark", options=[
            discord.SelectOption(label="Afraid", value="afraid"),
            discord.SelectOption(label="Angry", value="angry"),
            discord.SelectOption(label="Guilty", value="guilty"),
            discord.SelectOption(label="Hopeless", value="hopeless"),
            discord.SelectOption(label="Insecure", value="insecure"),
            discord.SelectOption(label="Damaged", value="damaged"),
        ])
        async def select_callback(self, select_interaction: discord.Interaction, select: discord.ui.Select):
            if select_interaction.user.id != self.original_interaction.user.id:
                await select_interaction.response.send_message("This menu is not for you.", ephemeral=True)
                return
            from playbook_interactions import condition_slash
            result = condition_slash(select_interaction, 'en', select.values[0], 'mark')
            await select_interaction.response.send_message(result, ephemeral=True)
            
    class ClearConditionView(discord.ui.View):
        def __init__(self, original_interaction):
            super().__init__()
            self.original_interaction = original_interaction

        @discord.ui.select(placeholder="Select a condition to clear", options=[
            discord.SelectOption(label="Afraid", value="afraid"),
            discord.SelectOption(label="Angry", value="angry"),
            discord.SelectOption(label="Guilty", value="guilty"),
            discord.SelectOption(label="Hopeless", value="hopeless"),
            discord.SelectOption(label="Insecure", value="insecure"),
            discord.SelectOption(label="Damaged", value="damaged"),
        ])
        async def select_callback(self, select_interaction: discord.Interaction, select: discord.ui.Select):
            if select_interaction.user.id != self.original_interaction.user.id:
                await select_interaction.response.send_message("This menu is not for you.", ephemeral=True)
                return
            from playbook_interactions import condition_slash
            result = condition_slash(select_interaction, 'en', select.values[0], 'clear')
            await select_interaction.response.send_message(result, ephemeral=True)

    class SelectMoveView(discord.ui.View):
        def __init__(self, original_interaction, char_info, all_moves):
            super().__init__()
            self.original_interaction = original_interaction
            unpicked = [
                m for m in char_info.get('moves', [])
                if not m.get('picked', False)
            ]
            options = []
            for char_move in unpicked[:25]:
                move_data = next((mv for mv in all_moves if str(mv['id']) == str(char_move.get('id'))), None)
                if move_data:
                    options.append(discord.SelectOption(
                        label=move_data.get('capital', f"Move {char_move.get('id')}")[:100],
                        value=str(char_move.get('id')),
                        description=move_data.get('blob', '')[:100],
                    ))
            if not options:
                options = [discord.SelectOption(label="No unpicked moves available", value="none")]
            select = discord.ui.Select(
                placeholder="Select a move to pick",
                options=options,
            )
            select.callback = self.select_callback
            self.add_item(select)

        async def select_callback(self, select_interaction: discord.Interaction):
            if select_interaction.user.id != self.original_interaction.user.id:
                await select_interaction.response.send_message("This menu is not for you.", ephemeral=True)
                return
            move_id = select_interaction.data['values'][0]
            if move_id == "none":
                await select_interaction.response.send_message("No moves available to pick.", ephemeral=True)
                return
            from playbook_interactions import toggle_move_picked
            result = toggle_move_picked(select_interaction, move_id, True)
            await select_interaction.response.send_message(result, ephemeral=True)

    class RemoveMoveView(discord.ui.View):
        def __init__(self, original_interaction, char_info, all_moves):
            super().__init__()
            self.original_interaction = original_interaction
            picked = [
                m for m in char_info.get('moves', [])
                if m.get('picked', False)
            ]
            options = []
            for char_move in picked[:25]:
                move_data = next((mv for mv in all_moves if str(mv['id']) == str(char_move.get('id'))), None)
                if move_data:
                    options.append(discord.SelectOption(
                        label=move_data.get('capital', f"Move {char_move.get('id')}")[:100],
                        value=str(char_move.get('id')),
                        description=move_data.get('blob', '')[:100],
                    ))
            if not options:
                options = [discord.SelectOption(label="No picked moves to remove", value="none")]
            select = discord.ui.Select(
                placeholder="Select a move to remove",
                options=options,
            )
            select.callback = self.select_callback
            self.add_item(select)

        async def select_callback(self, select_interaction: discord.Interaction):
            if select_interaction.user.id != self.original_interaction.user.id:
                await select_interaction.response.send_message("This menu is not for you.", ephemeral=True)
                return
            move_id = select_interaction.data['values'][0]
            if move_id == "none":
                await select_interaction.response.send_message("No moves available to remove.", ephemeral=True)
                return
            from playbook_interactions import toggle_move_picked
            result = toggle_move_picked(select_interaction, move_id, False)
            await select_interaction.response.send_message(result, ephemeral=True)

    class MeDashboardView(discord.ui.View):
        def __init__(self, original_interaction):
            super().__init__(timeout=None)
            self.original_interaction = original_interaction

        @discord.ui.button(label="Print Character", style=discord.ButtonStyle.primary, custom_id="dashboard_print", row=0)
        async def print_character(self, interaction: discord.Interaction, _button: discord.ui.Button):
            if interaction.user.id != self.original_interaction.user.id:
                await interaction.response.send_message("This dashboard is not for you.", ephemeral=True)
                return
            from playbook_interactions import print_playbook_slash
            await interaction.response.send_message(print_playbook_slash(interaction, 'en'), ephemeral=True)

        @discord.ui.button(label="Show Labels", style=discord.ButtonStyle.secondary, custom_id="dashboard_labels", row=0)
        async def show_labels(self, interaction: discord.Interaction, _button: discord.ui.Button):
            if interaction.user.id != self.original_interaction.user.id:
                await interaction.response.send_message("This dashboard is not for you.", ephemeral=True)
                return
            from playbook_interactions import get_labels_slash
            await interaction.response.send_message(get_labels_slash(interaction, 'en'), ephemeral=True)

        @discord.ui.button(label="Show Conditions", style=discord.ButtonStyle.secondary, custom_id="dashboard_conditions", row=0)
        async def show_conditions(self, interaction: discord.Interaction, _button: discord.ui.Button):
            if interaction.user.id != self.original_interaction.user.id:
                await interaction.response.send_message("This dashboard is not for you.", ephemeral=True)
                return
            from playbook_interactions import get_conditions_slash
            await interaction.response.send_message(get_conditions_slash(interaction, 'en'), ephemeral=True)

        @discord.ui.button(label="Show Advancements", style=discord.ButtonStyle.success, custom_id="dashboard_advancements", row=0)
        async def show_advancements(self, interaction: discord.Interaction, _button: discord.ui.Button):
            if interaction.user.id != self.original_interaction.user.id:
                await interaction.response.send_message("This dashboard is not for you.", ephemeral=True)
                return
            # Note: get_advancements expects message, we use context logic
            key = f'{getattr(interaction.channel, "id", getattr(interaction, "channel_id", None))}/{interaction.user.id}'
            char_info = info_from_s3(key, get_s3_client())
            if not char_info:
                await interaction.response.send_message("I'm sorry but it appears you have no character created", ephemeral=True)
                return
            from playbook_interactions import format_advancements
            await interaction.response.send_message(format_advancements(char_info["advancement"], 'en'), ephemeral=True)

        @discord.ui.button(label="Show Moves", style=discord.ButtonStyle.secondary, custom_id="dashboard_moves", row=1)
        async def show_moves(self, interaction: discord.Interaction, _button: discord.ui.Button):
            if interaction.user.id != self.original_interaction.user.id:
                await interaction.response.send_message("This dashboard is not for you.", ephemeral=True)
                return
            from playbook_interactions import get_moves_slash
            await interaction.response.send_message(get_moves_slash(interaction, 'en'), ephemeral=True)

        @discord.ui.button(label="Select Move", style=discord.ButtonStyle.success, custom_id="dashboard_select_move", row=2)
        async def select_move_btn(self, interaction: discord.Interaction, _button: discord.ui.Button):
            if interaction.user.id != self.original_interaction.user.id:
                await interaction.response.send_message("This dashboard is not for you.", ephemeral=True)
                return
            key = f'{getattr(interaction.channel, "id", getattr(interaction, "channel_id", None))}/{interaction.user.id}'
            char_info = info_from_s3(key, get_s3_client())
            if not char_info:
                await interaction.response.send_message("I'm sorry but it appears you have no character created", ephemeral=True)
                return
            with open('data.json', 'r') as f:
                all_moves = json.load(f)['moves']
            await interaction.response.send_message("Which move do you want to pick?", view=SelectMoveView(interaction, char_info, all_moves), ephemeral=True)

        @discord.ui.button(label="Remove Move", style=discord.ButtonStyle.danger, custom_id="dashboard_remove_move", row=2)
        async def remove_move_btn(self, interaction: discord.Interaction, _button: discord.ui.Button):
            if interaction.user.id != self.original_interaction.user.id:
                await interaction.response.send_message("This dashboard is not for you.", ephemeral=True)
                return
            key = f'{getattr(interaction.channel, "id", getattr(interaction, "channel_id", None))}/{interaction.user.id}'
            char_info = info_from_s3(key, get_s3_client())
            if not char_info:
                await interaction.response.send_message("I'm sorry but it appears you have no character created", ephemeral=True)
                return
            with open('data.json', 'r') as f:
                all_moves = json.load(f)['moves']
            await interaction.response.send_message("Which move do you want to remove?", view=RemoveMoveView(interaction, char_info, all_moves), ephemeral=True)

        @discord.ui.button(label="Toggle Influence", style=discord.ButtonStyle.secondary, custom_id="dashboard_influence", row=1)
        async def toggle_influence(self, interaction: discord.Interaction, _button: discord.ui.Button):
            if interaction.user.id != self.original_interaction.user.id:
                await interaction.response.send_message("This dashboard is not for you.", ephemeral=True)
                return
            from playbook_interactions import get_influence
            char_info = get_influence(interaction, 'en')
            if char_info in ["I'm sorry but it appears you have no character created", "No other players in the party."]:
                await interaction.response.send_message(char_info, ephemeral=True)
            elif len(char_info['influenceOver']) <= 1:
                await interaction.response.send_message("No other players in the party.", ephemeral=True)
            else:
                view = InfluenceView(interaction, char_info)
                await interaction.response.send_message("Toggle your influence over characters:", view=view, ephemeral=True)

        @discord.ui.button(label="Mark Condition", style=discord.ButtonStyle.danger, custom_id="dashboard_mark", row=1)
        async def mark_condition_btn(self, interaction: discord.Interaction, _button: discord.ui.Button):
            if interaction.user.id != self.original_interaction.user.id:
                await interaction.response.send_message("This dashboard is not for you.", ephemeral=True)
                return
            await interaction.response.send_message("Which condition do you want to mark?", view=MarkConditionView(interaction), ephemeral=True)

        @discord.ui.button(label="Clear Condition", style=discord.ButtonStyle.primary, custom_id="dashboard_clear", row=1)
        async def clear_condition_btn(self, interaction: discord.Interaction, _button: discord.ui.Button):
            if interaction.user.id != self.original_interaction.user.id:
                await interaction.response.send_message("This dashboard is not for you.", ephemeral=True)
                return
            await interaction.response.send_message("Which condition do you want to clear?", view=ClearConditionView(interaction), ephemeral=True)

    @bot.tree.command(name="me", description="Retrieve character information via a Dashboard")
    async def me(interaction: discord.Interaction):
        from playbook_interactions import get_character_ctx
        logger.info(f"{interaction.guild}|{interaction.user.display_name}|Opened /me dashboard")
        char_info = get_character_ctx(interaction)
        
        if not char_info:
            await interaction.response.send_message("You don't have a character in this channel.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"Dashboard: {char_info.get('characterName', 'Unknown Character')}",
            description=f"A {char_info.get('playbook', 'Unknown').capitalize()} played by {char_info.get('playerName', interaction.user.display_name)}",
            color=0x53B0B9
        )
        embed.add_field(name="Potential", value=f"{char_info.get('potential', 0)}/5", inline=False)
        embed.set_footer(text="Use the buttons below to interact with your character sheet.")

        view = MeDashboardView(interaction)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @bot.tree.command(name="stats", description="Bot Admin - Show usage stats across servers")
    async def stats(interaction: discord.Interaction):
        logger.info(f"{interaction.guild}|{interaction.user.display_name}|Opened /stats dashboard")
        # Ensure we only allow admin/owner usage or restrict to people who need it.
        # But as per request, just making a lightweight low-overhead dashboard.

        # Calculate metrics by scanning the TOP_DIR quickly
        total_guilds = len(bot.guilds)
        total_users_bot_sees = len(bot.users)

        total_channels_with_data = 0
        total_characters = 0

        if os.path.exists(TOP_DIR):
            for entry in os.listdir(TOP_DIR):
                channel_path = os.path.join(TOP_DIR, entry)
                if os.path.isdir(channel_path):
                    total_channels_with_data += 1
                    # count .json files inside it
                    json_files = [f for f in os.listdir(channel_path) if f.endswith(".json")]
                    # exclude settings.json from character count
                    char_files = [f for f in json_files if f != "settings.json"]
                    total_characters += len(char_files)

        embed = discord.Embed(
            title="Maddie Stats Dashboard",
            description="Quick overview of Maddie's usage and resources.",
            color=0x53B0B9
        )
        
        embed.add_field(name="Servers (Guilds)", value=str(total_guilds), inline=True)
        embed.add_field(name="Visible Users", value=str(total_users_bot_sees), inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True) # spacer
        
        embed.add_field(name="Active Channels", value=str(total_channels_with_data), inline=True)
        embed.add_field(name="Characters Created", value=str(total_characters), inline=True)

        # Get very basic memory usage info natively in python, since it's a 1GB google cloud device.
        try:
            import resource
        except ImportError:
            # resource module is Unix only
            embed.set_footer(text="Memory footprint: Unavailable on this OS")
        else:
            usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            # ru_maxrss is kilobytes on Linux
            memory_mb = usage / 1024.0
            embed.set_footer(text=f"Memory footprint: {memory_mb:.2f} MB")

        await interaction.response.send_message(embed=embed, ephemeral=True)


    class BattleView(discord.ui.View):
        def __init__(self, interaction: discord.Interaction, team_stat, embed):
            super().__init__(timeout=None)
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

    # --- Right-Click Context Menus ---

    # Right-click a Message -> "Spend Team"
    @bot.tree.context_menu(name="Spend Team")
    async def context_spend_team(interaction: discord.Interaction, message: discord.Message):
        from config_interactions import team_slash
        logger.info(f"{interaction.guild}|{interaction.user.display_name}|Context Menu: Spend Team")
        
        # Spend a team pool
        result = team_slash(interaction, 'en', 'decrease')
        
        await interaction.response.send_message(
            content=f"You spent a Team on [this roll]({message.jump_url})! {result}"
        )

    # Right-click a User -> "View Character"
    @bot.tree.context_menu(name="View Character")
    async def context_view_character(interaction: discord.Interaction, member: discord.Member):
        logger.info(f"{interaction.guild}|{interaction.user.display_name}|Context Menu: View Character for {member.display_name}")
        
        # Fetch their info from storage
        channel_id = getattr(interaction.channel, "id", getattr(interaction, "channel_id", None))
        key = f'{channel_id}/{member.id}'
        char_info = info_from_s3(key, get_s3_client())
        
        if not char_info:
            await interaction.response.send_message(
                f"{member.display_name} doesn't have a character in this channel.", 
                ephemeral=True
            )
            return
            
        embed = discord.Embed(
            title=char_info.get("characterName", "Unknown Character"),
            description=f"A {char_info.get('playbook', 'Unknown').capitalize()} played by {char_info.get('playerName', member.display_name)}",
            color=0x53B0B9
        )
        
        # Add labels
        from playbook_interactions import format_labels
        labels_str = format_labels(char_info.get("labels", {}), 'en')
        embed.add_field(name="Labels", value=labels_str, inline=True)
        
        # Add conditions
        from playbook_interactions import format_conditions
        cond_str = format_conditions(char_info.get("conditions", {}), 'en')
        embed.add_field(name="Conditions", value=cond_str, inline=True)
        
        # Add potential
        embed.add_field(name="Potential", value=f"{char_info.get('potential', 0)}/5", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # Right-click a User -> "View Influence"
    @bot.tree.context_menu(name="View Influence")
    async def context_view_influence(interaction: discord.Interaction, member: discord.Member):
        logger.info(f"{interaction.guild}|{interaction.user.display_name}|Context Menu: View Influence for {member.display_name}")
        
        # If they right clicked themselves, use the existing me/influence UI
        if member.id == interaction.user.id:
            from playbook_interactions import get_influence
            char_info = get_influence(interaction, 'en')
            if char_info in ["I'm sorry but it appears you have no character created", "No other players in the party."]:
                await interaction.response.send_message(char_info, ephemeral=True)
            elif len(char_info['influenceOver']) <= 1:
                await interaction.response.send_message("No other players in the party.", ephemeral=True)
            else:
                view = InfluenceView(interaction, char_info)
                await interaction.response.send_message("Toggle your influence over characters:", view=view, ephemeral=True)
        else:
            await interaction.response.send_message("You can only manage your own influence. Right-click yourself instead!", ephemeral=True)

    # Right-click a User -> "Add Potential"
    @bot.tree.context_menu(name="Add Potential")
    async def context_add_potential(interaction: discord.Interaction, member: discord.Member):
        logger.info(f"{interaction.guild}|{interaction.user.display_name}|Context Menu: Add Potential for {member.display_name}")
        if member.id == interaction.user.id:
            from playbook_interactions import mark_potential_slash
            result = mark_potential_slash(interaction, 'en')
            await interaction.response.send_message(result, ephemeral=True)
        else:
            await interaction.response.send_message("You can only add potential for your own character. Right-click yourself instead!", ephemeral=True)

    # Right-click a User -> "Remove Potential"
    @bot.tree.context_menu(name="Remove Potential")
    async def context_remove_potential(interaction: discord.Interaction, member: discord.Member):
        logger.info(f"{interaction.guild}|{interaction.user.display_name}|Context Menu: Remove Potential for {member.display_name}")
        if member.id == interaction.user.id:
            from playbook_interactions import remove_potential_slash
            result = remove_potential_slash(interaction, 'en')
            await interaction.response.send_message(result, ephemeral=True)
        else:
            await interaction.response.send_message("You can only remove potential for your own character. Right-click yourself instead!", ephemeral=True)

    # Right-click a User -> "Lock Label"
    @bot.tree.context_menu(name="Lock Label")
    async def context_lock_label(interaction: discord.Interaction, member: discord.Member):
        if member.id != interaction.user.id:
            await interaction.response.send_message("You can only lock labels for your own character. Right-click yourself instead!", ephemeral=True)
            return

        class LockLabelView(discord.ui.View):
            def __init__(self, original_interaction):
                super().__init__()
                self.original_interaction = original_interaction

            @discord.ui.select(placeholder="Select a label to lock", options=[
                discord.SelectOption(label="Danger", value="danger"),
                discord.SelectOption(label="Freak", value="freak"),
                discord.SelectOption(label="Savior", value="savior"),
                discord.SelectOption(label="Superior", value="superior"),
                discord.SelectOption(label="Mundane", value="mundane"),
                discord.SelectOption(label="Soldier", value="soldier"),
            ])
            async def select_callback(self, select_interaction: discord.Interaction, select: discord.ui.Select):
                if select_interaction.user.id != self.original_interaction.user.id:
                    await select_interaction.response.send_message("This menu is not for you.", ephemeral=True)
                    return
                from playbook_interactions import lock_label_slash
                result = lock_label_slash(select_interaction, 'en', select.values[0])
                await select_interaction.response.send_message(result, ephemeral=True)

        await interaction.response.send_message("Which label do you want to lock?", view=LockLabelView(interaction), ephemeral=True)


    # dynamically exec the generated slash commands into this file
    # we don't need to do this here anymore, generated_commands is imported directly in maddie.py
    # with open(os.path.join(os.path.normpath(os.path.join(os.path.realpath(__file__), os.pardir)), "generated_commands.py")) as generated_code:
    #     exec(generated_code.read())