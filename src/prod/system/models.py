from datetime import datetime
from typing import Annotated
from sqlalchemy import (
    UniqueConstraint,
    func,
    DateTime,
    Text,
    Boolean,
    Numeric,
    sql,
    ForeignKey, Integer,
)

from sqlalchemy.orm import Mapped, mapped_column
from src.prod.system.database import Base, str_3, str_64, engine_sync

""" Этот блок я переношу в разные проекты и логично, чтоб он носил все свое с собой"""


def OrmCreateTable():
    """Создать таблицы в базе данных"""
    Base.metadata.create_all(engine_sync)  # Декларативные


# Кастомные типы данных
int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(DateTime, server_default=func.now()
                                               , comment='Создано')]
updated_at = Annotated[datetime, mapped_column(DateTime, server_default=func.now()
                                               , server_onupdate=func.now()  # Пиши триггер сам =(
                                               , comment='Обновлено')]
is_active = Annotated[bool, mapped_column(Boolean, server_default=sql.true(), nullable=False
                                          , comment='Активно')]
hash_address = Annotated[str_64, mapped_column(comment='хеш сумма адреса строки')]
hash_data = Annotated[str_64, mapped_column(comment='хеш сумма данных строки')]


class InfoDB(Base):
    __tablename__ = 'info_db'
    __table_args__ = (
        UniqueConstraint('hash_address'),
        {
            'comment': 'Список баз данных и информации о них',
        }
    )
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    is_active: Mapped[is_active]
    hash_address: Mapped[hash_address]
    hash_data: Mapped[hash_data | None]
    date_creation: Mapped[datetime | None] = mapped_column(DateTime, comment='База данных. дата создания')
    host: Mapped[str | None] = mapped_column(comment='База данных. хост')
    host_name: Mapped[str | None] = mapped_column(comment='База данных. хост имя')
    port: Mapped[str | None] = mapped_column(comment='База данных. порт')
    database: Mapped[str | None] = mapped_column(comment='База данных. имя')
    stage: Mapped[str | None] = mapped_column(comment='База данных. слой')
    version: Mapped[str | None] = mapped_column(comment='База данных. версия')
    type: Mapped[str | None] = mapped_column(comment='База данных. тип')


class InfoSchema(Base):
    __tablename__ = 'info_schema'
    __table_args__ = (
        UniqueConstraint('hash_address'),
        {
            'comment': 'Список схем баз данных и информации о них'
        }
    )
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    is_active: Mapped[is_active]
    hash_address: Mapped[hash_address]
    hash_data: Mapped[hash_data | None]
    info_db_id: Mapped[int | None] = mapped_column(ForeignKey("info_db.id", ondelete="CASCADE"))
    table_schema: Mapped[str | None] = mapped_column(comment='Схема. имя в базе данных')


class InfoTable(Base):
    __tablename__ = 'info_table'
    __table_args__ = (
        UniqueConstraint('hash_address'),
        {
            'comment': 'Список таблиц баз данных и информации о них'
        }
    )
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    is_active: Mapped[is_active]
    hash_address: Mapped[hash_address]
    hash_data: Mapped[hash_data | None]
    info_schema_id: Mapped[int | None] = mapped_column(ForeignKey("info_schema.id", ondelete="CASCADE"))
    table_name: Mapped[str | None] = mapped_column(comment='Таблица. имя в базе данных')
    table_com: Mapped[str | None] = mapped_column(Text, comment='Таблица. комментарий')
    name: Mapped[str | None] = mapped_column(comment='Таблица. имя на русском')


class InfoColumn(Base):
    __tablename__ = 'info_column'
    __table_args__ = (
        UniqueConstraint('hash_address'),
        {
            'comment': 'Список столбцов в базе данных и информации о них'
        }
    )
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    is_active: Mapped[is_active]
    hash_address: Mapped[hash_address]
    hash_data: Mapped[hash_data | None]
    info_table_id: Mapped[int | None] = mapped_column(ForeignKey("info_table.id", ondelete="CASCADE"))
    ordinal_position: Mapped[int | None] = mapped_column(comment='Столбец. № позиции')
    column_name: Mapped[str | None] = mapped_column(comment='Столбец. дата создания')
    is_nullable: Mapped[str | None] = mapped_column(comment='Столбец. обязательное?')
    data_type: Mapped[str | None] = mapped_column(comment='Столбец. тип данных')
    column_default: Mapped[str | None] = mapped_column(comment='Столбец. значение по умолчанию')
    column_com: Mapped[str | None] = mapped_column(Text, comment='Столбец. комментарий')
