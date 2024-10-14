import requests
import pandas as pd
import os
from sqlalchemy import create_engine, text as sql_text
from sqlalchemy import MetaData, Table, Column, Integer, String, UniqueConstraint

import logging

def fetch_data(json_path:str) -> pd.DataFrame:
    response = requests.get(json_path)
    if response.ok:
        fetched_dataframe = pd.read_json(response.text) #Returns in json format
        fetched_dataframe = fetched_dataframe[["LocationId", "TotalCapacity", "LocationName", "LastUpdatedDateAndTime", "LastCount", "FacilityId", "IsClosed"]]
        return fetched_dataframe
    else:
        raise(ConnectionError("Unable to fetch data"))

def create_corec_usage_table(sqlite_file:str) -> None:
    conn_string = f"sqlite:///{os.path.realpath(sqlite_file)}"
    engine = create_engine(conn_string)

    # Define the table schema using SQLAlchemy Core
    metadata = MetaData()
    corec_usage = Table(
        'corec_usage', metadata,
        Column('id', Integer, primary_key=True),
        Column('LocationId', Integer),
        Column('TotalCapacity', Integer),
        Column('LocationName', String),
        Column('LastUpdatedDateAndTime', String),
        Column('LastCount', Integer),
        Column('FacilityId', Integer),
        Column('IsClosed', Integer),
        UniqueConstraint('LocationId', 'LastUpdatedDateAndTime', 'FacilityId')
    )
    #corec_usage.create(engine)
    metadata.create_all(engine, tables=[corec_usage])

def ingest_data(df, table_name="corec_usage", sqlite_file="/home/jake/scripts/workshop/corec-usage/corec_usage.db"):
    # Create a connection to the SQLite database
    conn_string = f"sqlite:///{os.path.realpath(sqlite_file)}"

    engine = create_engine(conn_string)
    unique_columns = ["LocationId", "LastUpdatedDateAndTime", "FacilityId"]

    # Read the existing data from the table
    # https://stackoverflow.com/questions/75309237/read-sql-query-throws-optionengine-object-has-no-attribute-execute-with

    query = f"SELECT {', '.join(unique_columns)} FROM {table_name};"
    existing_data = pd.read_sql_query(con=engine.connect(), 
                                  sql=sql_text(query))
    
    # Find the rows in df that don't exist in the database based on unique columns
    new_data = pd.merge(df, existing_data, on=unique_columns, how='left', indicator=True)
    new_data = new_data[new_data['_merge'] == 'left_only'].drop('_merge', axis=1)
    
    if not new_data.empty:
        # Insert new rows into the table
        new_data.to_sql(table_name, engine, if_exists='append', index=False)
        logging.info(f"{len(new_data)} new records inserted!")
    else:
        logging.info("No new records")


def main():
    main_dir = os.path.dirname(__file__)
    json_path:str = "https://goboardapi.azurewebsites.net/api/FacilityCount/GetCountsByAccount?AccountAPIKey=aedeaf92-036d-4848-980b-7eb5526ea40c"
    sqlite_path:str = "./data_public/corec_usage.db"

    fetched_dataframe = fetch_data(json_path = json_path)
    create_corec_usage_table(sqlite_file = sqlite_path)
    ingest_data(fetched_dataframe, sqlite_file = sqlite_path)


if __name__ == "__main__":
    main()
    