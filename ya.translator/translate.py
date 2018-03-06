# coding: utf8

import requests
import sys


TRANSLATE_TIMEOUT = 15

TRANSLATE_URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"

KEY_TRANSLATE = ""


def get_translate_or_none(text, direction, b):
    try:
        response = requests.get(
            TRANSLATE_URL,
            params={'key': KEY_TRANSLATE, 'text': text, 'lang': direction},
            timeout=TRANSLATE_TIMEOUT
        )
        response.raise_for_status()
        result_dict_text = response.json()['text'][0]

        if (result_dict_text != text) and b:
            print('-> ' + result_dict_text + '\n')
            return result_dict_text

        else:
            f = open('data.txt')
            answer = ''
            data = f.readlines()
            f.close()
            for line in data:
                if line.find(text) > -1:
                    answer += '\n' + line
            if answer:
                print("-> возможные варианты из data.txt: \n%s" % answer)
                return answer

        print('None\n')

    except Exception:
        print('None\n')

bool = True
direction = 'en'

def get_direction(text):
    en_letters = set('abcdefghijklmnopqrstuvwxyz')
    text = text.lower()
    if text[0] in en_letters:
        return 'ru'
    else:
        return 'en'

try:
    text = ''
    for i in sys.argv[1:]:
        if i:
            text += i + ' '
        else:
            break
    text = text.strip()
    direction = get_direction(text)
    print()
    get_translate_or_none(text, direction, 1)
    bool = False
except Exception:
    pass

if bool:
    print('\n\t\t===== Я. Переводчик (версия 0.09) =====')

while(bool):
    text = input().strip()
    if text in ['q', 'й']:
        print('\n\t\t=====      Завершение работы      =====\n')
        break
    if text in ['s', 'с']:
        f = open('data.txt', 'a')
        f.write("%s - %s\n" % (tmp, answer))
        f.close()
        print("\n\t\t* text '%s' is successfully saved *\n" % tmp)
        continue
    if text in ['a', 'д']:
        to_add = input().strip()
        f = open('data.txt', 'a')
        f.write("%s\n" % to_add)
        f.close()
        print("\n\t* text '%s' is successfully saved *\n" % to_add)
        continue
    if text == '--':
        answer = get_translate_or_none(tmp, direction, 0)
        tmp = text
        continue
    if text in ['data', 'd', 'дата', 'д']:
        f = open('data.txt')
        print('\n\t\t\t* Содержание data.txt *')
        for numb, line in enumerate(f.readlines()):
            print("%i. %s" % (numb+1, line))
        f.close()
        continue
    if text == 'clear':
        f = open('data.txt', 'w')
        f.close()
        print('\n\t\t\t   * Буфер очищен *\n')
        continue
    direction = get_direction(text)
    answer = get_translate_or_none(text, direction, 1)
    tmp = text
