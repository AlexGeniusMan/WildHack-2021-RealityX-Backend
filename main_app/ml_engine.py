import re
import logging
import numpy as np
import pandas as pd
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

# Объект орфографа русского языка
spell = Speller('ru')

query_popularity = pd.read_csv('main_app/query_popularity.csv')
data_most_common = np.char.lower(np.array(query_popularity['query'], dtype=np.str_))


def change_layout(query):
    """
    Изменение раскладки с английских символов на русские и с русских на английские
    :param query: поисковый запрос (str)
    :return: поисковый запрос с измененной раскладкой на русский язык и на английский язык в виде кортежа (tuple(str))
    """
    return query.translate(layout_en_ru), query.translate(layout_ru_en)


def correct_query_autocorrect(query):
    """
    Исправление опечаток запроса на русском языке
    :param query: поисковый запрос (str)
    :return: исправленный запрос (str)
    """
    return spell(query)


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
        pass
    else:
        # Анонимный пользователь
        logger.debug('Начинается поиск подсказок анонимному пользователю')
        # проверяем раскладку только на русском языке
        clear_query = correct_query_autocorrect(change_layout(query)[0])
        re_query = clear_query.replace(r'\s', r'\\\s')
        for string in data_most_common:
            result_one_string = re.findall(re_query, string)
            if result_one_string != list():
                result.append(string)
        logger.info(f'Найдено подсказок: {len(result)}')
    return result[:n_query]
