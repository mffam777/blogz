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
    completed = db.Column(db.Boolean)

    # constructor
    def __init__(self, name):
        self.name = name
        self.completed = False

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


 
@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_name = request.form('blog')
        new_blog = Blog(blog_name)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.filter_by(completed=False).all()
    completed_blogs = Blog.query.filter_by(completed=True).all()
    return render_template('blog.html', title="Build a Blog",
                           blogs=blogs, completed_blogs=completed_blogs)

# handeller to deleted blog


@app.route('/delete-blog', methods=['POST'])
def delete_blog():

    blog_id = int(request.form['blog-id'])
    blog = Blog.query.get(blog_id)
    blog.completed = True
    db.session.add(blog)
    db.session.commit()

    return redirect('/')



# shield app
if __name__ == '__main__':
    app.run()
