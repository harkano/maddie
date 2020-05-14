from en_dict import get_en_dict
from es_dict import get_es_dict

lang_dicts = {
  "en": get_en_dict(),
  "es": get_es_dict()
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