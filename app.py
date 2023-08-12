from flask import Flask, render_template, jsonify, request
from database import getProjects, getProject
from prophet import Prophet
from prophet.plot import plot_plotly
import yfinance as yf
from datetime import date
import forecaster as fc
import plotly 
import json
import mplfinance as mp
import tradingview as tv


app = Flask(__name__)

@app.route("/")
def root():
  Projects = getProjects()
  return render_template('home.html', projects=Projects)

@app.route("/project/<id>")
def show_project(id):
  Project = getProject(id)
  return render_template('project.html', project=Project)

@app.route("/api/projects")
def api_projects():
  Projects = getProjects()
  if not Project:
    return "Not Found", 404
  else:
    return jsonify(Projects)

#@app.route("/project/<id>/submit", methods=['post'])
#def api_project_comment(id):
#  data = request.form
#  return jsonify(data)
  
@app.route("/forecaster/<sym>")
def forecaster(sym):
  if sym == None:
    sym = 'SPY'
  START = "2018-01-01"
  TODAY = date.today().strftime("%Y-%m-%d")
  data = yf.download(sym, START, TODAY)
  data.reset_index(inplace=True)
  fig = fc.plot_raw_data(data)
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

  #Forecast
  df_train = data[["Date","Close"]]
  df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

  m = Prophet()
  m.fit(df_train, iter=1000)
  #future = m.make_future_dataframe(periods=period)
  #forecast = m.predict(future)

  #fig2 = plot_plotly(m, forecast)
  #graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

  
  return render_template('forecaster.html', graphJSON=graphJSON, graphJSON2=graphJSON)

@app.route('/chartdata', methods =['POST'])
def chart_data():
    if request.method == 'POST':
      sym = 'SPY'
      START = "2018-01-01"
      TODAY = date.today().strftime("%Y-%m-%d")
      data = yf.download(sym, START, TODAY)
      data.reset_index(inplace=True)
      
      body = request.json
      df = data
      df.index.name = 'Date'
      mplfinance.plot(df, type = 'candle',style ='yahoo',savefig ="sample.png")
      
      return "image to transferred" 

@app.route('/tv')
def tv():
  chart = tradingview.create_chart(symbol="AAPL", interval="1m")
  return render_template('tv.html', chart=chart)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)