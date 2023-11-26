import pandas as pd
import hashlib

from src.prod.system.function import get_request_data_all, calculate_hash_sum
from src.prod.tables.list_dns import ddd
from src.prod.tables.orm import OrmInfoDB_Insert, OrmInfoSchema_Insert, OrmInfoTable_Insert, OrmInfoColumn_Insert
from src.prod.tables.sql import sql_information_schema_columns

"""
для того чтобы смапить данные вышестоящего блока (база --> схема --> таблица --> колонка) 
необходимо:
    + в нижестоящий добавить хеш сумму.
    + перед загрузкой ее удалить
    + Если использовать хеш сумму как ключ, то можно было бы оставить как есть, но по ходу до этого мы еще не выросли
"""
df_db_insert = pd.DataFrame(
    {"hash_address": [], "hash_data": [], "date_creation": [], "host": [], "host_name": [], "port": [], "database": [],
     "stage": [], "version": [], "type": [], })
df_schema_insert = pd.DataFrame(
    {"hash_address": [], "hash_data": [], "info_db_id": [], "table_schema": [],
     'hash_address_db_insert': []})  # этот столбец для маппинга данных не забыть удалить
df_table_insert = pd.DataFrame(
    {"hash_address": [], "hash_data": [], "info_schema_id": [], "table_name": [], "table_com": [], "name": [],
     'hash_address_schema_insert': []})  # этот столбец для маппинга данных не забыть удалить
df_column_insert = pd.DataFrame(
    {"hash_address": [], "hash_data": [], "info_table_id": [], "ordinal_position": [], "column_name": [],
     "column_default": [], "is_nullable": [], "data_type": [], "column_com": [],
     'hash_address_column_insert': []})  # этот столбец для маппинга данных не забыть удалить

sss = get_request_data_all(sql_information_schema_columns, ddd)

for row in sss:
    address_info_db = [row['inet_server_addr'], row['table_catalog']]
    hash_address_info_db = calculate_hash_sum(address_info_db)

    address_info_table = [row['table_catalog'], row['table_schema'], row['table_name']]
    hash_address_info_table = calculate_hash_sum(address_info_table)

    address_info_column = [row['table_catalog'], row['table_schema'], row['table_name'], row['column_name']]
    hash_address_info_column = calculate_hash_sum(address_info_column)

    column_name = row['column_name']
    ordinal_position = row['ordinal_position']
    column_default = row['column_default']
    is_nullable = row['is_nullable']
    host = row['inet_server_addr']
    table_catalog = row['table_catalog']
    table_schema = row['table_schema']

    hash_address = hash_address_info_column  # пока один на всех общий

    if row['udt_name'] == 'varchar' and row['character_maximum_length'] is not None:
        data_type = (row['udt_name'] + '(' + str(row['character_maximum_length']) + ')')
    else:
        data_type = row['udt_name']

    column_com = row['column_com']

    data_row = ''
    for row_col in row:
        """ Требуется исключить часть столбцов т.к. они определяют абсолютную уникальность, что не требуется """
        data_row = '+'.join(str(row_col))
    hash_data = hashlib.sha256(data_row.encode()).hexdigest()

    # добавление данные в df базы данных
    db_insert = pd.DataFrame([[hash_address_info_db, hash_data, host, table_catalog]],
                             columns=['hash_address', 'hash_data', 'host', 'database'])
    df_db_insert = pd.concat([db_insert, df_db_insert])

    # добавление данные в df схемы базы данных
    address_info_schema = [row['table_catalog'], row['table_schema']]
    hash_address_info_schema = calculate_hash_sum(address_info_schema)
    schema_insert = pd.DataFrame([[hash_address_info_schema, hash_data, table_catalog, table_schema]],
                                 columns=['hash_address', 'hash_data', 'table_catalog', 'table_schema'])
    df_schema_insert = pd.concat([df_schema_insert, schema_insert]).reset_index(drop=True)

    address_info_table = [row['table_catalog'], row['table_schema'], row['table_name']]
    hash_address_info_table = calculate_hash_sum(address_info_table)
    table_name = row['table_name']
    table_com = row['table_com']
    name = row['table_com']

    table_insert = {
        "hash_address": hash_address_info_table,
        "hash_data": hash_data,
        'table_name': table_name,
        'table_com': table_com,
        'name': name,
    }
    # OrmInfoTable_Insert(table_insert)

    column_insert = {
        "hash_address": hash_address,
        "hash_data": hash_data,
        "column_name": column_name,
        "ordinal_position": ordinal_position,
        "column_default": column_default,
        "is_nullable": is_nullable,
        "data_type": data_type,
        "column_com": column_com
    }

    # OrmInfoColumn_Insert(column_insert)

print(df_db_insert.info())
print(df_schema_insert.info())
print(df_table_insert.info())
print(df_column_insert.info())
