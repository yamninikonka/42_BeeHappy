

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
        # --- Get rows from each table
        cursor.execute(f"""
            SELECT COUNT(*) FROM {table_name};
        """)
        rows=cursor.fetchall()
        if len(rows)>0:
            Logger.info(f"{table_name}, Total Rows: {rows[0]}")
            print(f"{table_name}, Total Rows: {rows[0]}")
        else:
            Logger.info(f"{table_name}, Total Rows: 0")
            print(f"{table_name}, Total Rows: 0")

        # --- Get last row from each table
        # Note: For beehives_sensornodes, we use time_of_entry instead of time_of_save
        if table_name!="beehives_sensornodes":
            cursor.execute(f"""
                SELECT * FROM {table_name}
                ORDER BY time_of_save DESC
                LIMIT 1;""")
        else:
            cursor.execute(f"""
                SELECT * FROM {table_name}
                ORDER BY time_of_entry DESC
                LIMIT 1;""")
        last_row=cursor.fetchall()
        if last_row:
            Logger.info(f"Last row: {last_row[0]}")
            print(f"Last row: {last_row[0]}\n")
        else:
            Logger.error(f"No rows found in {table_name}.")
            print(f"Error: No rows found in {table_name}.\n")

        
