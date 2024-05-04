import os
import json
from datetime import date
from datetime import datetime
from flask import Flask, render_template, jsonify, request, redirect, flash, url_for
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import forms as frm
import plotly
import mplfinance as mp
import tradingview as tv
#from prophet import Prophet
#from prophet.plot import plot_plotly

#My files
from fetcher import monthlyFetcher, weeklyFetcher, dailyFetcher
import forecaster as fc
#from models import Users

#############################################################################################
app = Flask(__name__)

#FORMS
app.config['SECRET_KEY'] = os.environ['form_key']
#DB
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['db_key2']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ds.db'
#MAIL
app.config['MAIL_SERVER'] = "smtp.googlemail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = "chrisfigy@gmail.com"
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_PASSWORD'] = os.environ['mail_key']

db = SQLAlchemy(app)
#db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])


@login_manager.user_loader
def load_user(user_id):
  return Users.query.get(int(user_id))


#####################
#CLASSES
class Users(db.Model, UserMixin):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(28), nullable=False, unique=True)
  name = db.Column(db.String(128), nullable=False)
  email = db.Column(db.String(128), nullable=False, unique=True)
  phone_number = db.Column(db.String(10))
  date_added = db.Column(db.DateTime, default=datetime.utcnow)
  password_hash = db.Column(db.String(128))

  @property
  def password(self):
    raise AttributeError('password is not readable attribute')

  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
    return '<Name %r>' % self.name


class Projects(db.Model):
  __tablename__ = 'projects'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(120), nullable=False, unique=True)
  link = db.Column(db.String(120))
  descr = db.Column(db.String(3000), nullable=False)
  date = db.Column(db.DateTime, default=datetime.utcnow)
  display = db.Column(db.Boolean, default=False)

##########################
#one time setup
def insertProjects():
  '''One time call to add .csv file of projects to db.'''
  #Open Read Close File
  infile = open('projectsTable.csv', 'r')     #Open a file
  allData = infile.readlines()           #Read data
  infile.close                           #close file
  
  #Cleanup data to insert
  for aline in allData:
      aline = aline.strip()           #Remove new line chars.
      aline = aline.split(',')        #Split into a list on ', '
      proj = Projects(id=int(aline[0]),
         title=aline[1],
         link=aline[2],
         descr=aline[3],
         date=datetime.strptime(aline[4],"%m/%d/%Y").date(),
         display=int(aline[5]))
      db.session.add(proj)
      db.session.commit()
  return "ok"
  
##################
#ROUTES
@app.route("/")
def index():
  try:
      projects = Projects.query.all()
      print("Project Len = " + str(len(projects)))
  except:
      print("INSERTING .CSV DATA")
      db.create_all()
      insertProjects()
      #####
      hashed_pw = generate_password_hash("123456",
         method='sha256')
      user = Users(name="test",
      username="test",
      email="test",
      phone_number="555",
      password_hash=hashed_pw)
      db.session.add(user)
      db.session.commit()
    ####
  projects = Projects.query.all()
  for p in projects:
    print(p.id) 
  print(type(projects))
  
  return render_template('home.html', projects=projects)


@app.route("/project/<id>")
def show_project(id):
  Project = Projects.query.filter_by(id=id).first() #getProject(id)
  return render_template('project.html', project=Project)


@app.route("/admin")
@login_required
def admin():
  return render_template('admin.html')


@app.route("/database")
@login_required
def database():
  #if current_user.id == 1:
  #r = db.create_all()
  r = db.session.query(Projects).all()
  return render_template('database.html', r=r)


# else:
#   return redirect(url_for('page_not_found'))

#############################################
#  Users routes


#delete user
@app.route("/delete/<int:id>")
@login_required
def delete(id):
  if current_user.id == 1:
    name = None
    form = frm.UserForm()
    user_to_delete = Users.query.get_or_404(id)

    try:
      db.session.delete(user_to_delete)
      db.session.commit()
      flash('User delete successful.')
      users = Users.query.order_by(Users.date_added)
      return render_template('add_user.html',
                             form=form,
                             name=name,
                             users=users)

    except:
      flash("Exception: Delete Failed")
      return render_template('users.html', users=users)
  else:
    return redirect(url_for('page_not_found'))


#login
@app.route("/login", methods=["GET", "POST"])
def login():
  form = frm.LoginForm()
  if form.validate_on_submit():
    user = Users.query.filter_by(username=form.username.data).first()
    if user:
      if check_password_hash(user.password_hash, form.password_hash.data):
        login_user(user)
        return redirect(url_for('dashboard'))
      else:
        flash('Wong password')
    else:
      flash('User not found.')
  return render_template('login.html', form=form)


#logout
@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))


#login 2 dashboard
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
  #if sym == None:
  sym = '^GSPC'
  mdata, mtable = monthlyFetcher(sym)
  # Plot the histogram with 30 bins
  fig = fc.plot_histo_data(mdata)
  mgjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

  wtable, wt = weeklyFetcher(sym)
  return render_template('dashboard.html',
                         sym=sym,
                         mdata=mdata,
                         mtable=mtable,
                         mgjson=mgjson,
                         wtable=wtable,
                         wt=wt)


#reg new user
@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
  name = None
  form = frm.UserForm()
  #POST
  if form.validate_on_submit():
    user = Users.query.filter_by(email=form.email.data).first()
    if user is None:
      #token = s.dump(form.email.data, salt='verifyEmail')
      hashed_pw = generate_password_hash(form.password_hash.data,
                                         method='sha256')
      user = Users(name=form.name.data,
                   username=form.username.data,
                   email=form.email.data,
                   phone_number=form.phone_number.data,
                   password_hash=hashed_pw)
      db.session.add(user)
      db.session.commit()
      #Create Email with token
      #token = s.dump(form.email.data, salt='email-confirm')
      #msg_title = "PitSavvy Email Verification"
      #sender = "noreply@pitsavvy.com"
      #msg = Message(msg_title, sender=sender, recipients=[form.email.data])
      #link = url_for('confirm_email', token=token, _external=True)
      #msg.html = render_template("verify_email.html", form=form, link=link)

      #try:
      #  mail.send(msg)
      #return "Email sent.."
      #except Exception as e:
      #  print(e)
      #return "Error"
      name = form.name.data
      form.name.data = ''
      form.username.data = ''
      form.email.data = ''
      form.phone_number.data = ''
      form.password_hash.data = ''
      flash(
        "User created! Check your email for a one-time email confirmation before attempting to log in."
      )

    else:
      flash("User already exists. User not added. Try again.")
  #GET

  return render_template('register.html', form=form)


@app.route("/confirm_email/<token>")
def confirm_email(token):
  email = s.load(token, salt='email-confirm', max_age=600)


# return admin user list
@app.route("/users")
@login_required
def users():
  if current_user.id == 2:
    users = Users.query.order_by(Users.date_added)
    return render_template('users.html', users=users)
  else:
    return redirect(url_for('page_not_found'))


#update
@app.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):
  if current_user.id == 1:
    form = frm.UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
      name_to_update.name = request.form['name']
      name_to_update.email = request.form['email']
      name_to_update.phone_number = request.form['phone_number']
      try:
        db.session.commit()
        flash("Update Successful")
        name = None
        form = frm.UserForm()
        users = Users.query.order_by(Users.date_added)

        return render_template('add_user.html',
                               form=form,
                               name=name,
                               users=users)
      except:
        flash("Exception: Update Failed")
        return render_template('update.html',
                               form=form,
                               id=id,
                               name_to_update=name_to_update)
    else:
      return render_template('update.html',
                             form=form,
                             id=id,
                             name_to_update=name_to_update)
  else:
    return redirect(url_for('page_not_found'))


###################
#Extras
'''
@app.route("/name", methods=["GET", "POST"])
def name():
  name = None
  form = frm.NamerForm()
  if form.validate_on_submit():
    name = form.name.data
    form.name.data = ''
    flash("Submitted Successfully")
  return render_template('name.html', name=name, form=form)


@app.route("/test_pw", methods=["GET", "POST"])
@login_required
def test_pw():
  email = None
  password = None
  pw_to_check = None
  passed = None
  form = frm.PasswordForm()

  if form.validate_on_submit():
    email = form.email.data
    password = form.password_hash.data
    form.email.data = ''
    form.password_hash.data = ''
    #lookup by user email
    pw_to_check = Users.query.filter_by(email=email).first()
    #compare pw
    passed = check_password_hash(pw_to_check.password_hash, password)
    #flash("Submitted Successfully")
  return render_template('test_pw.html',
                         email=email,
                         password=password,
                         pw_to_check=pw_to_check,
                         passed=passed,
                         form=form)
'''


#Error pages
@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html')


@app.errorhandler(500)
def page_not_found(e):
  return render_template('500.html')


#example for all projects
#@app.route("/api/projects")
#def api_projects():
#  Projects = getProjects()
#  if not Project:
#    return "Not Found", 404
#  else:
#    return jsonify(Projects)


#example post method with form
@app.route("/admin/submit", methods=['post'])
def admin_submit():
  data = request.form
  return jsonify(data)


@app.route("/forecaster/<sym>")
@login_required
def forecaster(sym):
  if sym == None:
    sym = 'SPY'
  data = dailyFetcher(sym)
  fig = fc.plot_raw_data(data)
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

  #Forecast
  df_train = data[["Date", "Close"]]
  df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

  #m = Prophet()
  #m.fit(df_train, iter=1000)
  #future = m.make_future_dataframe(periods=period)
  #forecast = m.predict(future)

  #fig2 = plot_plotly(m, forecast)
  #graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

  return render_template('forecaster.html',
                         graphJSON=graphJSON)  # graphJSON2=graphJSON)


@app.route('/chartdata', methods=['POST'])
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
    mplfinance.plot(df, type='candle', style='yahoo', savefig="sample.png")

    return "image to transferred"


@app.route('/tv')
def tv():
  chart = tradingview.create_chart(symbol="AAPL", interval="1m")
  return render_template('tv.html', chart=chart)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)