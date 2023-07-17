from flask import Flask, render_template, jsonify
from database import getProjects

app = Flask(__name__)

@app.route("/")
def root():
  Projects = getProjects()
  return render_template('home.html', projects=Projects)

@app.route("/api/projects")
def apiprojects():
  Projects = getProjects()
  return jsonify(Projects)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)