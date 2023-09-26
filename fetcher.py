import pandas as pd
import yfinance as yf
import datetime
from datetime import date


def monthlyFetcher(sym):
  START = "2018-01-01"
  TODAY = date.today().strftime("%Y-%m-%d")
  data = yf.download(sym, START, TODAY, interval='1mo')
  # Calculate returns
  data['NetChange'] = data['Adj Close'].diff()
  data['%Change'] = data['Adj Close'].pct_change() * 100
  # Extract year and month from the Date index
  print(f'Index is a {type(data.index)} datatype.')
  data['Year'] = data.index.year
  data['Month'] = data.index.month
  # Pivot the data to create a pivot table with months as columns and years as rows
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
  # average_row = pivot_table.mean().to_frame(name="Average")
  # pivot_table = pivot_table.append(average_row.T)
  mtable = pivot_table.to_html(classes='table table-striped')
  return mtable


def weeklyFetcher(sym):
  START = "2018-01-01"
  TODAY = date.today().strftime("%Y-%m-%d")
  data = yf.download(sym, START, TODAY, interval='1wk')
  # Calculate returns
  data['NetChange'] = data['Adj Close'].diff()
  data['%Change'] = data['Adj Close'].pct_change() * 100
  # Extract year and month from the Date index
  data['Year'] = data.index.year
  data['Week'] = data.index.isocalendar().week

  # Pivot the data to create a pivot table with months as columns and years as rows
  pivot_table = pd.pivot_table(data,
                               values=['NetChange'],
                               index='Year',
                               columns='Week')

  # Rename the columns with month names
  week_names = range(1, 54)
  pivot_table.columns = week_names

  # Calculate the average row and add it to the pivot table
  # average_row = pivot_table.mean().to_frame(name="Average")
  # pivot_table = pivot_table.append(average_row.T)
  wtable = pivot_table.to_html(classes='table table-striped')
  return wtable, date.today().isocalendar().week


def dailyFetcher(sym):
  START = "2014-01-01"
  TODAY = date.today().strftime("%Y-%m-%d")
  data = yf.download(sym, START, TODAY)
  data.reset_index(inplace=True)
  return data
