import pandas as pd
import numpy as np
from datetime import date

def basicTI(df):
  # Calculate returns
  df['NetChange'] = df['Adj Close'].diff()
  df['%Change'] = df['Adj Close'].pct_change() * 100
  # Log of Close
  df['logC']= np.log(df['Adj Close'])
  df['logR']= np.log(df['Adj Close']).diff()
  # Calc True_Range
  df['True_Range'] = np.maximum(df['High'] - df['Low'], abs(df['High'] - df['Close'].shift(1)), abs(df['Low'] - df['Close'].shift(1)))

  # Calculate DM+ & DM-
  df['DM+'] = np.maximum(df['High'] - df['High'].shift(1), 0)
  df['DM-'] = np.maximum((-1*df['Low'].diff()),0)

  # Calculate the body size of the candlestick. abs(close-open):
  df['Body_Size'] = abs(df['Close'] - df['Open'])

  # Calculate the wick size of the candlestick. max(abs(high-max(close-open), abs(low-min(close-open)):
  df['Top_Wick'] = df['High'] - np.maximum(df['Close'], df['Open'])
  df['Bottom_Wick'] = np.minimum(df['Close'], df['Open']) - df['Low']
  #EMAs
  df['9_EMA'] = df['Close'].ewm(span=9, adjust=False).mean()
  df['21_EMA'] = df['Close'].ewm(span=21, adjust=False).mean()
  df['54_EMA'] = df['Close'].ewm(span=54, adjust=False).mean()
  df['126_EMA'] = df['Close'].ewm(span=126, adjust=False).mean()
  # Calculate Bollinger Bands
  df['20_MA'] = df['Close'].rolling(window=20).mean()
  df['UBB'] = df['20_MA'] + 2 * df['Close'].rolling(window=20).std()
  df['LBB'] = df['20_MA'] - 2 * df['Close'].rolling(window=20).std()
  # Calculate Keltner Channels
  df['20_ATR'] = df['True_Range'].rolling(window=20).mean()
  df['20_EMA'] = df['Close'].ewm(span=20, adjust=False).mean()
  df['ub_kc'] = df['20_EMA'] + 1.5 * df['20_ATR']
  df['lb_kc'] = df['20_EMA'] - 1.5 * df['20_ATR']
  # Calculate Squeeze
  #if df['ub_kc'] < df['UBB'] or df['lb_kc'] > df['LBB'] :
  #  df['Squeeze'] = -1
  #else:
  #  df['Squeeze'] = df['Squeeze'].shift(1) + 1
    
  return df
  