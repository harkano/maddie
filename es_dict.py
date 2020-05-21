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
    "marcarcondicion": "markcondition",
    "borrarcondicion": "clearcondition",
    "crear": "create",
    "config": "settings",
    "cambiarconfig": "change_settings",
    "lenguaje": "language",
    "nombreequipo": "teamname",
    "editarleng": "update_lang",
    "editargm": "update_gm",
    "editarnombre": "update_teamname",
    "crearconfig": "create_settings",
    "etiquetas": "labels",
    "condiciones": "conditions",
    "ver_potencial": "get_potential",
    "avances_pendientes": "pending_advancements",
    "avances": "advancements",
    "mov_mi_libreto": "mov_my_playbook",
    "mov_otro_libreto": "mov_other_playbook",
    "reorganizar": "rearrange",
    "mas_roles": "more_roles",
    "mov_adulto": "add_adult",
    "mas_a_etiquetas": "more_to_labels",
    "borrar_signo": "clear_sign",
    "obtener_burns": "get_burns",
    "etiqueta_mascara": "mask_label",
    "obtener_impulsos": "get_drives",
    "obtener_santuario": "get_sanctuary"
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
    "condition_status": lambda status: f"Oh,{status} tenés esa condición marcada.",
    "no_character": "Lo siento, pero parece que no tenés ningún personaje creado",
    "existing_character": "Lo siento, pero parece que ya tenés ningún personaje creado",
    "invalid_condition": lambda condition_name: f"Oh no, {condition_name} no es una condición válida",
    "different_labels": "Las etiquedas deben ser diferentes",
    "congrats_pending_advancements": lambda adv_count: f"Genial, ahora podés hacer {adv_count + 1} avances",
    "congrats_potential": lambda potential: f"Genial, tenés {potential + 1} potencial marcado",
    "no_template": lambda playbook_name: f"Parece ser que no tengo una plantilla para un libreto llamado {playbook_name}",
    "congrats_on_creation": lambda char, playbook: f"Felicidades {char}, {playbook} por unirte al equipo!",
    "potential": lambda potential: f"Tenés {potential} potencial marcado",
    "pending_advancements": lambda adv_count: f"Podés hacer {adv_count} avances",
    "basic": "\nBásicos:",
    "advanced": "\nAvanzados:",
    "taken": "[TOMADO] ",
    "no_moves_pb": "Perdón, pero no hay movimientos de tu libreto que coincidan con ese nombre",
    "no_moves": "Perdón, pero no hay movimientos que coincidan con ese nombre",
    "move_already_taken": "Ya conseguiste este movimiento, elegí otro",
    "successfully_added_move": lambda move_name: f"Genial, ahora podes usar el movimiento {move_name}",
    "your_playbook": "No podés agregar un movimiento de tu libreto con este avance",
    "more": "más",
    "less": "menos",
    "equal": "igual",
    "add_one_to_label": lambda difference, direction: f"Deberías agregarle uno a una de tus etiquetas, la diferencia en este caso da {difference} {direction} que la suma original",
    "less_than_min": lambda min_allowed, intended: f"Lo siento, pero {intended} no es un valor válido para una etiqueta, el mínimo es {min_allowed}",
    "greater_than_max": lambda max_allowed, intended: f"Lo siento, pero {intended} no es un valor válido para una etiqueta, el máximo es {max_allowed}",
    "no_playbook": lambda name: f"Para realizar este avance debes tener el libreto {name}",
    "invalid_roles": "Los roles válidos son: defensor, amigo, confidente y habilitador. A continuación los roles no válidos:",
    "successfull_update": "El cambio se hizo con éxito",
    "role_is_picked": lambda role: f"El rol {role} ya fue elegido, debes elegir dos nuevos",
    "not_adult": lambda name: f"El movimiento {name} no es adulto",
    "already_max": lambda value, name: f"La etiqueta {name} ya tiene el valor máximo ({value})",
    "invalid_label": lambda name: f"La etiqueta {name} no existe. ",
    "invalid_doomsign": lambda doomsign: f"El signo de perdición {doomsign} no existe, los válidos son visiones infinitos, portal, ardor, reforzado y morir",
    "doomsign_not_marked": lambda doomsign: f"El signo de perdición {doomsign} debe estar marcado para poder borrarlo",
    "already_mask_label": lambda label_name: f"La etiqueta {label_name} ya corresponde a tu máscara, debes elegir una diferente",
    "already_have": lambda name: f"Ya tienes {name}"
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
  "configuration": {
    "settings": "Configuración\n",
    "language": "Lenguaje",
    "teamname": "Nombre de equipo",
    "gm": "GM",
    "customNames": "Nombres customizados",
    "no_file": "Este chat no tiene archivo de configuración. Para crearlo escribí el siguiente comando:\n!aventura es\nsi querés que esté en español.\n",
    "existing_settings": "Este chat ya tiene archivo de configuración.",
    "successfull_update": "El cambio se hizo con éxito",
    "successfull_creation": "El archivo de configuración ha sido creado",
    "invalid_lang": lambda lang: f"{lang} no es un idioma válido, las opciones son: es (español), en (inglés)",
    "gm": "GM"
  },
  "playbooks": {
    "the": "",
    "list": ['emblema', 'toro', 'delincuente', 'condenado', 'jano', 'legado', 'nova', 'extranjero', 'protegido', 'transformado', 'brain', ', harbinger', 'innocent', 'joined', 'newborn', 'nomad', 'reformed', 'scion', 'soldier'],
    "names": {
      "emblema": "beacon",
      "toro": "bull",
      "delincuente": "delinquent",
      "condenado": "doomed",
      "jano": "janus",
      "legado": "legacy",
      "nova": "nova",
      "extranjero": "outsider",
      "protegido": "protege",
      "transformado": "transformed",
      "brain": "brain",
      "harbinger": "harbinger",
      "innocent": "innocent",
      "joined": "joined",
      "newborn": "newborn",
      "nomad": "nomad",
      "reformed": "reformed",
      "scion": "scion",
      "soldier": "soldier"
    },
    "inverted_names": {
      "beacon": "emblema",
      "bull": "toro",
      "delinquent": "delincuente",
      "doomed": "condenado",
      "janus": "jano",
      "legacy": "legado",
      "nova": "nova",
      "outsider": "extranjero",
      "protege": "protegido",
      "transformed": "transformado",
      "brain": "brain",
      "harbinger": "harbinger",
      "innocent": "innocent",
      "joined": "joined",
      "newborn": "newborn",
      "nomad": "nomad",
      "reformed": "reformed",
      "scion": "scion",
      "soldier": "soldier"
    },
    "playbooks": "Libretos",
    "available": "Los Libretos disponibles son - ",
    "playbook_re": r"!mdlv ([a-z]+)",
    "moment_of_truth": "MOMENTO DE LA VERDAD",
    "this_is_mot": lambda usr: f"Este es el momento de la verdad de {usr}!",
    "advances": {
      "moveYouPlaybook": "Toma otro movimiento de tu libreto",
      "moveOtherPlaybook": "Toma un movimiento de otro libreto",
      "loseInfluence": "Alguien pierde permanentemente Influencia sobre tí; agrega +1 a una Etiqueta",
      "rearrange": "Reorganiza tus etiquetas como elijas y agrega +1 a una etiqueta",
      "mot": "Desbloquea tu Momento de la Verdad",
      "moreRoles": "Elige otros dos roles para el Corazón del Toro",
      "motAgain": "Desbloquea tu Momento de la Verdad después de que se haya utilizado una vez",
      "playbookChange": "Cambia de libreto",
      "adult": "Toma un movimiento adulto",
      "lock": "Bloquea una etiqueta y agrega +1 a una etiqueta a tu elección",
      "retire": "Retirate de la vida de superhéroe o convertite en un parangón de la ciudad",
      "plusOne": "Añade +1 a dos etiquetas",
      "clear": "Borra una Señal de perdición, pierdes acceso a ese movimiento, por ahora",
      "burns": "Toma Burn y tres bengalas (del libreto de Nova)",
      "confront": "Enfrenta a tu condena en tus términos. Si sobrevives, cambia de libreto",
      "paragon": "Conviértete en un parangón de la ciudad por el tiempo que te",
      "maskLabel": "Cambia la etiqueta de tu máscara, agrega +1 a la nueva etiqueta de tu máscara",
      "drives": "Toma impulsos del libreto del Emblema",
      "sanctuary": "Toma un Santuario del libreto del Condenado",
      "powers": "Desbloquea los dos poderes restantes de tu conjunto",
      "flares": "Desbloquea tres nuevas bengalas",
      "heart": "Toma Coracón de Toro del libreto del Toro",
      "abilities": "Elige dos nuevas nuevas habilidades de cualquier playbook",
      "identity": "Adoptas una vida humana, toma Identidad secreta y La Máscara del libreto del Jano",
      "mentorLabel": "Add +2 to the Label your mentor embodies or denies",
      "resources": "Choose up to four more resources from your mentor",
      "doom": "Take a doom, doomtrack, and doomsigns from the Doomed playbook",
      "mutate": "Mutate further and reveal another two new abilities (chosen from any playbook)",
      "lockLessons": "Bloquea tus aprendizajes y cambia de libreto",
      "mentor": "Elegí un mentor para vos (del libreto Protegido)",
      "pastParagon": "Volvé de vuelta a tu tiempo o convertite en un icono de la ciudad",
      "legacy": "Te volves parte de una larga tradición de superhéroes y tomas un Legado (del libreto Legado)",
      "joinAbilities": "Gana dos nuevas habilidades de otro libreto",
      "advance": "Toma un avance del libreto de tu otra mitad",
      "shame": "Confronta a Tu Vergüenza en tus términos, si sobrevivís, cambia de libreto",
      "enhancement": "Te sometes a mejoras: tomas 2 nuevas habilidades",
      "lockSoldier": "Bloquea Soldado y agrega +1 a una Etiqueta a tu elección",
      "noAegis": "A.E.G.I.S permanentemente pierde Influencia sobre vos, cambia de libreto",
      "civilian": "Retírate de A.E.G.I.S a la vida de civil o unite a las altos mandos de A.E.G.I.S como Director Superior",
      "future": "Volve  al futuro y acepta su nueva forma o viaja a otro punto del pasado para iniciar de nuevo tu misión.",
      "depart": "Partís a parajes desconocidos, para no volver nunca más",
      "mask": "Toma La Máscara y una identidad secreta del libreto Jano"
    },
    "beacon": {
      "drives": "impulsos",
      "drivesDescription": "Elige cuatro impulsos para marcar al comienzo del juego. Cuando cumplas con un impulso marcado, tachalo y elegí una:\nMarcar potencial, eliminar una condición, tomar Influencia sobre alguien involucrado\nCuando los cuatro impulsos marcados estén tachados, elegí y marcá cuatro impulsos nuevos.\nCuando se hayan tachado todos los impulsos, cambiá de libreto, retirate de la vida de superhéroe o convertite en un parangón de la ciudad.",
      "lead": "lidera el equipo exitosamente en la batalla",
      "kissDanger": "besa a alguien peligroso",
      "hitYouShouldnt": "golpea a alguien que probablemente no deberías",
      "helpTeammate": "ayuda a un compañero cuando más te necesita",
      "endThreat": "acaba con una amenaza por tu cuenta",
      "outperform": "logra hacer algo mejor que un héroe adulto",
      "ridiculous": "completa una proeza ridícula",
      "saveTeammateLife": "salva la vida de un compañero de equipo",
      "drunkOrDrug": "emborrachate o drogate con un compañero",
      "drive": "conduce un vehículo fantástico",
      "newSuit": "consigue un nuevo traje",
      "newName": "consigue un nuevo nombre de héroe",
      "gainRespect": "gana el respeto de un héroe al que admiras",
      "kissTeammate": "besate con un compañero de equipo",
      "punchTeammate": "golpea a un compañero de equipo",
      "breakRelation": "rompe una relación con alguien",
      "stopFight": "deten una pelea con palabras tranquilizadoras",
      "trueFeelings": "dile a alguien tus verdaderos sentimientos hacia él/ella",
      "placeOrTime": "viaja a un lugar (o tiempo) increíble",
      "reject": "rechaza a alguien que te dice `no deberías estar aquí`"
    },
    "bull": {
      "rival": "rival",
      "lover": "amor",
      "title": "Corazón del Toro",
      "explanation": "Siempre tienes exatamente un amor y un rival. Puedes cambiar tu amor o rival en cualquier momento; dale al nuevo objeto de tus afectos o desdén Influencia sobre tí. Toma +1 continuado (ongoing) a cualquier acción que impresione a tu amor o frustre a tu rival",
      "description": "Elige un rol que normalmente cumples para tu amor o rival:",
      "roles": {
        "list": ["defensor", "amigo", "confidente", "habilitador"],
        "titles_dict": {
          "defensor": "defender",
          "amigo": "friend",
          "confidente": "listener",
          "habilitador": "enabler"
        },
        "titles": {
          "defender": "Defensor",
          "friend": "Amigo",
          "listener": "Confidente",
          "enabler": "Habilitador"
        },
        "descriptions": {
          "defender": "Cuando saltas para defender a tu amor o rival en batalla, tira +Peligro en lugar de +Salvador para defenderlos.",
          "friend": "Cuando reconfortas o apoyas a tu amor o rival, marca potencial en un éxito. Cuando tu amor o rival te reconforta o apoya, marca potencial cuando ellos obtienen un éxito.",
          "listener": "Cuando atravieses la máscara de tu amor o rival, siempre puedes dejar que te hagan una pregunta para hacerles una pregunta adicional, incluso en un fallo. No es necesario que estas preguntas estén en la lista.",
          "enabler": "Cuando provocas a tu amor o rival, tira +Peligro si estás tratando de provocarlos a tomar acciones precipitadas o poco pensadas."
        }
      }
    },
    "doomed": {
      "nemesis": {
        "title": "Némesis",
        "description": "Tienes un némesis, un enemigo épico y poderoso que representa y encarna tu perdición. Tomará todo lo que tengas poder derrotarlo en el tiempo que te queda.\n¿Quién es tu némesis? ______________________\nAl final de cada sesión, response la pregunta: ¿Has progresado en derotar a tu némesis? Si la respuesta es afirmativa, marca potencial. Si la respuesta es no, marca la grilla de perdición."
      },
      "doomBringers": {
        "title": "Perdición",
        "description": "Estás condenado. Tus poderes pueden estar matándote, o tal vez te persiguen despiadadamente, o quizás tú mismo encarnas el apocalipsis. Pero de una forma u otra, tu futuro es sombrío. ¿Qué cosas te acercan a tu perdición? Elige dos.",
        "track": "Grilla de Perdición:",
        "markExplanation": "Cada vz que tu perdición se acerque, marca una casilla en la grilla de perdición.",
        "fillExplanation": "Cuando la grilla de perdición se llene, elimínala y toma una de sus señales de perdición.",
        "overexerting": "sobreexigirte",
        "innocents": "lastimar a inocentes",
        "alone": "enfrentar peligro solo",
        "loved": "asustar a tus seres queridos",
        "mercy": "mostrar piedad",
        "openly": "hablar abiertamente sobre ello"
      },
      "doomsigns": {
        "title": "Señales de perdición",
        "description": "Estas son habilidades que adquieres a medida que te acercas a tu perdición. Una vez que hayas tomado las cinco Señales de perdición por encima de la línea, debes tomar 'Tu perdición llega' la próxima vez que la grilla de perdición se llene. Elige una señal de perdición inicial durante la creación del personaje.",
        "accessors": {
          "visiones": "visions",
          "infinitos": "infinite",
          "portal": "portal",
          "ardor": "bright",
          "reforzado": "bolstered",
          "morir": "perish"
        },
        "titles": {
          "visions": "Visiones oscuras",
          "infinite": "Poderes infinitos",
          "portal": "Portal",
          "bright": "Ardor resplandeciente",
          "bolstered": "Reforzado",
          "perish": ""
        },
        "descriptions": {
          "visions": "Marca tu grilla de perdición para tener una Visión sobre la situación actual. Después de la visión, hazle al GM una pregunta, te contestará honestamente.",
          "infinite": "Marca tu grilla de perdición para usar una habilidad de cualquier playbook, una vez.",
          "portal": "Marca tu grilla de perdición para aparecer en una escena con quien tu quieras.",
          "bright": "Marca tu grilla de perdición para ignorar uno de los requisitos establecidos por el GM al invocar los recursos de tu santuario.",
          "bolstered": "Marca tu grilla de perdición para usar un movimiento adulto una vez.",
          "perish": "Tu perdición llega. Enfréntala y perece."
        }
      },
        "sanctuary": {
          "title": "Santuario",
          "description": "Tienes un lugar donde puedes descansar, recuperarte y reflexionar sobre tus poderes. Elige y subraya tres características de tu santuario:",
          "callResources": "Cuando recurras a los recursos del santuario para resolver un problema, describe lo que deseas hacer. El GM te dará de una a cuatro condiciones que debes cumplir para completar la solución:",
          "features": {
            "assistant": "un ayudante o asistente",
            "traps": "cerraduras y trampas",
            "tomes": "una biblioteca de tomos valiosos",
            "relics": "diversas reliquias antiguas",
            "teleportal": "un teleportal",
            "containment": "un sistema de contención",
            "computer": "una computadora poderosa",
            "tools": "herramientas útiles",
            "meditation": "un espacio de meditación",
            "battery": "una batería de energía",
            "enhancement": "un sistema amplificador de poderes",
            "healing": "equipo de curación",
            "art": "arte, música y comida"
          },
          "downsides": {
            "access": "de difícil acceso",
            "attention": "atrae una atención peligrosa",
            "location": "ubucación conoida por muchos",
            "damaged": "fácilmente dañada o manipulada",
            "tied": "vinculado intrínsecamente a tu perdición"
          },
          "conditions": {
            "first": "Primero, debes ______________",
            "help": "Necesitarás ayuda de _____________",
            "danger": "Tú y tu equipo correrán peligro de ____________",
            "lesser": "Lo mejor que puedes lograr es una versión menor, poco fiable y limitada",
            "doom": "Deberás marcar una casilla en la grilla de perdición",
            "obtain": "Necesitarás obtener ______________"
          }
        }
    },
    "janus": {
      "title": "Identidad secreta",
      "description": "Tu vida mundana viene con una serie de obligaciones. Elije un total de tres obligaciones:",
      "jobs": {
        "barista": "barista",
        "intern": "interno",
        "host": "camarero/a",
        "sales": "vendedor/a",
        "delivery": "repartidor/a",
        "fastfood": "trabajador de comida rapida",
        "babysitter": "niñero/a",
        "dishwasher": "lavaplatos",
        "tech": "soporte técnico",
        "waiter": "recepcionista"
      },
      "school": {
        "schoolwork": "trabajo escolar",
        "athletic": "equipo de atletismo",
        "chess": "club de ajedrez",
        "photography": "club de fotografía",
        "government": "gobierno estudiantil"
      },
      "home": {
        "caring": "cuidar de alguien",
        "chores": "tareas domésticas",
        "bills": "pagar facturas",
        "parenting": "padrastro/madrastra"
      },
      "social": {
        "significant": "pareja",
        "friend": "mejor amigo/a",
        "popularity": "popularidad",
        "relative": "pariente cercano",
        "teacher": "entrenador/a o maestro/a"
      }
    },
    "legacy": {
      "active": "sigue siendo activo y prominente en la ciudad.",
      "retired": "está retirado y es bastante prejuicioso.",
      "possible": "es el siguiente posible miembro de tu legado.",
      "opponent": "es el mayor oponente al que se ha enfrentado tu legado... y aún está en libertad."
    },
    "nova": {
      "flares": "bengalas",
      "yourFlares": "Tus bengalas son:",
      "names": {
        "storm": "Tormenta de realidad",
        "shield": "Blindaje",
        "constructs": "Constructo",
        "moat": "Foso",
        "worship": "Adoración",
        "move": "Movimiento",
        "boost": "Impulso",
        "overcharge": "Sobrecarga",
        "elemental": "Percepción elemental",
        "snatch": "Arrebato"
      },
      "descriptions": {
        "storm": "Canalizas una explosión destructiva con tus poderes. Gasta 1 Burn para enfrentar directamente una amenaza usando tus poderes, tirando +Fenómeno en lugar de +Peligro. Si lo haces, causarás daño colateral no deseado a menos que gastes otro Burn.",
        "shield": "Conjuras rápidamente un campo de protección para detener un peligro. Gasta 1 Burn para defender a alguien de una amenaza inmediata, tirando +Fenómeno en lugar de +Salvador.",
        "constructs": "Gasta 1 Burn para crear cualquier objeto con tus poderes, hasta el tamaño de una persona. Gasta un Burn adicional para animarla independientemente de ti. El constructo se disuelve al final de la escena.",
        "moat": "Gasta 1 Burn para crear una barrera que retenga las amenazas siempre y cuando mantengas tu atención en ella. El GM puede pedirte que gastes otro Burn si la barera está amenazada por enemigos particularmente poderosos.",
        "worship": "Exhibes una gran demostración de tu poder. Gasta 1 Burn para asombrar a una audiencia y dejarla en silencio, respeto y atención cuando liberes tus poderes.",
        "move": "Gasta 1 Burn para moverte a cualquier lugar que elijas dentro de la escena, rompiendo o deslizándote por cualquier barrera o restricción que encuentres en tu camino. Gasta un segundo Burn para moverte a cualquier lugar que hayas estado anteriormente.",
        "boost": "Gasta 1 Burn para potenciar los esfuerzos de un compañero con tus poderes, dándole una bonificación de +1 a su tirada como msi hubieras gastado TP del pozo.",
        "overcharge": "Canaliza toda la capacidad de tus increíbles poderes para superar un obstáculo, remodelar tu entorno o ampliar tus sentidos. Gasta 2 Burns para ganar un 10+ cuando desates tus poderes.",
        "elemental": "Gasta 1 Burn y marca una condición para abrir tu mente al mundo que te rodea con tus poderes. Puedes hacer cualquier pregunta sobre el mundo que te rodea y el GM responderá con sinceridad.",
        "snatch": "Gasta1 Burn para usar tus poderes para arrebatarle cualquier objeto de hasta el tamaño de una persona a alguien que está a la vista."
      }
    },
    "protege": {
      "mentor": {
        "title": "Mentor",
        "description": "Tienes un mentor, alguien que te enseñó, te entrenó, te dio ayuda o te crió. Alguien que puede haberte confijado de forma demasiado rígida a un solo camino.\n¿Qué etiqueta encarna y cuál niega? (marca uno de cada uno)",
        "embodies": "Encarna",
        "denies": "Niega"
      },
      "resources": {
        "base": "una base oculta",
        "vehicle": "un vehículo",
        "supercomputer": "una supercomputadora",
        "communicators": "comunicadores",
        "surveillance": "equipo de vigilancia",
        "identities": "identidades falsas",
        "badges": "insignias de autoridad",
        "chem": "un laboratorio de química",
        "med": "un laboratorio médico",
        "teleportal": "un teletransportador",
        "weapon": "un arma de último recurso",
        "security": "sistemas de seguridad",
        "robots": "robots simples"
      }
    },
    "reformed": {
      "title": "Amigos en lugares bajos",
      "description": "Tenes vínculos con villanos de tu vida anterior. Elegí tres nombres para completar:",
      "nameExamples": "Finch, Ellen “Diablo” Drummond, Mr. Cane, The Mad Magpie, Dr. Cutler, Armorer, Tegan Queen, Lovelace",
      "choose": "Para cada uno elegí una Especialidad.",
      "speciality": "Especialidad",
      "obligation": "Obligación",
      "specialities": ["armas", "materiales", "artefactos cósmicos", "tecnología alíen", "información interna"],
      "atCreation": "Cuando creas tu personaje marca 2 obligaciones con un villano y marca una obligación en otro."
    },
    "newborn": {
      "title": "Una Hoja en Blanco",
      "description": "Fuiste creado con un entendimiento básico del mundo. Cuando aprendes algo que te ayuda a entender mejor el mundo anota como un aprendizaje. Completa dos al crear tu personaje y completa las otras dos cuando las hayas aprendido durante la partida.",
      "iam": "Yo soy",
      "should": "Un superhéroe debería",
      "always": "Siempre",
      "never": "Nunca"
    },
    "innocent": {
      "title": "Yo del futuro",
      "description": "Tu yo del futuro está ahí fuera, es una figura importante en Ciudad Halcyon y en el resto del mundo (también es todo lo que esperabas nunca ser). Pero enterarte de cómo se volvió quien es puede llevarte a seguir un camino similar. Elegí un paso del camino de tu Yo del Futuro que ya sepas y circúlalo.",
      "lost": "Perdió a alguien que le importaba mucho",
      "failed": "Falló de forma horrible en una causa noble",
      "crime": "Cometió un crimen mayor",
      "betray": "Traicionó a un amigo o aliado cercano",
      "cost": "Consiguió una victoria  a un precio horrible para el mundo que los rodea",
      "kill": "Mató a alguien",
      "battled": "Peleó públicamente contra otro héroe",
      "innocent": "Lastimó a un inocente"
    },
    "star": {
      "title": "Audiencia",
      "description": "Sos una celebridad en la ciudad. Por defecto tu audiencia es un grupo limitado de fans interesados con quienes te comunicas a través de entrevistas luego de la acción y frecuentes conferencias de prensa.",
      "lovesDescription": "¿Por qué tu audiencia te ama? Marca todo lo que aplique",
      "loves": {
        "alike": "Sos como ellos",
        "dangerous": "Sos una persona peligrosa, una mala influencia",
        "noble": "Sos un noble guerrero de la justicia",
        "beautiful": "Sos impresionante, único, bello",
        "charming": "Sos encantador, bien hablado e inteligente",
        "firebrand": "Sos un agitador, mobilizas a la gente"
      },
      "advantagesDescription": "Elegí 2 ventajas:",
      "advantages": {
        "devoted": "Tu audiencia tiene una gran devoción hacia vos",
        "speak": "Podés hablar fácilmente con ellos en cualquier momento",
        "agent": "Tenés un agente de relaciones públicas que maneja a tu audiencia",
        "money": "Ganas mucho dinero por su interés",
        "endorsement": "Tenés el aval de un héroe importante",
        "wider": "Tenés una audiencia muy amplia"
      },
      "demandsDescription": "Elegí 2 demandas de tu audiencia:",
      "demands": {
        "stimulation": "Requieren estimulación constante",
        "perfection": "Requieren perdección, no admiten errores",
        "drama": "Requieren constantes escenas de drama",
        "heroism": "Requieren grandes actos de heroísmo",
        "novelty": "Requieren novedad y acción siempre distinta",
        "chemistry": "Requieren química con tus aliados"
      }
    },
    "joined": {
      "otherHalf": {
        "title": "Tu otra mitad",
        "description": "Compartís un profundo vínculo con tu otra mitad. Son más fuertes juntos que cuando están separados, por ahora. Si tu otra mitad es un Delinquent, Outsider o Transformed, toma dos movimientos de su playbook, uno que hayan elegido y otro que no. Recorda que comparten más que solo movimientos; por ejemplo, si tu otra mitad es Outsider, ambos vienen del mismo planeta/dimensión, etc, Para todos los demás playbooks compartís los extras de base de tu mitad.",
        "beacon": "Toma Impulso y marca cuatro de tu elección. Cuando tu otra mitad tacha un Impulso, también lo tachas.",
        "bull": "Toma el Corazón de Toro con el mismo amor y rival que tu otra mitad. Elegí un diferente rol que cumplís de forma complementaria.",
        "janus": "Toma La  máscara y una identidad secreta. Elegí una Etiqueta distinta para tu mascara. Toma dos obligaciones: una compartida y otra única para vos.",
        "legacy": "Toma un Legado. Tu otra mitad pone tantos nombres en la lista inicial como elija, vos completas el resto. Nunca podes contestar las preguntas del movimiento de Legado de tu otra mitad.",
        "protege": "Compartís un mentor con tu otra mitad. Cuando tu otra mitad define el mentor y los recursos, agrega un recurso adicional.",
        "doomed": "Toma un santuario, una perdición y la grilla de perdición: Vos y tu otra mitad comparten las mismas condiciones que acercan su perdición. Cuando se llena la grilla de perdición, ambos eligen una nueva señal de perdición. Empezas con la señal de perdición que eligió tu otra mitad. Tu otra mitad elige las características y desventajas iniciales del santuario compartido. Vos elegís una más de cada una.",
        "nova": "Toma un santuario, una perdición y la grilla de perdición: Vos y tu otra mitad comparten las mismas condiciones que acercan su perdición. Cuando se llena la grilla de perdición, ambos eligen una nueva señal de perdición. Empezas con la señal de perdición que eligió tu otra mitad. Tu otra mitad elige las características y desventajas iniciales del santuario compartido. Vos elegís una más de cada una."
      },
      "bondsDistinctions": {
        "title": "Vínculos y Distinciones",
        "description": "En la creación de personajes empezas con Únicos, luego elegí otro vinculo. Cuando vos o tu otra mitad bloqueen una etiqueta, tacha uno de tus vínculos elegidos y elegí una distinción.",
        "bonds": {
          "titles": {
            "two": "Únicos",
            "fastball": "Fastball special",
            "activate": "Powers, activate!",
            "eyes": "Four eyes are better"
          },
          "descriptions": {
            "two": "When time passes, ",
            "fastball": "",
            "activate": "When you and your other half",
            "eyes": "Four eyes are better"
          }
        }
      }
    },
    "brain": {
      "title": "Tu Vergüenza",
      "description": "Tenes una profunda y constante sensación de culpa por algo que creaste o diste una mano para crearlo. Puede ser algo que inventaste cuanto te volviste un genio o algo que comenzaste a hacer y que ya no tenes el poder de detener. Incluso puede ser algo que este mas alla de tus habilidades volver a lograr, esta creación única solo puede ser hecha una vez en la vida. Asi como tu inteligencia es de escala mundial, Tu Vergüenza es un problema de escala mundial. Cualquiera sea el caso, tu rol en la creación de esto no es públicamente conocido … por ahora.",
      "is": "¿Qué es tu Vergüenza?",
      "isOptions": ["Un prototipo de Inteligencia Artificial", "Un Fenómeno Cósmico", "Un arma catastrófica", "Un peligroso compuesto químico", "Una monstruosidad viviente", "Un antiguo aliado ahora alterado"]
    },
    "soldier": {
      "title": "Una llamada más alta",
      "description": "Trabajas para una agencia policial metahumana (A.E.G.I.S) que mantiene al mundo a salvo de todo tipo de amenazas superhumanas, sobrenaturales y extraterrestres. Te ofreciste voluntariamente a trabajar con un equipo de jóvenes héroes como parte de un nuevo programa de A.E.G.I.S designado para mantener la ciudad segura.",
      "label": "Tenes una Etiqueta adicional:",
      "labelExplanation": "Soldado funciona como cualquier otra Etiqueta. Los personajes con Influencia sobre vos pueden alterarla y marcas una condición si tuviera que alterarse por sobre +3 o -2. Solo podes cancelar la Influencia de A.E.G.I.S sobre vos usando el avance apropiado. No podes bloquear Soldado con el Momento de la Verdad."
    },
    "harbinger": {
      "monster": "Monstruo",
      "traitor": "Traidor",
      "corruptor": "Corruptor",
      "martyr": "Mártir",
      "builder": "Constructor",
      "leader": "Líder"
    },
    "nomad": {
      "title": "Echando raíces",
      "description": "Estás acá, y a la vez no, y se nota. Con el tiempo vas a poder comprometerte con este lugar y encontrar porque esta gente elige invertir en los demás.\nLos adultos no tienen Influencia sobre vos por defecto. Nadie la tiene. Solo podes dar un total de 6 de Influencia. Durante la partida, solo podes dar Influencia revelando una vulnerabilidad o debilidad a alguien. Podes dar Influencia a través del movimiento de fin de sesión. No podes darle Influencia a alguien que ya tenga sobre vos.\nLos otros no pueden tomar Influencia sobre vos; si fueran a hacerlo, en vez de eso pueden marcar potencial o infligirte una condición, a su elección. Rechazas Influencia con -2 por defecto, en vez de +0. Cuando alguien toma ventaja de la Influencia sobre vos, pueden elegir dos opciones de la lista. Al final de cada sesión, podes tomar de vuelta 1 Influencia de alguien a tu elección.\nSi diste 0-Influencia, no podes reconfortar ni apoyar a nadie. Si fueras a activar ese movimiento, en vez de eso marca una condición mientras decís exactamente la cosa equivocada. Si diste 0-Influencia y alguien intenta reconfortarte o apoyarte a vos, no podes abrirte a ellos.",
      "benefits": "You gain benefits based on how much Influence you have given out. These benefits stack.",
      "oneTwo": "Cuando defendes a alguien que tiene Influencia sobre vos podes ignorar la condición Inseguro. Cuando enfrentas de forma directa a alguien que tiene Influencia sobre vos, podes ignorar la condición Asustado.",
      "three": "Cuando recibís un golpe poderoso de alguien que tiene Influencia sobre vos, toma -2 a la tirada.",
      "four": "Cuando atravesas la máscara de alguien que tiene Influencia sobre vos, podes siempre hacerles una pregunta, incluso en un fallo.",
      "five": "Cuando gastas un Equipo para ayudar a alguien que tiene Influencia sobre vos, le das +2 a la tirada.",
      "six": "Cuando aceptas la palabras de alguien que tiene Influencia sobre vos, marca potencial, remove una condición o toma +1 a la siguiente tirada.ss"
    },
    "scion": {
      "title": "Respeto",
      "description": "Escribí los nombres de al menos otros dos personajes cuyo respeto necesitas ganar para diferenciarte de tu familia. Podes agregar nuevos nombres cuando sea apropiado.",
      "enemy": "El mayor enemigo de tu padre/madre ",
      "victim": "La mayor víctima de tu padre/madre",
      "idol": "Tu ídolo personal",
      "leader": "El líder de la ciudad",
      "hero": "La más grande heroína de la ciudad",
      "celebrity": "El más famoso de la ciudad"
    }
  }
}


def get_es_dict():
    return es