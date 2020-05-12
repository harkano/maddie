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
  },
  "playbooks": {
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
      "mutate": "Mutate further and reveal another two new abilities (chosen from any playbook)"
    },
    "beacon": {
      "drivesDescription": "Elige cuatro impulsos para marcar al comienzo del juego. Cuando cumplas con un impulso marcado, tachalo y elegí una:\nMarcar potencial, eliminar una condición, tomar Influencia sobre alguien involucrado\nCuando los cuatro impulsos marcados estén tachados, elegí y marcá cuatro impulsos nuevos.\nCuando se hayan tachado todos los impulsos, cambiá de libreto, retirate de la vida de superhéroe o convertite en un parangón de la ciudad."
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
    }
    "nova": {
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
    }
  }
}


def get_es_dict():
    return es