import psycopg2
import pandas as pd
import numpy as np
import os
import sqlalchemy as sa

### data stored on local system path
base_folder = "D:\Misogynistic"
task = "Search"
folder_path = base_folder + "\\" + task
files = os.listdir(folder_path)

### Connect to the database
database_config = {
    "user": "postgres",
    "password": "unnati",
    "host": "localhost",
    "port": "5432",
    "database": "misogynistic_tweets",  ## databsse you want to store data in
}
conn_str = "postgresql+psycopg2://postgres:unnati@localhost/misogynistic_tweets"

engine = sa.create_engine(conn_str)


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
    n = df.to_sql(name=table_name, con=engine, if_exists="append", index=False)
    return n
