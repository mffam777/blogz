# School: Launch Code
# Class: LC101 Ft. Meade, MD F18
# Student: Alberto Morales
# Instructor: Patrick Kozub
# TA: Jesse Shaw
# TA: Benjamin Muyinda
# Assignment: Blogz
# Due date: January 14, 2019 @ 21:00
# Location: Anne Arundel Community College; Mall Campus
# Git Hub Repository: https://github.com/mffam777/-blogz.git


from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
#from datetime import datetime
#from flask_wtf import FlaskForm
#from wtforms import StringField, SubmitField, BooleanField, TextAreaField, Form, TextField
#from wtforms.validators import DataRequired, ValidationError, Email
#import secrets
from hashutils import make_pw_hash, check_pw_hash, make_salt

# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:otro@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'secret'


class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(120))
    title = db.Column(db.String(120))
    # completed = db.Column(db.Boolean)
    post = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, title, owner):
        self.title = title
        self.post = False        
        #self.post = Blog
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    pw_hash = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.pw_hash = make_pw_hash(password, salt=None)

@app.before_request
#@app.route('/', methods=['POST', 'GET'])
def require_login():
    
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

# initial page
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_pw_hash(password, user.pw_hash):
            session['email'] = email
            flash("Logged in")
            # verify index.html
            return redirect('/')
        else:
                flash('User password incorrect, or user does not exist', 'error')
    # user not in file redirect to signup page
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    #print("------SIGN UP-----------/")

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['email']

    return redirect('/')


@app.route('/', methods=['POST', 'GET'])
def index():
    #print("------INDEX-----------/")

    owner = User.query.filter_by(email=session['email']).first()

    #form = Blog()
    #if request.method == "GET":
        #blogs = Blog.query.all()
        #print(blogs[1].id)
        #return render_template('index.html', blog=blogs)

   #if request.method == "POST":
       # post = Blog(title=request.form['btitle'],
                   # content=request.form['new_blog'])
        #db.session.add(post)
       # db.session.commit()
        #flash('Your post has been created!', 'success')
        #return redirect(url_for('index.html'))


    if request.method == 'POST':
        #print("-------------------")
        #print(request.form)
        print("-------------------")
        blog_name = request.form['blog']
        #blog_id = request.form['blog']
        #blog_title = request.form['btitle']
        #blog_post = request.form['new_blog']
        new_blog = Blog(blog_name, owner)
        #new_blog = Blog(blog_id, owner)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.filter_by(post=False, owner=owner).all()
    post_blogs = Blog.query.filter_by(post=True, owner=owner).all()
    return render_template('index.html', title="Blogz!", 
    blogs=blogs, post_blogs=post_blogs)

  


@app.route('/delete-blog', methods=['POST'])
def delete_blog():

    blog_id = int(request.form['blog-id'])
    blog = Blog.query.get(blog_id)
    blog.post = True
    db.session.add(blog)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run()
