import re

##Setup the big sub
def mad_parse(msg,user):
    blob = ""
    capital = ""
    phrase = ""
    word = ""
    mod = ""
    num = int(0)
    quiet = 0
    match = 0
    # parse command into parts
    msg = msg.lower()
    searchStr1 = r'[a-z]+'
    searchStr2 = r'[\+\-]'
    searchStr3 = r'[1234567890]'
    log_line = ''
    result1 = re.search(searchStr1, msg)
    if result1:
        log_line = log_line + result1.group(0)
        word = result1.group(0)
    else: log_line = log_line + "no cmd "
    result2 = re.search(searchStr2, msg)
    if result2:
        log_line = log_line + result2.group()
        mod = result2.group(0)
    else: log_line = log_line + "no mod "
    result3 = re.search(searchStr3, msg)
    if result3:
        log_line = log_line + result3.group(0)
        num = int(result3.group(0))
    else: log_line = log_line + "no num "
    logger.info (msg + log_line)
 # figure out which type of modifier it is
    num_calc = get_modified_num(mod, num)
 # lookup a table for the big blob of text and a wee blob
    for p in json_array['moves']:
        if p['shortName'] == word:
            blob = p['blob']
            capital = p['capital']
            phrase = p['phrase']
            img = p['img']
            roll = p['requiresRolling']
            match = 1
    #Quiet mode
    searchStr4 = r'!!'
    result4 = re.search(searchStr4, msg)
    if result4: quiet = 1
#Ugly format blob!
    if match == 1 : #lets us ignore ! prefix commands that aren't in our list
        embed=discord.Embed(title=f"{capital}")
        embed.set_author(name=f"{user} {phrase}")
        embed.set_thumbnail(url=img)
        if quiet == 0: embed.add_field(name="Description", value=f"{blob}") # don't include the blob if we're in quiet mode (!!)
        if roll:
            add_result(embed, num_calc, mod)
        embed.set_footer(text=" ")

        return embed

    else:
        logger.info('no match found for '+msg)
        return 0

