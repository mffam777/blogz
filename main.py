# School: Launch Code
# Class: LC101 Ft. Meade, MD F18
# Student: Alberto Morales
# Instructor: Patrick Kozub
# TA: Jesse Shaw
# TA: Benjamin Muyinda
# Assignment: build-a-blog
# Due date: January 02, 2019 @ 21:00
# Location: Anne Arundel Community College; Mall Campus
# Git Hub Repository: https://github.com/mffam777/-build-a-blog.git


from flask import Flask, render_template, request, redirect, flash, url_for
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

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:toor@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

app.config["DEBUG"] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    def __init__(self, title, content):
        self.title = title
        self.completed = False
        self.content = content

    # def __repr__(self):
        # return f"Post('{self.title}', '{self.date_posted}')"


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


@app.route('/', methods=['GET', 'POST'])
def article():
    form = PostForm()
    if request.method == "GET":
        blogs = Blog.query.all()
        print(blogs[1].id)
        return render_template('article.html', blog=blogs)
    if request.method == "POST":
        post = Blog(title=request.form['btitle'], content=request.form['new_blog'])
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('article'))


@app.route('/blogi/', methods=['GET', 'POST'])
def get_blog():
    id_blog = request.args.get("id")
    blog = Blog.query.get(id_blog)
    # print(request)

    return render_template('posted_blog.html', blog=blog)


@app.route('/article', methods=['GET', 'POST'])
def home():

    return redirect(url_for('article'))


if __name__ == '__main__':
    app.run()
