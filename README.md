# maddie

Masks Automated Discord Dice Interpreter &amp; Explainer!

# Add Maddie to Your Server

https://discordapp.com/channels/696999350726819931/697551365362417664/697551552550010891

# Maddie Commands 

`!help` - Displays all commands

Syntax is as follows - `move+/-label` e.g.

`!engage+3`

`!support-2`

If you're using a playbook move not covered here you can use `!other+1`
The idea is to save you having the generic moves sheet open at any time.
  
You can be pretty messy with the command as it uses regular expression matches, it will also only use the first number in the command, and assumes a + if there's no modifier.  So you should be able to `!   unleash234` to get an Unleash+2.  Note that it currently doesn't support prefix changes, so it doesn't play with with other ! prefix bots.

![Loud Mode](https://i.imgur.com/MtVp1KM.png "Loud Mode")

I will be a bit less verbose if you prefix with !! (once you're comfortable with the detailed results) e.g. `!!unleash+2`

![Quiet Mode](https://i.imgur.com/5iVp7FK.png "Quiet Mode")

Type `!moves` to see the short version of help.
Type `!moves+` to get a more detailed explanation of all moves.

# Basic moves
`!engage`  - DIRECTLY ENGAGE A THREAT

`!unleash` - UNLEASH YOUR POWERS

`!comfort` - COMFORT OR SUPPORT

`!pierce`  - PIERCE THE MASK

`!defend`  - DEFEND

`!assess`  - ASSESS THE SITUATION

`!provoke` - PROVOKE SOMEONE

`!take`    - TAKE A POWERFUL BLOW

`!reject`  - REJECT SOMEONE'S INFLUENCE

`!other`   - ANY OTHER PLAYBOOK MOVE

# Adult moves
`!wield`     - WIELD YOUR POWERS

`!overwhelm` - OVERWHELM A VULNERABLE FOE

`!persuade`  - PERSUADE WITH BEST INTERESTS

`!empathize` - EMPATHIZE

`!standup`   - STAND UP FOR SOMETHING

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

