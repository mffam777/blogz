# School: Launch Code
# Class: LC101 Ft. Meade, MD F18
# Student: Alberto Morales
# Instructor: Patrick Kozub
# TA: Jesse Shaw
# TA: Benjamin Muyinda
# Assignment: Blogz
# Due date: January 02, 2019 @ 21:00
# Location: Anne Arundel Community College; Mall Campus
# Git Hub Repository: https://github.com/mffam777/-blogz.git


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

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:otro@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True

app.config["DEBUG"] = True
db = SQLAlchemy(app)




if __name__ == '__main__':
    app.run()
