import re
import time
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

query_popularity = pd.read_csv('query_popularity.csv')
data_most_common = np.char.lower(np.array(query_popularity['query'], dtype=np.str_))


def correct_query(query):
    """
    Изменение раскладки с английских символов на русские и с русских на английские
    :param query: поисковый запрос (str)
    :return: поисковый запрос с измененной раскладкой на русский язык и на английский язык в виде кортежа (tuple(str))
    """
    query_split = query.split()
    words_query = {}

    i = 0
    output = np.array([])
    n_output = 0

    for word in query_split:
        words_query[i] = (list(np.unique([word, word.translate(layout_en_ru), (word.translate(layout_ru_en))])))
        n_output += len(words_query[i])
        i += 1

    if i != 1:

        for j in range(1, len(words_query)):
            if j == 1:
                for _ in product(words_query[j - 1], words_query[j]):
                    output = np.append(output, str(_))
            else:
                for _ in product(output, words_query[j]):
                    output = np.append(output, str(_).replace('"', '').replace('\\', ''))

        output = output[-n_output:]
        start_time = time.time()
        for n_varient in range(len(output)):
            output[n_varient] = re.sub("\'|\)|\(|\,", '', output[n_varient])

            output[n_varient] = spell_ru(output[n_varient]).replace(' ', '\s')
            # output[n_varient] = output[n_varient].replace(' ', '\s')
        logger.info(f'Затраченное время на исправление опечаток: {time.time() - start_time}')


    else:

        start_time = time.time()
        for word in words_query[0]:
            output = np.append(output, str(spell_ru(word)))
            # output = np.append(output, str(word))
        logger.info(f'Затраченное время на исправление опечаток: {time.time() - start_time}')

    return '(' + ')|('.join(output) + ')'


def search(status_autorization, query, n_query):
    """
    Выдача поисковых подсказок
    :param status_autorization: статус авторизации пользователя (boolean)
    :param query: запрос пользователя (str)
    :param n_query: количество подсказок в выдаче (int)
    :return: выдача подсказок (list(str))
    """

    result = []

    if status_autorization:
        # Авторизированный пользователь
        logger.debug(f'Начинается поиск подсказок авторизированного пользователя')
        # проверяем раскладку только на русском языке
        start_time2 = time.time()
        reg = re.compile('[^\|a-zа-я0-9\\\s\^]')
        re_query = reg.sub('', correct_query(query))
        logger.info(f'Затраченное время на обработку запроса: {time.time()-start_time2}')
        start_time3 = time.time()
        for string in data_most_common:
            result_one_string = re.findall(re_query, string, flags=re.IGNORECASE)
            if result_one_string != list():
                result.append(string)
        logger.info(f'Найдено подсказок: {len(result)}')
        logger.info(f'Затраченное время на поиск подсказок: {time.time()-start_time3}')
    else:
        # Анонимный пользователь
        logger.debug('Начинается поиск подсказок анонимному пользователю')
        # проверяем раскладку только на русском языке
        start_time2 = time.time()
        reg = re.compile('[^\|a-zа-я0-9\\\s\^]')
        re_query = reg.sub('', correct_query(query))
        logger.info(f'Затраченное время на обработку запроса: {time.time()-start_time2}')
        start_time3 = time.time()
        for string in data_most_common:
            result_one_string = re.findall(re_query, string, flags=re.IGNORECASE)
            if result_one_string != list():
                result.append(string)
        logger.info(f'Найдено подсказок: {len(result)}')
        logger.info(f'Затраченное время на поиск подсказок: {time.time()-start_time3}')
    return result[:n_query]
