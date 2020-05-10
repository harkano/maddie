en = {
  "embed_commands": {
    "mot": "mot",
    "playbooks": "playbooks"
  },
  "plain_commands": {
    "helphere": "helphere",
    "lock": "lock",
    "editlabels": "editlabels",
    "potential": "potential",
    "markcondition": "markcondition",
    "clearcondition": "clearcondition",
    "create": "create",
    "settings": "settings",
    "changesettings": "change_settings",
    "language": "language",
    "teamname": "teamname",
    "updatelang": "update_lang",
    "updategm": "update_gm",
    "updateteamname": "update_teamname",
    "createsettings": "create_settings"
  },
  "dice_rolling": {
    "calculation_title": "Calculation",
    "calculation": lambda result1, result2, mod, calc: f"Dice **{result1}** + **{result2}**, Label{mod} **{calc}**",
    "dice": "Dice",
    "label": "Label",
    "result": "Result"
  },
  "description": "Description",
  "moves": {
    "moves": "moves",
    "adult": "adult",
    "non_existent_playbook_intro": "Sorry, I couldn't find that playbook, the available playbooks are:",
    "non_existent_playbook_end": "\nType an exclamation sign and one of the names in lowercase and without the 'The', moves or adult\ne.g.: !beacon, !moves, !adult",
    "moves_plus": {
      "response_header": "**Name - description, keyword, label**\n"
    }
  },
  "playbook_interactions": {
    "fail_preffix": "Oh no, ",
    "already_locked": lambda label_name: f"Oh no, {label_name} is already locked!",
    "is_locked": lambda label_name: f"Oh no, {label_name} is locked, this one can't change!",
    "labels_base": "Your labels are:\n",
    "up": "up",
    "down": "down",
    "value_is_in_border": lambda value, label_name, direction: f"Oh no, with a value of {value}, your {label_name} can't go {direction}! You get a condition!",
    "locked": "[LOCKED]",
    "condition_not_marked": "You don't have any condition marked",
    "youre": "You are:\n",
    "dont": "don't ",
    "condition_status": lambda status: f"Oh, you {status}have that condition marked.",
    "no_character": "I'm sorry but it appears you have no character created",
    "existing_character": "I'm sorry but it appears you already have character created",
    "invalid_condition": lambda condition_name: f"Oh no, {condition_name} is not a valid condition",
    "different_labels": "The labels must be different",
    "congrats_pending_advancements": lambda adv_count: f"Nice, you can now do {adv_count + 1} advancements",
    "congrats_potential": lambda potential: f"Nice, you have {potential + 1} potential marked",
    "no_template": lambda playbook_name: f"It seems I don't have a template for a playbook called {playbook_name}",
    "congrats_on_creation": lambda char, playbook: f"Congratulations {char}, The {playbook} on joining the team!",
    "potential": lambda potential: f"You have {potential} potential marked",
    "congrats_pending_advancements": lambda adv_count: f"You can do {adv_count + 1} advancements"
  },
  "labels": {
    "danger": "danger",
    "freak": "freak",
    "superior": "superior",
    "savior": "savior",
    "mundane": "mundane"
  },
  "inverted_labels": {
    "danger": "danger",
    "freak": "freak",
    "superior": "superior",
    "savior": "savior",
    "mundane": "mundane"
  },
  "conditions": {
    "afraid": "afraid",
    "angry": "angry",
    "guilty": "guilty",
    "hopeless": "hopeless",
    "insecure": "insecure"
  },
  "inverted_conditions": {
    "afraid": "afraid",
    "angry": "angry",
    "guilty": "guilty",
    "hopeless": "hopeless",
    "insecure": "insecure"
  },
  "playbooks": {
    "the": "The",
    "list": ['beacon', 'bull', 'delinquent', 'doomed', 'janus', 'legacy', 'nova', 'outsider', 'protege', 'transformed'],
    "playbooks": "Playbooks",
    "available": "Available Playbooks are - ",
    "playbook_re": r"!mot ([a-z]+)",
    "moment_of_truth": "MOMENT OF TRUTH",
    "this_is_mot": lambda usr: f"This is {usr}'s moment!"
  },
  "configuration": {
    "settings": "Settings\n",
    "language": "Language",
    "teamname": "Team name",
    "customNames": "Custom names",
    "no_file": "This chat doesn't have a configuration file. To create it write the following command:\n!adventure en\nif you wish for it to be in english.\n",
    "existing_settings": "This chat already has a configuration file.",
    "successfull_update": "The update was successfull",
    "successfull_creation": "The configuration file has been created"
  },
  "playbooks": {
    "advances": {
      "moveYouPlaybook": "Take another move from your playbook",
      "moveOtherPlaybook": "Take a move from another playbook",
      "loseInfluence": "Someone permanently loses Influence over you; add +1 to a Label",
      "rearrange": "Rearrange your Labels as you choose, and add +1 to a Label",
      "mot": "Unlock your Moment of Truth",
      "moreRoles": "Choose another two roles for the Bull's Heart", # Bull
      "motAgain": "Unlock your Moment of Truth after it's been used once",
      "playbookChange": "Change playbooks",
      "adult": "Take an adult move",
      "lock": "Lock a Label and add +1 to a Label your Choice",
      "retire": "Retire from the life or become a paragon of the city",
      "plusOne": "Add +1 to any two Labels", # Delinquent
      "clear": "Clear a doomsign; you lose access to that move for now", # Doom
      "burns": "Get burn and three flares (from the Nova's playbook)" # Doom
      "confront": "Confront your doom on your terms; if you survive, change playbooks", # Doom
      "paragon": "Become a paragon of the city for however long you have left", # Doom
      "maskLabel": "Change your mask's Label; add +1 to your new mask's Label", # Janus
      "drives": "Take drives from the Beacon's playbook", # Janus
      "sanctuary": "Take a Sanctiary from the Doomed playbook" # Legacy
      "powers": "Unlock the remaining two powers of your suite" # Legacy,
      "flares": "Unlock three new flares", # Nova
      "heart": "Take The Bull's Heart from the Bull playbook" # Nova
      "abilities": "Choose two new abilities from any playbook as you come into your own", # Outsider
      "identity": "You adopt a human life, take Secret Identity and The Mask from the Janus playbook" # Outsider
      "mentorLabel": "Add +2 to the Label your mentor embodies or denies", # Protege
      "resources": "Choose up to four more resources from your mentor" # Protege
      "doom": "Take a doom, doomtrack, and doomsigns from the Doomed playbook" # Transformed
      "mutate": "Mutate further and reveal another two new abilities (chosen from any playbook)" # Transformed
    },
    "doomed": {
      "doomBringers": {
        "overexerting": "overexerting yourself",
        "innocents": "injuring innocents",
        "alone": "facing danger alone",
        "loved": "frightening loved ones",
        "mercy": "showing mercy",
        "openly": "talking about it openly"
      },
      "doomsigns": {
        "titles": {
          "visions": "Dark Visions",
          "infinite": "Infinite Powers",
          "portal": "Portal",
          "bright": "Burning Bright",
          "bolstered": "Bolstered",
          "perish": ""
        },
        "descriptions": {
          "visions": "Mark your doom track to have a vision about the situation at hand. After the vision, ask the GM a question; they will answer it honestly.",
          "infinite": "Mark your doom track to use an ability from any playbook, one time.",
          "portal": "Mark your doom track to appear in a scene with anyone you want.",
          "bright": "Mark your doom track to ignore one of the GM's stated requirements when you call upon the resources of your sanctuary.",
          "bolstered": "Mark your doom track to use an Adult Move one time.",
          "perish": "Your doom arrives; confront it and perish."
        },
        "sanctuary": {
          "features": {
            "assistant": "an aide or assistant",
            "traps": "locks and traps",
            "tomes": "a library full of valuable tomes",
            "relics": "a scattering of ancient relics",
            "teleportal": "a teleportal",
            "containment": "a containment system",
            "computer": "a powerful computer",
            "tools": "useful tools",
            "meditation": "a meditation space",
            "battery": "a power battery",
            "enhancement": "a power enhancement system",
            "healing": "healing equipment",
            "art": "art, music and food"
          },
          "downsides": {
            "access": "difficult to access",
            "attention": "draws dangerous attention",
            "location": "location known to many",
            "damaged": "easily damaged or tampered with",
            "tied": "tied intricately to your doom"
          },
          "conditions": {
            "first": "First, you must ______________",
            "help": "You'll need help from _____________",
            "danger": "You and your team will rist danger from ____________",
            "lesser": "The best you can do is a lesser version, unreliable and limited",
            "doom": "You'll need to mark one box on your doom track",
            "obtain": "You'll have to obtain ______________"
          }
        }
      }
    },
    "janus": {
      "jobs": {
        "barista": "barista",
        "intern": "intern",
        "host": "host/ess",
        "sales": "salesperson",
        "delivery": "delivery person",
        "fastfood": "fast-food worker",
        "babysitter": "babysitter",
        "dishwasher": "dishwasher",
        "tech": "tech support",
        "waiter": "waitress/er"
      },
      "school": {
        "schoolwork": "schoolwork",
        "athletic": "athletic team",
        "chess": "chess club",
        "photography": "photography club",
        "government": "student government"
      },
      "home": {
        "caring": "caring for someone",
        "chores": "household chores",
        "bills": "paying bills",
        "parenting": "surrogate parenting"
      },
      "social": {
        "significant": "significant other",
        "friend": "best frient",
        "popularity": "popularity",
        "relative": "close relative",
        "teacher": "coach/teacher"
      }
    },
    "legacy": {
      "active": "is still active and prominent in the city.",
      "retired": "is retired and quite judgemental.",
      "possible": "is the next possible member of your legacy",
      "opponent": "is the greatest opponent of your legacy ever faced... and is still at large."
    }
    "nova": {
      "names": {
        "storm": "Reality storm",
        "shield": "Shielding",
        "constructs": "Constructs",
        "moat": "Moat",
        "worship": "Worship",
        "move": "Move",
        "boost": "Boost",
        "overcharge": "Overcharge",
        "elemental": "Elemental awareness",
        "snatch": "Snatch"
      },
      "descriptions": {
        "storm": "You channel a destructive burst with your powers. Spend 1 burn to directly engage a threat using your powers, rolling + Freak instead of + Danger. If you do, you will cause unwanted collateral damage unless you spend another burn.",
        "shield": "You call up a fast protective field to stop a danger. Spend 1 burn to defend someone else from an immediate threat, rolling + Freak instead of + Savior.",
        "constructs": "Spend 1 burn to create any object with your powers, up to the size of a person. Spend an additional burn to animate it independently of yourself. The construct dissolves at the end of the scene.",
        "moat": "Spend 1 burn to create a barrier that will hold back threats as long as you keep your atention on it. The GM may call for you to spend another burn if the barrier is threatened by particularly powerful enemies.",
        "worship": "You put a tremendous display of your might. Spend 1 burn to awe an audience into silence, respect and attention when you unleash your powers.",
        "move": "Spend 1 burn to move to any place you choose within the scene, breaking trough or slipping any barriers or restraints in your way. Spend a second burn to move to any place you've previously been.",
        "boost": "Spend 1 burn to supercharge a teammate's efforts with your powers, giving them a +1 bonus to their rols as if you had spent Team from the pool.",
        "overcharge": "You channel the full capacity of your increible powers to overcome an obstacle, reshape your enviroment, or extend your senses. Spend 2 burn to take a 10+ when you unleash your powers.",
        "elemental": "Spend 1 burn and mark a condition to open your mind up to the world around you with your powers. You can ask any one question about the world around you, and the GM will answer honestly.",
        "snatch": "Spend 1 burn to use your powers to seize any one object up to the size of a person from someone within view."
      }
    },
    "protege": {
      {
      "base": "a hidden base",
      "vehicle": "a vehicle",
      "supercomputer": "a supercomputer",
      "communicators": "communicators",
      "surveillance": "surveillance equipment",
      "identities": "false identities",
      "badges": "badges of authority",
      "chem": "a chem lab",
      "med": "a med lab"
      "teleportal": "a teleportal",
      "weapon": "a weapon of last resport",
      "security": "security systems",
      "robots": "simple robots"
    }
  }
}

es = {
  "embed_commands": {
    "mdlv": "mot",
    "libretos": "playbooks"
  },
  "plain_commands": {
    "ayudaaqui": "helphere",
    "bloquear": "lock",
    "editaretiquetas": "editlabels",
    "potencial": "potential",
    "marcarpotencial": "markcondition",
    "borrarcondicion": "clearcondition",
    "crear": "create",
    "config": "settings",
    "cambiarconfig": "change_settings",
    "lenguaje": "language",
    "nombreequipo": "teamname",
    "editarleng": "update_lang",
    "editargm": "update_gm",
    "editarnombre": "update_teamname",
    "crearconfig": "create_settings"
  },
  "dice_rolling": {
    "calculation_title": "Cálculo",
    "calculation": lambda result1, result2, mod, calc: f"Dados **{result1}** + **{result2}**, Etiqueta{mod} **{calc}**",
    "result": "Resultado"
  },
  "description": "Descripción",
  "moves": {
    "moves": "movimientos",
    "movimientos": "moves",
    "adult": "adultos",
    "non_existent_playbook_intro": "Perdón, no pude encontrar ese libreto, los libretos disponibles son:",
    "non_existent_playbook_end": "\nEscribí un signo de exclamación y uno de los libretos en minúscula y sin el 'El', movimientos o adultos\np.ej.: !beacon, !movimientos, !adultos",
    "moves_plus": {
      "response_header": "**Nombre - descripción, accesor, etiqueta**\n"
    }
  },
  "playbook_interactions": {
    "fail_preffix": "Oh no, ",
    "already_locked": lambda label_name: f"Oh no, {label_name} ya está bloqueada!",
    "is_locked": lambda label_name: f"Oh no, {label_name} está bloqueada, no puede ser alterada!",
    "labels_base": "Tus etiquetas son:\n",
    "up": "subir",
    "down": "bajar",
    "value_is_in_border": lambda value, label_name, direction: f"Oh no, con un valor de {value}, tu {label_name} no puede {direction}! Marcá una condición!",
    "locked": "[BLOQUEADA]",
    "condition_not_marked": "Esa condición no está marcada",
    "youre": "Estás:\n",
    "dont": " no",
    "condition_status": lambda status: f"Oh,{status} tenés have that condition marked.",
    "no_character": "Lo siento, pero parece que no tenés ningún personaje creado",
    "existing_character": "Lo siento, pero parece que ya tenés ningún personaje creado",
    "invalid_condition": lambda condition_name: f"Oh no, {condition_name} no es una condición válida",
    "different_labels": "Las etiquedas deben ser diferentes",
    "congrats_pending_advancements": lambda adv_count: f"Genial, ahora podés hacer {adv_count + 1} avances",
    "congrats_potential": lambda potential: f"Genial, tenés {potential + 1} potencial marcado",
    "no_template": lambda playbook_name: f"Parece ser que no tengo una plantilla para un libreto llamado {playbook_name}",
    "congrats_on_creation": lambda char, playbook: f"Felicidades {char}, {playbook} por unirte al equipo!",
    "potential": lambda potential: f"Tenés {potential} potencial marcado",
    "pending_advancements": lambda adv_count: f"Podés hacer {adv_count} avances"
  },
  "labels": {
    "danger": "peligro",
    "freak": "fenómeno",
    "superior": "superior",
    "savior": "salvador",
    "mundane": "mundano"
  },
  "inverted_labels": {
    "peligro": "danger",
    "fenomeno": "freak",
    "superior": "superior",
    "salvador": "savior",
    "mundano": "mundane"
  },
  "conditions": {
    "afraid": "asustado",
    "angry": "enojado",
    "guilty": "culpable",
    "hopeless": "desesperanzado",
    "insecure": "inseguro"
  },
  "inverted_conditions": {
    "asustado": "afraid",
    "enojado": "angry",
    "culpable": "guilty",
    "desesperanzado": "hopeless",
    "inseguro": "insecure"
  },
  "playbooks": {
    "the": "",
    "list": ['emblema', 'toro', 'delincuente', 'condenado', 'jano', 'legado', 'nova', 'extranjero', 'protegido', 'transformado'],
    "playbooks": "Libretos",
    "available": "Los Libretos disponibles son - ",
    "playbook_re": r"!mdlv ([a-z]+)",
    "moment_of_truth": "MOMENTO DE LA VERDAD",
    "this_is_mot": lambda usr: f"Este es el momento de la verdad de {usr}!"
  },
  "configuration": {
    "settings": "Configuración\n",
    "language": "Lenguaje",
    "teamname": "Nombre de equipo",
    "customNames": "Nombres customizados",
    "no_file": "Este chat no tiene archivo de configuración. Para crearlo escribí el siguiente comando:\n!aventura es\nsi querés que esté en español.\n",
    "existing_settings": "Este chat ya tiene archivo de configuración.",
    "successfull_update": "El cambio se hizo con éxito",
    "successfull_creation": "El archivo de configuración ha sido creado"
  }
}


lang_dicts = {
  "en": en,
  "es": es
}


def get_for_all_langs(accessor):
    response = ''

    for lang in lang_dicts:
        response = response + get_translation(lang, accessor)

    return response


def get_translation(lang, accessor):
    key_list = accessor.split('.')
    partial_result = lang_dicts[lang]

    for key in key_list:
        if key not in partial_result:
            return None

        partial_result = partial_result[key]

    return partial_result