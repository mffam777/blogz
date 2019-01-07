from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost :80/build-a-blog'

db = SQLAlchemy(app)
app.config['SQLALCHEMY_ECHO'] = True


class Blog(db.Model):

    id = db.Column(db.Interger, primary_key=True)
    name = db.Column(db.String(120))

    #constructor
    def __init__(self, name):
        self.name = name

    # http://flask-sqlalchemy.pocoo.org/2.3/quickstart/
    # https://github.com/Microsoft/vscode-python/issues/50
    #def __repr__(self):
        #return '<User %r>' % self.name

blogs = []

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog = request.form('blog')
        blogs.append(blog)

    return render_template('blog.html', title="Build a Blog", blogs=blogs)

# shield app
if __name__ == '__main__':
    app.run()
