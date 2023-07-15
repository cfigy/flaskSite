from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def root():
  return render_template('home.html')

@app.route("/projects")
def webhook():
  return render_template('hook.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)