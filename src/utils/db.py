

import pandas as pd

from __init__ import Logger


def print_dbTables_Columns(cursor):
    # ----- @Perplexity -----
    # cursor.execute("""
    # DROP TABLE IF EXISTS names CASCADE;
    # """)
    # Get all table names in the public schema
    cursor.execute("""
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public';
    """)
    tables = cursor.fetchall()

    for (table_name,) in tables:
        print(f"Table: {table_name}")
        # Get column names for each table
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s;
        """, (table_name,))
        columns = cursor.fetchall()
        for (column_name,) in columns:
            print(f"    Column: {column_name}")
        print()


def print_dbTables_Values(cursor):
    cursor.execute("""
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public';
    """)
    tables = cursor.fetchall()

    for (table_name,) in tables:
        print(f"Table: {table_name}")
        # Get column names for each table
        cursor.execute(f"""
            SELECT * FROM {table_name};
        """)
        df=pd.DataFrame(columns=[des[0] for des in cursor.description],
                        data=cursor.fetchall())
        print(df)
        print()

def print_dbTables_totalRows(cursor):
    cursor.execute("""
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public';
    """)
    tables = cursor.fetchall()

    for (table_name,) in tables:
        # Get rows from each table
        cursor.execute(f"""
            SELECT COUNT(*) FROM {table_name};
        """)
        rows=cursor.fetchall()
        if rows:
            Logger.info(f"{table_name}, total Rows: {rows[0]}\n")
            print(f"{table_name}, total Rows: {rows[0]}\n")
        else:
            Logger.info(f"{table_name}, total Rows: 0\n")
            print(f"{table_name}, total Rows: 0\n")
