import pandas as pd
from pandas.core import series
import numpy as np
import yfinance as yf
from datetime import date
import calculator as calc


def monthlyFetcher(sym):
  '''This function fetches monthly data from yahoo and returns a timeseries
      and a monthly pivot datasets.
      
      TODO: -Remove the hardcoded start date and allow user to define'''
  
  START = "2018-01-01"
  TODAY = date.today().strftime("%Y-%m-%d")
  data = yf.download(sym, START, TODAY, interval='1mo')
  print(data)
  data = calc.basicTI(data)
  
  #Add day of weekto both and hour too Hour Datset
  #data['DoW'] = data.index.day_of_week
  #find out the number of hours between row 1 & 2
  #delta = df.index[1] - df.index[0]
  #hrs = delta.days * 24 + delta.seconds // 3600
  #if hrs < 24:
  #  df['Hour'] = df.index.hour
  #  df['DoW'] = df.index.day_of_week

  timestamp_s = data.index.map(pd.Timestamp.timestamp)

  day = 24*60*60
  month = (21)*day
  year = (254)*day

  #if hrs < 24:
  #  df['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
  #  df['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
  data['Month sin'] = np.sin(timestamp_s * (2 * np.pi / month))
  data['Month cos'] = np.cos(timestamp_s * (2 * np.pi / month))
  data['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
  data['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))
  
  # Extract year and month from the Date index
  print(f'Index is a {type(data.index)} datatype.')
  data['Year'] = data.index.year
  data['Month'] = data.index.month
  # Pivot to create a table with months as columns and years as rows
  pivot_table = pd.pivot_table(data,
                               values=['NetChange'],
                               index='Year',
                               columns='Month')

  # Rename the columns with month names
  month_names = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
    'Nov', 'Dec'
  ]
  pivot_table.columns = month_names

  # Calculate the average row and add it to the pivot table
  average_row = pivot_table.mean(axis=0)
  std = pivot_table.std(axis=0)  # Calculate the standard dev

  # Convert the average row into a DataFrame and transpose it
  average_row_df = pd.DataFrame(average_row, columns=["Average"]).T
  std_df = pd.DataFrame(std, columns=["Std Dev"]).T

  # Concatenate the pivot table and the average row
  pivot_table = pd.concat([pivot_table, average_row_df, std_df])

  mtable = pivot_table.to_html(classes='table table-striped')
  return data, mtable


def weeklyFetcher(sym):
  START = "2018-01-01"
  TODAY = date.today().strftime("%Y-%m-%d")
  data = yf.download(sym, START, TODAY, interval='1wk')
  data = calc.basicTI(data)
  
  #Add day of weekto both and hour too Hour Datset
  #data['DoW'] = data.index.day_of_week
  #find out the number of hours between row 1 & 2
  #delta = df.index[1] - df.index[0]
  #hrs = delta.days * 24 + delta.seconds // 3600
  #if hrs < 24:
  #  df['Hour'] = df.index.hour
  #  df['DoW'] = df.index.day_of_week

  timestamp_s = data.index.map(pd.Timestamp.timestamp)

  day = 24*60*60
  month = (21)*day
  year = (254)*day

  #if hrs < 24:
  #  df['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
  #  df['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
  data['Month sin'] = np.sin(timestamp_s * (2 * np.pi / month))
  data['Month cos'] = np.cos(timestamp_s * (2 * np.pi / month))
  data['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
  data['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))


  
  # Extract year and month from the Date index
  data['Year'] = data.index.year
  data['Week'] = data.index.isocalendar().week

  # Pivot to create a table with months as columns and years as rows
  pivot_table = pd.pivot_table(data,
                               values=['NetChange'],
                               index='Year',
                               columns='Week')

  # Rename the columns with month names
  week_names = range(1, 54)
  pivot_table.columns = week_names

  # Calculate the average row
  average_row = pivot_table.mean(axis=0)
  std = pivot_table.std(axis=0)  # Calculate the standard dev

  # Convert the average row into a DataFrame and transpose it
  average_row_df = pd.DataFrame(average_row, columns=["Average"]).T
  std_df = pd.DataFrame(std, columns=["Std Dev"]).T
 
  # Concatenate the pivot table and the average row
  pivot_table = pd.concat([pivot_table, average_row_df, std_df])
  
  wtable = pivot_table.to_html(classes='table table-striped')
  week_number = date.today().isocalendar().week

  return wtable, week_number

def dailyFetcher(sym):
  START = "2014-01-01"
  TODAY = date.today().strftime("%Y-%m-%d")
  data = yf.download(sym, START, TODAY)
  data.reset_index(inplace=True)
  return data

def daily2Fetcher(sym):
  '''This function fetches daily data from yahoo and returns a timeseries dataframe TODO: -Remove the hardcoded start date and allow user to define'''
  START = "2018-01-01"
  TODAY = date.today().strftime("%Y-%m-%d")
  data = yf.download(sym, START, TODAY)
  data = calc.basicTI(data)
  
  #Add day of weekto both and hour too Hour Datset
  data['DoW'] = data.index.day_of_week
  #find out the number of hours between row 1 & 2
  #delta = df.index[1] - df.index[0]
  #hrs = delta.days * 24 + delta.seconds // 3600
  #if hrs < 24:
  #  df['Hour'] = df.index.hour
  #  df['DoW'] = df.index.day_of_week

  timestamp_s = data.index.map(pd.Timestamp.timestamp)

  day = 1 #24*60*60
  month = (21)*day
  year = (254)*day

  #if hrs < 24:
  #  df['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
  #  df['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
  data['Month sin'] = np.sin(timestamp_s * (2 * np.pi / month))
  data['Month cos'] = np.cos(timestamp_s * (2 * np.pi / month))
  data['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
  data['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))

  # Extract year and month from the Date index
  print(f'Index is a {type(data.index)} datatype.')
  data['Year'] = data.index.year
  data['Month'] = data.index.month
  

  # Pivot to create a table with months as columns and years as rows
  #pivot_table = pd.pivot_table(data,
  #                             values=['NetChange'],
  #                             index='Year',
  ##month_names = [
  #  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
  #  'Nov', 'Dec'
  #]
  #pivot_table.columns = month_names

  # Calculate the average row and add it to the pivot table
  #average_row = pivot_table.mean(axis=0)
  #std = pivot_table.std(axis=0)  # Calculate the standard dev

  # Convert the average row into a DataFrame and transpose it
  #average_row_df = pd.DataFrame(average_row, columns=["Average"]).T
  #std_df = pd.DataFrame(std, columns=["Std Dev"]).T

  # Concatenate the pivot table and the average row
  #pivot_table = pd.concat([pivot_table, average_row_df, std_df])

  #mtable = pivot_table.to_html(classes='table table-striped')
  return data