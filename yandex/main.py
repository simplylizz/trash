# coding: utf-8

"""
Есть два списка разной длины. В первом содержатся ключи, а во втором
значения. Напишите функцию, которая создаёт из этих ключей и значений
словарь. Если ключу не хватило значения, в словаре должно быть
значение None. Значения, которым не хватило ключей, нужно
игнорировать.
"""

import itertools


def make_dict(keys, values):
    """Make dict from keys and values lists.

    If values is missing for key then None is setted.

    >>> list_1 = [1, 2, 3]
    >>> list_2 = ['a', 'b']
    >>> make_dict(list_1, list_2)
    {1: 'a', 2: 'b', 3: None}
    >>> make_dict(list_1, list_2 + ['c', 'd'])
    {1: 'a', 2: 'b', 3: 'c'}
    """
    values = values + [None] * (len(keys) - len(values))
    return dict(itertools.izip(keys, values))


# 2 ###

"""
В системе авторизации есть ограничение: логин должен начинаться с
латинской буквы, состоять из латинских букв, цифр, точки и минуса, но
заканчиваться только латинской буквой или цифрой; минимальная длина
логина — один символ, максимальная — 20. Напишите код, проверяющий
соответствие входной строки этому правилу. Придумайте несколько
способов решения задачи и сравните их.
"""

import re
import string


# Not using str.islapha/str.isalphanum because it could return True for
# non-latin symbols.
ALPHA = string.ascii_letters
ALPHANUM = ALPHA + string.digits
# allowed in *body* of login
ALLOWED_SYMBOLS = ALPHANUM + '-.'


def check_login(login):
    """Return True if login passes all checks else False.

    >>> check_login('a')
    True
    >>> check_login('a1')
    True
    >>> check_login('a.1')
    True
    >>> check_login('1a')
    False
    >>> check_login('1')
    False
    >>> check_login('a' * 21)
    False
    >>> check_login('a' * 18 + '.1')
    True
    """
    if not 1 <= len(login) <= 20:
        return False

    # NOTE: Is alpha could return True for non-latin symbols
    if login[0] not in ALPHA or login[-1] not in ALPHANUM:
        return False

    return all(s in ALLOWED_SYMBOLS for s in login)

    # alternative return:
    # re.match(r'^([a-z0-9\.\-])$', login, re.IGNORE_CASE)


def check_login_re(login):
    """Return True if login passes all checks else False.

    >>> check_login_re('a')
    True
    >>> check_login_re('a1')
    True
    >>> check_login_re('a.1')
    True
    >>> check_login_re('1a')
    False
    >>> check_login_re('1')
    False
    >>> check_login_re('a' * 21)
    False
    >>> check_login_re('a' * 18 + '.1')
    True
    """
    # If you have a problem and you want to solve it with regexps than
    # you have two problems.
    return bool(re.match(
        (
            r'^'  # just for symmetry's sake
            r'[a-z]'  # first symbol is alpha
            r'([a-z0-9\-\.]{0,18}'  # then an optional group of allowed symbols
            r'[a-z0-9])?'  # which ends with alphanum (and total length 1-19)
            r'$'  # end of string
        ),
        login,
        re.IGNORECASE,
    ))


# 3 ###

"""
Есть две таблицы — users и messages:

users
UID Name
1. Платон Щукин
2. Лера Страза
3. Георгий Атласов

messages
UID msg
1 – "Привет, Платон!"
3 – "Срочно пришли карту."
3 – "Жду на углу Невского и Тверской."
1 – "Это снова я, пиши чаще"


Напишите SQL-запрос, результатом которого будет таблица из двух
полей: «Имя пользователя» и «Общее количество сообщений».
"""

"""
SELECT users.name, COUNT(*) FROM users, messages
WHERE users.uid = messages.uid GROUP BY users.uid;
"""


# 4 ###

"""
Предположим, у нас есть access.log веб-сервера. Как с помощью
стандартных консольных средств найти десять IP-адресов, от которых
было больше всего запросов? А как сделать это с помощью скрипта на
Python?
"""

"""
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10
"""

import collections


def get_top_visitors():
    """Read access.log and return top 10 visitors.

    Return pairs (<ip>, <num of visits>).
    """

    visitors = collections.Counter()

    with open('access.log', 'r') as access_log:
        for line in access_log:
            visitors[line.split(' ', 1)[0]] += 1

    return visitors.most_common(10)


# 5 ###

"""
Оцените свои знания нижеперечисленных технологий: 0 — не сталкивался,
1 — имею небольшой опыт, 2 — знаю хорошо, 3 — эксперт.
    Python
    С++
    Django или другие Python-фреймворки
    язык SQL, MySQL или другой SQL-сервер
    NoSQL базы данных
    ОС Unix/Linux, стандартные средства shell
    алгоритмы и структуры данных
    JavaScript
    XML/XSLT
    Git, SVN, другие VCS
"""

"""
Python - 2
С++ - 1
Django или другие Python-фреймворки - 2
язык SQL, MySQL или другой SQL-сервер - 1
NoSQL базы данных - 1
ОС Unix/Linux, стандартные средства shell - 1
алгоритмы и структуры данных - 1
JavaScript - 1
XML/XSLT - 1
Git, SVN, другие VCS - 2
"""


# 6 ###

"""
Напишите, какого рода задачи вам хотелось бы решать.
"""

"""
Backend, оптимизация, работа с мессейджингом, nosql, opensource,
хотелось бы получить больше "боевого" опыта high-load, etc.
"""


if __name__ == "__main__":
    import doctest
    doctest.testmod()
