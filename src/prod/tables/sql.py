sql_information_schema_columns = """
SELECT
      inet_server_addr() as inet_server_addr, table_catalog
    , table_schema, table_name, column_name, ordinal_position, column_default, is_nullable, data_type
    , character_maximum_length, character_octet_length, numeric_precision, numeric_precision_radix, numeric_scale
    , datetime_precision, interval_type, interval_precision, character_set_catalog, character_set_schema
    , character_set_name, collation_catalog, collation_schema, collation_name, domain_catalog, domain_schema
    , domain_name, udt_catalog, udt_schema, udt_name, scope_catalog, scope_schema, scope_name, maximum_cardinality
    , dtd_identifier, is_self_referencing, is_identity, identity_generation, identity_start, identity_increment
    , identity_maximum, identity_minimum, identity_cycle, is_generated, generation_expression, is_updatable
    , obj_description((table_schema||'.'||table_name)::regclass::oid)                   as table_com
    , col_description((table_schema||'.'||table_name)::regclass::oid, ordinal_position) as column_com
FROM 
    information_schema.columns WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
    """
sql_pg_class = """
SELECT
   tab_4.table_catalog as main_table_catalog
  ,tab_4.table_schema  as main_table_schema
  ,tab_4.table_name    as main_table_name
  ,tab_4.column_name   as main_column_name
    ,tab_3.table_catalog as sub_table_catalog
    ,tab_3.table_schema  as sub_table_schema
    ,tab_3.table_name    as sub_table_name
    ,tab_3.column_name   as sub_column_name
FROM pg_constraint as c
    left join pg_class as                tab_1 on tab_1.oid = c.conrelid
    left join pg_class as                tab_2 on tab_2.oid = c.confrelid
    left join information_schema.columns tab_3 on tab_3.table_name = tab_1.relname and c.conkey[1] = tab_3.ordinal_position
    left join information_schema.columns tab_4 on tab_4.table_name = tab_2.relname and c.confkey[1] = tab_4.ordinal_position
WHERE c.contype = 'f'
     """
