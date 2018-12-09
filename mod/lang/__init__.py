from . import cpp

LANG_CODE_MAP = {
    'cpp': cpp
}


def get_lang(lang_code):
    return LANG_CODE_MAP[lang_code.lower()]
