import pandas as pd
import requests
import os
import csv

#Function for getting data from ECCC using year and station_id
def get_monthly_data(year,station_id):
  #Create temporary dataframe which will return as an output of the function to appened to the main dataframe which will export to csv
  df = pd.DataFrame(columns=['Longitude(x)','Latitude(y)','Station Name','Climate ID','Date/Time','Year','Month','Day','Data Quality','Max Temp (°C)','Max Temp Flag','Min Temp (°C)','Min Temp Flag','Mean Temp (°C)','Mean Temp Flag','Heat Deg Days (°C)','Heat Deg Days Flag','Cool Deg Days (°C)','Cool Deg Days Flag'])

  #Requests data from ECCC for station and year,
  url = 
  response = requests.get(url)
  #Decodes csv using utf-8 format
  data = response.content.decode('utf-8')
  cr = csv.reader(data.splitlines(), delimiter=',')

  #Appends data from csv from ECCC onto temporary dataframe
  my_list = list(cr)
  for row in my_list:
      longitude = row[0]
      latitude = row[1]
      stn_name = row[2]
      cl_id = row[3]
      dt_tm = row[4]
      yr = row[5]
      mn = row[6]
      dy = row[7]
      dt_ql = row[8]
      mx_tp = row[9]
      mx_tp_fg = row[10]
      mn_tp = row[11]
      mn_tp_fg = row[12]
      mean_tp = row[13]
      mean_tp_flag = row[14]
      hdd = row[15]
      hdd_flag = row[16]
      cdd = row[17]
      cdd_flag = row[18]
      df = df.append({"Longitude(x)":longitude,"Latitude(y)":latitude,"Station Name":stn_name,"Climate ID":cl_id,"Date/Time":dt_tm,"Year":yr,"Month":mn,"Day":dy,"Data Quality":dt_ql,"Max Temp (°C)":mx_tp,"Max Temp Flag":mx_tp_fg,"Min Temp (°C)":mn_tp,"Min Temp Flag":mn_tp_fg,"Mean Temp (°C)":mean_tp,"Mean Temp Flag":mean_tp_flag,"Heat Deg Days (°C)":hdd,"Heat Deg Days Flag":hdd_flag,"Cool Deg Days (°C)":cdd,"Cool Deg Days Flag":cdd_flag}, ignore_index=True)

  #Removes 1st row which is column names
  df = df.iloc[1:]
  #Returns dataframe to append to main dataframe
  return df

#Function gets data for all years of station
#Have to use 4 digit climate ID of station
def all_station_data(year_start,year_end,station_id):
  #Create temporary dataframe to return as function output
  df_all = pd.DataFrame(columns=['Longitude(x)','Latitude(y)','Station Name','Climate ID','Date/Time','Year','Month','Day','Data Quality','Max Temp (°C)','Max Temp Flag','Min Temp (°C)','Min Temp Flag','Mean Temp (°C)','Mean Temp Flag','Heat Deg Days (°C)','Heat Deg Days Flag','Cool Deg Days (°C)','Cool Deg Days Flag'])

  #Forms range of years from those in station
  year_range=[year_start,year_end]
  years=range(year_range[0],year_range[1]+1)

  #Adds data for each month in each year in range to temporary dataframe
  for year in years:
    df_year = get_monthly_data(year,station_id)
    df_all = df_all.append(df_year)

  #Returns dataframe
  return df_all

#Getting all Trenton data and exporting to csv
Trenton_A = all_station_data(1953,2024,5126)
Trenton_A.to_csv("Trenton (5126) Data.csv", encoding='utf-8')

#Getting all Belleville data and exporting to csv
Belleville= all_station_data(1866,2024,4859)
Belleville.to_csv("Belleville (4859) Data.csv", encoding='utf-8')
