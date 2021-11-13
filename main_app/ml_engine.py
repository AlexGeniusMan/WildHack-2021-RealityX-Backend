import re
import logging
import numpy as np
import pandas as pd
from itertools import product
from autocorrect import Speller

# Создаем логгер с уровнем логгирования DEBUG
logger = logging.getLogger('search_engine')
logger.setLevel(logging.DEBUG)

# Создаем Хэндлер консоли
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

# Определеяем свой формат вывода сообщений
formatter = logging.Formatter('[%(asctime)s | %(levelname)s]: %(message)s', "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)

# Добавляем хэндлер к логгеру
logger.addHandler(handler)

# Словарь для перевода английской раскладки на русскую
layout_en_ru = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                                 'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
                        "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                        'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))

# Словарь для перевода русской раскладки на английскую
layout_ru_en = dict(zip(map(ord, "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                                 'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'),
                        "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                        'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'))

# Объект орфографа русского и английского языка
spell_en = Speller('en')
spell_ru = Speller('ru')

query_popularity = pd.read_csv('main_app/query_popularity.csv')
data_most_common = np.char.lower(np.array(query_popularity['query'], dtype=np.str_))

import re


def change_layout(query):
    """
    Изменение раскладки с английских символов на русские и с русских на английские
    :param query: поисковый запрос (str)
    :return: поисковый запрос с измененной раскладкой на русский язык и на английский язык в виде кортежа (tuple(str))
    """
    reg = re.compile("\'|\)|\(|\,")

    query_split = query.split()
    words_query = {}

    i = 0
    result = []
    output = []
    n_output = 1

    for word in query_split:
        words_query[i] = (list(np.unique([word, word.translate(layout_en_ru), (word.translate(layout_ru_en))])))
        i += 1

    for word in words_query.values():
        n_output *= len(word)

    if i != 1:

        for j in range(1, len(words_query)):
            if j == 1:
                for _ in product(words_query[j - 1], words_query[j]):
                    output.append(_)
            else:
                for _ in product(output, words_query[j]):
                    output.append(_)

        for n_varient in range(len(output)):
            output[n_varient] = re.sub("\'|\)|\(|\,", '', str(output[n_varient])).replace(' ', '\s')

        return output[-n_output:]

    else:

        return words_query[0]


def correct_query_autocorrect(queries):
    """
    Исправление опечаток запроса на русском языке
    :param query: поисковый запрос (str)
    :return: исправленный запрос (str)
    """
    result = []
    for query in queries:
        result.append(spell_en(query))
        result.append(spell_ru(query))
    result = np.unique(np.array(result, dtype=np.str_))
    result = '^' + '|'.join(result)
    return result


def search(status_autorization, query, n_query):
    """
    Выдача поисковых подсказок
    :param status_autorization: статус авторизации пользователя (boolean)
    :param query: запрос пользователя (str)
    :param n_query: количество подсказок в выдаче (int)
    :return: выдача подсказок (list(str))
    """

    result = []
    query = query.lower()

    if status_autorization:
        # Авторизированный пользователь
        logger.debug(f'Начинается поиск подсказок авторизированного пользователя')
        # проверяем раскладку только на русском языке
        re_query = correct_query_autocorrect(change_layout(query))
        for string in data_most_common:
            result_one_string = re.findall(re_query, string, flags=re.IGNORECASE)
            if result_one_string != list():
                result.append(string)
        logger.info(f'Найдено подсказок: {len(result)}')
    else:
        # Анонимный пользователь
        logger.debug('Начинается поиск подсказок анонимному пользователю')
        # проверяем раскладку только на русском языке
        re_query = correct_query_autocorrect(change_layout(query))
        for string in data_most_common:
            result_one_string = re.findall(re_query, string, flags=re.IGNORECASE)
            if result_one_string != list():
                result.append(string)
        logger.info(f'Найдено подсказок: {len(result)}')
    return result[:n_query]
