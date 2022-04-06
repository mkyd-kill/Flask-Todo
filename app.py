from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import path

app = Flask(__name__) # creating the web application
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db" # /// are for the relative positioning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# making the model
class Todo(db.Model):
    # setting up the columns
    id = db.Column(db.Integer, primary_key=True) # setting the primary key
    content = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # function returns a string everytime a new element is created
    def __repr__(self) -> str:
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET']) # creating the default route
def index():
    # if post grab the task and write it on the database
    if request.method == 'POST':
        # logic for adding task into the database
        task_content = request.form['content']
        # creating a todo object
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception:
            return "There was an issue adding your page"
    # otherwise look at the page
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('hello/index.html', tasks=tasks) # the render_template renders the html page

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception:
        return 'There was a problem deleting the task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except Exception:
            return 'There was an issue updating task'
    else:
        return render_template('hello/update.html', task=task)

def create_database(app):
    try:
        if not path.exists('/test.db'):
            db.create_all(app=app)
            print('Database Created Successfully!!!')
    except Exception as error:
        print(f'Error During Database Creation: {error}')


if __name__ == "__main__":
    create_database(app=app)
    app.run(debug=True, port=5001) # debug set to true to show all the possible errors