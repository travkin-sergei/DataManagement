from sqlalchemy import insert

from src.prod.system.database import session_sync
from src.prod.system.models import InfoDB, InfoSchema, InfoColumn, InfoTable


def OrmInfoDB_Insert(dictionary):
    """
    Функция для записи в модель InfoColumn
    :param dictionary:
    :return: pk of inserted data
    """
    with session_sync() as session:
        try:
            session.execute(InfoDB.__table__.insert(), dictionary)
            session.commit()
        except:
            print('ошибка')


def OrmInfoSchema_Insert(dictionary):
    """
    Функция для записи в модель InfoSchema
    :param dictionary:
    :return: pk of inserted data
    """
    with session_sync() as session:
        try:
            session.execute(InfoSchema.__table__.insert(), dictionary)
            session.commit()
        except:
            print('ошибка')


def OrmInfoTable_Insert(dictionary):
    """
    Функция для записи в модель InfoTable
    :param dictionary:
    :return: pk of inserted data
    """
    with session_sync() as session:
        try:
            session.execute(InfoTable.__table__.insert(), dictionary)
            session.commit()
        except:
            print('ошибка')


def OrmInfoColumn_Insert(dictionary):
    """
    Функция для записи в модель InfoColumn
    :param dictionary:
    :return: pk of inserted data
    """
    with session_sync() as session:
        try:
            session.execute(InfoColumn.__table__.insert(), dictionary)
            session.commit()
        except:
            print('ошибка')
