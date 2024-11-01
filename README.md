# corec-usage
Determine what time is best to get your workout in at the Purdue Corec!


# About 
So the Purdue CoRec center *USED* to provide historical data about how busy certain areas in the facility were at any given time on any given weekday. However, this has since been removed and the only *current* usage is provide.

This historical data was really nice for deciding what time of day to plan a trip, so I guess I'll just have to make it myself. This code is that. It performs the following:
1) Scrapes the current usage of the Corec every 30 minutes
2) Appends any new data to a database
3) Runs data analysis and visualization to guide my "when to go to corec" decisions.

## Data Format
Data is stored in a single sqlite table titled ```corec_usage``` under ```./data_public/corec_usage.db``` with the following columns:


|    |   id |   LocationId |   TotalCapacity | LocationName               | LastUpdatedDateAndTime   |   LastCount |   FacilityId |   IsClosed |
|---:|-----:|-------------:|----------------:|:---------------------------|:-------------------------|------------:|-------------:|-----------:|
|  0 |    1 |         6129 |              10 | Upper Track (4th Floor)    | 2024-10-13T20:26:16.17   |           0 |          976 |          0 |
|  1 |    2 |         5978 |              20 | Faculty/Staff Workout Area | 2024-10-13T20:26:16.827  |           1 |          976 |          0 |
|  2 |    3 |         5995 |              30 | Upper Fitness              | 2024-10-13T20:26:17.45   |           5 |          976 |          0 |
|  3 |    4 |         5996 |              75 | Upper Gym                  | 2024-10-13T20:26:18.077  |          45 |          976 |          0 |
|  4 |    5 |         7451 |              30 | MP6                        | 2024-10-13T20:26:18.78   |          20 |          976 |          0 |


# How to use:
## 1) Install Dependencies:

```pandas```, ```sqlite3```, ```sqalchemy```, ```requests```, ```matplitlib```, ```seaborn```, ```tabulate```
### Install conda environment from file
 * ```conda install -f environment.yaml```
## 2) Set Up Cron Job to collect data
Cron is the job scheduling bit that will run the scraping code on a regular intervals. From experience, the Corec seems to update their data on hour intervals at most, so an interval of 30 minutes should be fine to make sure no data is missed. 

To Set up a CRON Job to run every 30 minutes, you need to edit the "cron table"
* In a terminal, type ```crontab -e```
    * It will likely open in the vim or nano editor (two terminal based editors). You can change this by running the ```select-editor``` command, and selecting a different editor
* At the bottom of the file, add the following line: ```*/30 * *   *   *    /path/to/corec-usage/bin/python /path/to/corec_scrape.py```
    * MAKE SURE YOU ALTER THE PYTHON AND FILE PATHS
    * In the cron table, the prder goes "minutes, hours, dom, month, dow, command" The line above is just saying "Every 30 minutes of every hour of every day, run this command"

## 3) Run analysis on data
Data Analysis is ran in a n
