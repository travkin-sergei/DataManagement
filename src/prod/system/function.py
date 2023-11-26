import hashlib
import psycopg2
from psycopg2 import Error

from psycopg2.extras import DictCursor


def calculate_hash_sum(list: list):
    """
    Требуется для расчета hash_address и hash_data. Алгоритм sha256
    :param list: list
    :return: list
    """
    list_str = [str(i) for i in list]
    list_union = '+'.join(list_str)
    ha256 = hashlib.sha256(list_union.encode()).hexdigest()
    return ha256


def get_request_data_all(sql, dsn):
    """
    Получение данные в которые не использовались (ошибки исключаются из выборки)
    :param version:
    :return:
    """
    conn = psycopg2.connect(dsn=dsn)
    cursor = conn.cursor(cursor_factory=DictCursor)  # позволяет обращаться как по индексу, так и по имени
    try:
        cursor.execute(sql)
        record = cursor.fetchall()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        record = 'except: ' + str(error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")
    return record
