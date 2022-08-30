import os
import json
from bot_config import LANG

TEXTS = None

def get_text(key):
    global TEXTS
    return TEXTS.get(key)

def init_texts():
    """
    Loads the texts from the texts json file
    """
    global TEXTS
    # check if texts file exists
    texts_path = f'texts/{LANG}.json'
    if not os.path.exists(texts_path):
        texts_path = 'texts/en-US.json'  # default language
    with open(texts_path, encoding='utf-8') as texts:
        TEXTS = json.load(texts)