import json
import plotly as plt
from plotly import graph_objects as go

def plot_raw_data(data):
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Open'))
  fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Close'))
  fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
  return fig
  