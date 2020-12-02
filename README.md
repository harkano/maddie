# maddie

Masks Automated Discord Dice Interpreter &amp; Explainer!

# Add Maddie to Your Server

https://discordapp.com/api/oauth2/authorize?client_id=696512126675583026&permissions=101440&scope=bot

# Maddie Commands 

`!help` - Displays all commands

Syntax is as follows - `move+/-label` e.g.

`!engage+3`

`!support-2`

If you're using a custom or playbook move not covered here you can use `!other+1`
The idea is to save you having the generic moves sheet open at any time.
  
You can be pretty messy with the command as it uses regular expression matches, it will also only use the first number in the command, and assumes a + if there's no modifier.  So you should be able to `!   unleash234` to get an Unleash+2.  Note that it currently doesn't support prefix changes, so it doesn't play with with other ! prefix bots.

![Loud Mode](https://i.imgur.com/MtVp1KM.png "Loud Mode")

I will be quieter if you prefix with !! (once you're comfortable with the detailed results) e.g. `!!unleash+2`

![Quiet Mode](https://i.imgur.com/5iVp7FK.png "Quiet Mode")

Type `!moves` to see the the basic moves.
Type `!moves+` to get a more detailed explanation of all moves.

# Basic moves
`!engage`  - DIRECTLY ENGAGE A THREAT
`!unleash` - UNLEASH YOUR POWERS
etc.
`!moves` for more.

# Playbook moves
`!playbooks` lists all available playbooks
`!nomad` lists all moves in that playbook

# Adult moves
`!wield`     - WIELD YOUR POWERS
`!adult` for more.

# Moment of Truth!
`!mot beacon` will display your playbook's Moment of Truth text.

# Change the character sheet!
- `!create beacon Beacon-man Maddie mundane` will create a new character, _Beacon-man_, that is played by _Maddie_, that is a _beacon_ and has the initial labels plus one in _mundane_ (All 20 core game and expansion playbooks are supported).
- `!editlabels mundane freak` will shift mundane up and freak(if _mundane_ isn't in +3 and _freak_ in -2 and neither of them is blocked) for the character of the player that sent the message.
- `!lock mundane` will lock mundane if it wasn't already.
- `!potential` will add a potential to you pool. If you reach 5 of them m.a.d.d.i.e. will tell you how many unresolved advances you have.
- `!markcondition angry` will mark _angry_ if it wasn't alread.
- `!clearcondition` will clear _angry_ if it was marked.

# Configure settings for the chat!
- `!create_settings en` will create a configuration file in english. The other language supported is spanish (es).
- `!update_lang es` will change the language to the language sent. 
- `!update_gm` will set or update a gm for the adventure played in the chat.
- `!update_teamname` will set or update the team name of young heroes.
- `!settings` will return all the current settings saved.
- `!language` will return the language that is set (just the short name, like en or es).
- `!teamname` will return the name of the team.

# Make advancements!
- `mov_my_playbook move_name` will add the name with the accessor move_name (if it is from your playbook) to your moves.
- `mov_other_playbook move_name` will do the same as the last command but for moves from another playbook.
- `rearrange 0 0 0 0 0` will set your label values (freak, danger, savior, superior, mundane) in order as long as : 
  - none of those values is less than -2
  - none of those values is more than 3
  - the sum is one more than the sum of the previous values
- `more_roles defender friend` will add more roles to the bulls heart. **Only for BULL**.  The roles are:
  - defender
  - friend
  - listener
  - enabler
- `add_adult persuade` will add the adult move specified.
- `more_to_labels danger freak` will add one to both specified labels. **Only for DELINQUENT**.
- `clear_sign` clears a doomsign. **Only for DOOMED**.
- `get_burns` get the burns and three flares from the Nova. **Only for DOOMED and NEWBORN**. 
- `mask_label freak` will let you change your mask label. **Only for JANUS**.
- `get_drives` will let you get the drives from the Beacon. **Only for JANUS and REFORMED**.
- `get_sanctuary` lets you acquire a sanctuary from the Doomed. **Only for LEGACY**.
- `more_flares` lets you add 3 more flares. **Only for NOVA**.
- `get_heart` lets you get the Bulls heart. **Only for NOVA**.
- `get_mask` lets you get the Janus secret identity and mask. **Only for OUTSIDER and SCION**.
- `mentor_label` lets you add one to the label your mentor enbodies or denies. **Only for PROTEGE**.
- `more_resources` lets you get more resources from your mentos. **Only for PROTEGE**.
- `get_mentor` lets you get a mentor from the Protege. **Only for innocent**.
- `get_legacy` lets you be a part of a superhero tradition. **Only for STAR**.
- `lock_soldier` lets you lock the soldier label. **Only for SOLDIER**.

# Dataset

Note that the moveset is designed by a very open JSON format, so I'm potentially interested in adapting this for a variety of PBTA movesets.  I just wanted to run Masks first :)
e.g.
![JSON Data](https://i.imgur.com/qmUCXWW.png "JSON")

# Future Enhancements

Currently she's deployed on AWS Free Tier, and I need to hook it up properly so you can release from here.

I've got a protoype of prefix changing in the 2.0 version, but it loses a lot of command parsing flexiblity.

I'm also interested in connecting to an online character sheet, but that's still pending me learning a lot more about web programming.

# Credits

Special Graphics thanks to - Chordial#6969

For any feedback, feature request or bug reports please visit our Discord @ https://discord.gg/7p8g8H5 'Harkano (Ross) #7019'

Masks The New Generation is a Powered by the Apocalypse RPG designed by Brendan Conway and team @ http://magpiegames.com
