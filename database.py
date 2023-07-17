from sqlalchemy import create_engine, text
import os

def createTable(engine):
  createtbl="""
  CREATE TABLE IF NOT EXISTS Projects(
  	id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(120) NOT NULL,
    link VARCHAR(120) NOT NULL,
    descr VARCHAR(3000),
    date VARCHAR(15),
    PRIMARY KEY (id)
    )"""
  conn = engine.connect() 
  conn.execute(text(createtbl)) 
  conn.commit()
  conn.close()
  return "Table Created"

def getProjects():
  my_secret = os.environ['db_key']
  engine = create_engine(my_secret, connect_args={
    "ssl":{
    "ssl_ca": "/etc/ssl/cert.pem"
    }
  })
  conn = engine.connect()
  result = conn.execute(text("Select * from Projects"))  
  conn.close()
  result_dict =[]
  for row in result.all():
    result_dict.append(dict(row._mapping))
  return result_dict

def getTables(engine):
  conn = engine.connect()
  result = conn.execute(text("Show Tables"))  
  conn.commit()
  conn.close()
  return result.all

def insertProjects(engine):
  conn = engine.connect()
  #Insert data
  for project in PROJECTS:
    conn.execute(text("INSERT INTO Projects (title, link, descr, date) VALUES('"+project['title']+"','"+project['link']+"','"+project['desc']+"','"+project['date']+"')"))  
  conn.commit()
  conn.close()
###############
PROJECTS = [
{
  'title':"Neural Networks Weather Prediction",
  'link':"www.example.com",
  'desc':"This project uses various ML technics to forecast the weather. There is a summary to show which ML methods work best.",
  'date':"12/20/2021"  
},
{
  'title':"Neural Networks: S&P 500 Prediction",
  'link':"www.example.com",
  'desc':"This project uses various ML technics to forecast the closing price of the S&P 500. There is a summary to show which ML methods work best.",
  'date':"12/20/2021"  
},
{
  'title':"Bond Yields",
  'link':"www.example.com",
  'desc':"This project calculates the yeild of bond auctions from Treasury Direct. The cheapest to deliver is also calculated along with a yield curve.",
  'date':"12/20/2021"  
}]
###########
#db_string = pw.pw['db_connection_str'] #os.getenv("DB_CONNECTION_STRING")
#my_secret = os.environ['DB_CONNECTION_STRING']
#print(os.getenv("DB_CONNECTION_STRING"))
#print(my_secret)
#engine = create_engine(db_string, connect_args={
#    "ssl":{
#    "ssl_ca": "/etc/ssl/cert.pem"
#    }
#  })
#x = getProjects()
#print(x)