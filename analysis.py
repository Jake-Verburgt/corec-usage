import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine,text as sql_text
from datetime import datetime as dt
import os


def read_db(sqlite_file: str ="/home/jake/scripts/workshop/corec-usage/data_public/corec_usage.db", 
               table_name: str ="corec_usage",
               start_range:dt= dt.strptime("1970-01-01T00:00:00.000",'%Y-%m-%dT%H:%M:%S.%f'),
               end_range:dt = dt.now()) -> pd.DataFrame:
    
    #Convert datetimes to strings that make sqlite happy
    start_range = start_range.strftime('%Y-%m-%dT%H:%M:%S.%f')#type:ignore
    end_range = end_range.strftime('%Y-%m-%dT%H:%M:%S.%f')#type:ignore

    #Open the conncection
    assert os.path.isfile(os.path.realpath(sqlite_file))
    conn_string = f"sqlite:///{os.path.realpath(sqlite_file)}"
    engine = create_engine(conn_string)

    #Fetch the data
    query = f"SELECT * FROM {table_name} WHERE LastUpdatedDateAndTime BETWEEN '{start_range}' AND '{end_range}';"
    existing_data = pd.read_sql_query(con=engine.connect(), 
                                    sql=sql_text(query))
    
    #Process data types and add date data
    existing_data["LastUpdatedDateAndTime"] = pd.to_datetime(existing_data.LastUpdatedDateAndTime) #Convert string column to datetime object
    existing_data["day_name"] = existing_data["LastUpdatedDateAndTime"].dt.day_name() # Extract day of the week
    existing_data["day_of_week"] = existing_data.LastUpdatedDateAndTime.dt.dayofweek #Get Day 0f week (0-7)
    existing_data["hour_of_day"] = existing_data.LastUpdatedDateAndTime.dt.round("h").dt.hour #Get nearest hour (0-23)
    existing_data["hour_of_day"] = existing_data["hour_of_day"].replace(0, 24)
    existing_data["IsClosed"] = existing_data.IsClosed.astype(bool)

    return existing_data



#Dump relevant timestamp information
# corec_df["LastUpdatedDateAndTime"] = corec_df.LastUpdatedDateAndTime.apply(pd.to_datetime) #Convert to datetime object
# corec_df["day"] = corec_df["LastUpdatedDateAndTime"].dt.day_name() # Extract day of the week
# corec_df["day"] = pd.Categorical(corec_df["day"],categories=days_of_week, ordered = True) # Make the days a proper categorical variable
# corec_df["time"] = corec_df["LastUpdatedDateAndTime"].dt.time #Extract time of day
# corec_df["date"] = corec_df["LastUpdatedDateAndTime"].dt.date #Extract date
# corec_df["hour"] = corec_df["LastUpdatedDateAndTime"].dt.round('H').dt.hour #Extract nearest hour
# corec_df["hour"] = corec_df["hour"].replace(0, 24)
# corec_df.head()

def main():
    data:pd.DataFrame = read_db()
    print(data)


if __name__ == "__main__":
    main()

# iso_format = dt.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
# A = dt.strptime("1970-01-01T00:00:00.000",'%Y-%m-%dT%H:%M:%S.%f')
# print(isinstance(A, dt))