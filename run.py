from flask import *
import psycopg2
from functools import wraps
from time import *

app=Flask(__name__)
app.secret_key="has"
@app.route('/')
def welcome():
	return render_template('welcome.html')
@app.route('/home')
def home():
		conn=psycopg2.connect(database='has')
		c=conn.cursor()
		c.execute('select * from blog1 order by id desc')
		value=[dict(id=i[0],title=i[1],post=i[2],day=i[3],time=i[4]) for i in c.fetchall()]
		return render_template('home.html',value=value)

def login_required(test):
	@wraps(test)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return test(*args,**kwargs)
		else:
			print 'you need to login first'
			return redirect(url_for('login'))
	return wrap

@app.route('/login',methods=['GET','POST'])
def login():
    	if request.method == 'POST':
        	if request.form['username'] != 'haseeb':
                	print 'Invalid username'
        	elif request.form['password'] != '123':
                	print 'Invalid password'
        	else:
			session['logged_in']=True
        	     	print 'You were logged in'
        		return redirect(url_for('post'))
        return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	return redirect(url_for('welcome'))


@app.route('/post')
@login_required
def post():
	return render_template('post.html')


@app.route('/home',methods=['POST'])
def submit():
	conn=psycopg2.connect(database='has')
	c=conn.cursor()
	c.execute('insert into blog1 (title,post,time,date) values(%s,%s,%s,%s)',[request.form['title'],request.form['post'],strftime("%d %b %Y ", gmtime()),strftime("%H:%M:%S ", gmtime())])
	conn.commit()
	c.execute('select * from blog1 order by id desc')

	value=[dict(id=i[0],title=i[1],post=i[2],day=i[3],time=i[4]) for i in c.fetchall()]
	return render_template('home.html',value=value)
	
app.run(debug=True)
