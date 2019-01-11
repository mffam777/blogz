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
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
import secrets


app = Flask(__name__)
app.secret_key = 'secret'


# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:otro@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True

app.config["DEBUG"] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, owner):
        self.name = name
        self.completed = False
        self.owner = owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
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
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')
    # user not in file redirect to signup page
    return render_template('signup.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
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

    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')


@app.route('/', methods=['POST', 'GET'])
def index():

    owner = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        blog_name = request.form['blog']
        new_blog = Blog(blog_name, owner)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.filter_by(completed=False, owner=owner).all()
    completed_blogs = Blog.query.filter_by(completed=True, owner=owner).all()
    return render_template('index.html',title="Blogz!", 
        blogs=blogs, completed_blogs=completed_blogs)


@app.route('/delete-blog', methods=['POST'])
def delete_blog():

    blog_id = int(request.form['blog-id'])
    blog = Blog.query.get(blog_id)
    blog.completed = True
    db.session.add(blog)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run()
