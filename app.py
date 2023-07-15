from flask import Flask, render_template, jsonify

app = Flask(__name__)

PROJECTS = [
{
  'id':1,
  'title':"Neural Networks: Weather Prediction",
  'link':"www.example.com",
  'desc':"This project uses various ML technics to forecast the weather. There is a summary to show which ML methods work best." 
},
{
  'id':2,
  'title':"Neural Networks: S&P 500 Prediction",
  'link':"www.example.com",
  'desc':"This project uses various ML technics to forecast the closing price of the S&P 500. There is a summary to show which ML methods work best.",
  'date':"12/20/2021"  
},
{
  'id':3,
  'title':"Bond Yields",
  'link':"www.example.com",
  'desc':"This project calculates the yeild of bond auctions from Treasury Direct. The cheapest to deliver is also calculated along with a yield curve.",
  'date':"12/20/2021"  
},
  
]
@app.route("/")
def root():
  return render_template('home.html', projects=PROJECTS)

@app.route("/api/projects")
def webhook():
  return jsonify(PROJECTS)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)