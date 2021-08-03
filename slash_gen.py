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
                        'description': move['phrase']
                    }
                else:
                    print("Error, data file contains duplicate move {}".format(move['shortName']))
        else:
            top = top_commands[OTHER]
            if top.get(move['shortName']) is None:
                top[move['shortName']] = {
                    'name': move['shortName'],
                    'description': move['phrase']
                }
            else:
                print("Error, data file contains duplicate move {}".format(move['shortName']))
    return top_commands


def generate_code(top_commands):
    generated_code = ""
    for command_name, command in top_commands.items():
        top_template = Template("""
@slash.slash(
    name = "$name",
    description = "$name moves".title(),
    # Remove this argument to open up to all guilds, I guess?
    guild_ids = [696999350726819931],
    options = [
        create_option(name = 'move',
            description = 'Choose $name move',
            required = True,
            option_type = 3,
            choices = [
                $sub_commands
            ]
        ),
        create_option(name = 'modifier',
            description = "What modifier are we adding to the dice roll?",
            required = False,
            option_type = 4
        )
    ])
async def slash_${name}(ctx, move, modifier):
    from parse import mad_parse
    response = mad_parse("!" + move + " " + modifier)
    # this is incomplete
""")
        sub_commands = []
        for sub_name, sub in command.items():
            sub_template = Template('create_choice(name = "$description", value = "$name")')
            sub_commands.append(sub_template.substitute(name = sub_name, description = sub['description']))
        generated_code += top_template.substitute(name = command_name, sub_commands = ", ".join(sub_commands))
    return generated_code

def main(data_file, out_file):
    top_commands = parse_file(data_file)
    out_file.write(generate_code(top_commands))

parser = argparse.ArgumentParser(description = 'Generate Slash Command code from a given Masks data file.')
parser.add_argument('--data-file', type = open, default = "language_files/en.json",
                    help='Source Masks data file'
)
parser.add_argument('dest_file', type = argparse.FileType('w', encoding = 'utf-8'),
                    help = 'Destination file for generated code'
)
args = parser.parse_args()
main(args.data_file, args.dest_file)
