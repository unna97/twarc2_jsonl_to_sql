import psycopg2
import pandas as pd
import numpy as np
import os
import sqlalchemy as sa

### data stored on local system path
base_folder = "D:\Misogynistic"
curr_task = "Search"
folder_path = base_folder + "\\" + curr_task
files = os.listdir(folder_path)


def fetch_search_type_data(chunk):
    raise NotImplementedError


def fetch_follower_type_data(chunk):
    raise NotImplementedError


def fetch_following_type_data(chunk):
    raise NotImplementedError


task = {
    "Search": fetch_search_type_data,
    "followers": fetch_follower_type_data,
    "following": fetch_following_type_data,
}

### Connect to the database
database_config = {
    "user": "postgres",
    "password": "unnati",
    "host": "localhost",
    "port": "5432",
    "database": "misogynistic_tweets",  ## database you want to store data in
}
conn_str = "postgresql+psycopg2://postgres:unnati@localhost/misogynistic_tweets"

engine = sa.create_engine(conn_str, pool_pre_ping=True)


def insert_dataframe_into_table(df: pd.DataFrame, table_name: str) -> int:

    """
    Inserts a dataframe into a table in the database.If the table already exists, it will be appended.

    Parameters
    ----------
    df: dataframe
    A pandas dataframe to be inserted into the database.

    table_name: str
    The name of the table to insert the dataframe into.

    Returns
    -------
    n: int
    The number of rows inserted into the database.

    """
    if len(df) == 0:
        print("no data to insert:", table_name)
        return 0
    n = df.to_sql(name=table_name, con=engine, if_exists="append", index=False, method='multi')
    return n


def delete_specified_table(table_name: str) -> None:

    """
    Deletes a table from the database.

    Parameters
    ----------
    table_name: str
    The name of the table to delete.

    """
    #if input("are you sure you want to delete table: " + table_name) == "yes":
    engine.execute("DROP TABLE " + table_name)
    print("table deleted:", table_name)
    return


def get_tables_in_database():
    """
    Returns a list of tables in the database.
    """
    return engine.table_names()


def read_jsonl_file_and_process_save_it(type_command: int, file_name: str) -> None:

    """
    Reads a jsonl file and processes it.

    Parameters
    ----------
    type_command: str
    The type of command run to fetch the file

    file_name: str
    The name of the file to be read.

    """
    reader = pd.read_json(folder_path + "\\" + file_name, lines=True, chunksize=20)
    for chunk in reader:
        task[type_command](chunk)
    return
