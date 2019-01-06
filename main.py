from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True


class Task(db.Model):

    id = db.Column(db.Interger, primary_key=True)
    name = db.Column(db.String(120))

    #constructor
    def __init__(self, name):
        self.name = name

    # http://flask-sqlalchemy.pocoo.org/2.3/quickstart/ 
    #def __repr__(self):
        #return '<User %r>' % self.name

task = []

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task = request.form('task')
        task.append(task)

    return render_template('todos.html', title="Build a Blog", task=task)

# shield app 
if __name__ == '__main__':
    app.run()
