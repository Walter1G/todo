from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):

    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f'<Todo {self.id}- {self.title}>'


@app.route('/welcome')
def home():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def welcome():

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, description=desc)
        db.session.add(todo)
        db.session.commit()

        allTodos = Todo.query.all()
        return render_template('index.html', alltodos=allTodos)
    if request.method == 'GET':

        allTodos = Todo.query.all()
        return render_template('index.html', alltodos=allTodos)


@app.route('/update/<int:id>', methods=['POST','GET'])
def updateTodo(id):

      if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(id=id).first()
        todo.title = title
        todo.description = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
      else:  # For GET request
          todo = Todo.query.filter_by(id=id).first()
          return render_template('update.html', todo=todo)


@app.route('/delete/<int:id>')
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
