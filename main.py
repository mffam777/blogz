from flask import Flask, Request, redirect, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

task = []

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task = request.form('task')
        task.append(task)

    return render_template('todos.html', title="Build a Blog", task=task)


app.run()
