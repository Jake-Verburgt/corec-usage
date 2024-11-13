import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine,text as sql_text
from datetime import datetime as dt
import os


def read_db(sqlite_file: str ="./data_public/corec_usage.db", 
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
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    existing_data["day_name"] = existing_data["LastUpdatedDateAndTime"].dt.day_name() # Extract day of the week
    existing_data["day_name"] = pd.Categorical(existing_data.day_name,categories=days_of_week, ordered = True) # Make the days a proper categorical variable
    existing_data["day_of_week"] = existing_data.LastUpdatedDateAndTime.dt.dayofweek #Get Day 0f week (0-7)
    existing_data["hour_of_day"] = existing_data.LastUpdatedDateAndTime.dt.round("h").dt.hour #Get nearest hour (0-23)
    existing_data["hour_of_day"] = existing_data["hour_of_day"].replace(0, 24)
    existing_data["date"] = existing_data["LastUpdatedDateAndTime"].dt.date #Extract date

    existing_data["percent_util"] = existing_data.LastCount / existing_data.TotalCapacity

    existing_data.sort_values(by="LastUpdatedDateAndTime", inplace=True)

    return existing_data






def main():
    data:pd.DataFrame = read_db()
    day_hour_averages = data.groupby(["LocationId", "day_name", "hour_of_day"]).mean().reset_index().sort_values(["day_name", "hour_of_day"])
    
    day_hour_averages = day_hour_averages.pivot(index="day_name", columns=["LocationId", "hour_of_day"], values="percent_util") #percent_util #LastCount
    day_hour_averages.fillna(0.0, inplace = True)

    ids_to_name = data[["LocationId", "LocationName"]].drop_duplicates().set_index("LocationId")["LocationName"].to_dict()
    names_to_id = { name.strip():id for id, name in  ids_to_name.items()}

    for name, id in names_to_id.items():
        fig, ax = plt.subplots(1, 1, figsize=(16, 8))
        sns.heatmap(day_hour_averages[id], ax=ax)

        fig.savefig(f"./data_public/images/{name.replace(' ', '_').replace('/', '-')}.png")


if __name__ == "__main__":
    main()

# iso_format = dt.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
# A = dt.strptime("1970-01-01T00:00:00.000",'%Y-%m-%dT%H:%M:%S.%f')
# print(isinstance(A, dt))