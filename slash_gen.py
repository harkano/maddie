#!/usr/bin/env python3
import json
from string import Template
import argparse
import pathlib


def parse_file(data_file):
    OTHER = 'other'
    top_commands = {OTHER: dict()}
    data = json.load(data_file)
    playbooks = data['playbooks']
    moves = data['moves']
    # We probably won't use this one.
    sources = data['sources']

    adult = {"id": 99, "name":'adult'}
    basic = {"id": 98, "name":'basic'}

    #Add basic and adult moves
    playbooks.append(adult)
    playbooks.append(basic)

    for playbook in playbooks:
        if top_commands.get(playbook['name']) is None:
            top_commands[playbook['name']] = dict()
        else:
            print("Error, data file contains duplicate playbook {}".format(playbook['name']))
    for move in moves:
        playbook = move.get('playbook')
        if playbook is not None:
            top = top_commands.get(playbook)
            if top is not None:
                if top.get(move['shortName']) is None:
                    top[move['shortName']] = {
                        'name': move['shortName'],
                        'description': move['capital'],
                        'id': move['id']
                    }
                else:
                    print("Error, data file contains duplicate move {}".format(move['shortName']))
        else:
            top = top_commands[OTHER]
            if top.get(move['shortName']) is None:
                top[move['shortName']] = {
                    'name': move['shortName'],
                    'description': move['capital'],
                    'id': move['id']
                }
            else:
                print("Error, data file contains duplicate move {}".format(move['shortName']))
    return top_commands


def generate_code(top_commands):
    generated_code = ""
    for command_name, command in top_commands.items():
        top_template = Template("""
@app_commands.command(
    name="$name",
    description="$name moves".title(),
)
@app_commands.choices(
    move=[
        $sub_commands
    ],
    modifier=[
        app_commands.Choice(name='+4', value=4),
        app_commands.Choice(name='+3', value=3),
        app_commands.Choice(name='+2', value=2),
        app_commands.Choice(name='+1', value=1),
        app_commands.Choice(name='0', value=0),
        app_commands.Choice(name='-1', value=-1),
        app_commands.Choice(name='-2', value=-2),
        app_commands.Choice(name='-3', value=-3)
    ]
)
async def slash_${name}(interaction: discord.Interaction, move: int, modifier: int=0):
    from parse import slash_parse
    logger.info(f"{interaction.guild}|{interaction.user.display_name}|{interaction.data}")
    # slash_parse needs to handle app_commands correctly, passing interaction or contextual data.
    # Currently passing 'ctx' equivalent as interaction.
    embed, addendum = slash_parse(interaction, move, modifier)
    if addendum:
        await interaction.response.send_message(embed=embed, content=addendum)
    else:
        await interaction.response.send_message(embed=embed)
""")
        sub_commands = []
        for sub_name, sub in command.items():
            sub_template = Template('app_commands.Choice(name="$description", value=$id)')
            sub_commands.append(sub_template.substitute(name=sub_name, id=sub['id'], description=sub['description']))
        generated_code += top_template.substitute(name=command_name, sub_commands=", ".join(sub_commands))
    return generated_code


def main(data_file, out_file):
    top_commands = parse_file(data_file)
    out_file.write(generate_code(top_commands))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Slash Command code from a given Masks data file.')
    parser.add_argument('--data-file', type=open, default="language_files/en.json",
                        help='Source Masks data file'
                        )
    parser.add_argument('dest_file', type=argparse.FileType('w', encoding='utf-8'),
                        help='Destination file for generated code'
                        )
    args = parser.parse_args()
    main(args.data_file, args.dest_file)
