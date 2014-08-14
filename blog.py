#blog using flask

import os
import sqlite3
from flask import Flask,request,g,redirect,url_for,render_template,flash,session
from functools import wraps
from datetime import datetime



from flask import g, session


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
   DATABASE=os.path.join(app.root_path,'blog.db'),
   DEBUG=True,
   SECRET_KEY='jibin jose',
   USERNAME='admin',
   PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS',silent=True)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash(' You need to login first.')
            return redirect(url_for('login'))
    return wrap


def connect_db():
  rv=sqlite3.connect(app.config['DATABASE'])
  rv.row_factory=sqlite3.Row
  return rv

def init_db():
  with app.app_context():
     db=get_db()
     with app.open_resource('schema.sql',mode='r')as f:
	db.cursor().executescript(f.read())
     db.commit()


def get_db():
  if not hasattr(g,'sqlite_db'):
     g.sqlite_db=connect_db()
  return g.sqlite_db



@app.route('/add',methods=['GET','POST'])
@login_required
def add():
  if request.method=='POST':
    if request.form['publish']=="publish":
    
      db=get_db()
      #db.execute('insert into posts (title,post) values (?,?)',[request.form['title'],request.form['content']])
      #db.execute('insert into posts (title,post) values ("second","i am jac")')
      db.execute('insert into posts (title,catogory,t_comments,p_date,post) values (?,?,?,?,?)',[request.form['title'],request.form['catogary'],0,datetime.now().replace(microsecond=0),request.form['content']])
      db.commit()
      flash(' Details added')
  return render_template('newpost.html')


@app.route('/view',methods=['GET','POST'])
@login_required
def  view():
  db = get_db()
  cur = db.execute('select title,catogory,t_comments,p_date,post from posts')
  entries = cur.fetchall()
  return render_template('home.html', entries=entries)

  




@app.route('/contact',methods=['GET','POST'])
@login_required
def  contact():
  return render_template('contact.html')



@app.route('/about',methods=['GET','POST'])
@login_required
def about():
  return render_template('about.html')



@app.route('/post/<post_title>',methods=['GET','POST'])

def show_post(post_title):
  if request.method=='POST':
    if request.form['submit']=="submit":
      print "in submit"
      db=get_db()
      #db.execute('insert into posts (title,post) values (?,?)',[request.form['title'],request.form['content']])
      #db.execute('insert into posts (title,post) values ("second","i am jac")')
      #db.execute('update posts set comment = (?),c_name = (?) where title = (?)',[request.form['comment'],request.form['c_name'],post_title])
      db.execute('update posts set t_comments = t_comments+1 where title = (?)',[post_title])
      db.execute('insert into comments(c_id,c_name,comment) values (?,?,?)',[post_title,request.form['c_name'],request.form['comment']])


      db.commit()
      flash(' Details added')
      print "asd"+post_title
  db = get_db()
  cur = db.execute('select title,catogory,t_comments,p_date,post from posts where title= ?',[post_title])
  entries = cur.fetchall()
  print entries
  cur = db.execute('select c_name,comment from comments where c_id= ?',[post_title])
  comments = cur.fetchall()
  cur = db.execute('select title from posts')
  titles = cur.fetchall()
  

  return render_template('singlepost.html',entries=entries,comments=comments,titles=titles)





@app.route('/',methods=['GET','POST'])
def home():
  if request.method=='POST':
    if request.form['opt']=="login":
      return redirect(url_for('login'))
    if request.form['opt']=="logout":
      return redirect(url_for('logout'))
  if session['logged_in'] == True:
    return redirect(url_for('view'))
    
  return render_template('home.html')

@app.route('/welcome')
def welcome():
   return render_template('welcome.html')  

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = "username"
        elif request.form['password'] != app.config['PASSWORD']:
            error = "password"
        else:
            session['logged_in'] = True
            session['username'] = app.config['USERNAME']
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login1.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash(' You were logged out')
    return redirect(url_for('home'))

@app.teardown_appcontext
def close_db(error):
  if hasattr(g,'sqlite_db'):
     g.sqlite_db.close()



if __name__=='__main__':
 app.run(debug=True)
