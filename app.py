from flask import Flask, render_template, jsonify
from database import getProjects, getProject


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

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)