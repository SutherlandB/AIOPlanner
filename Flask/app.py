from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from datetime import datetime
from src.Models.models import *
from src.Services.todo.todo import todo_page
from src.Services.calendar import CalendarMonthly_page 
from src.Services.assigments import assignment_page 

app = Flask(__name__)
#config file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#initialize SQLALCHEMY_DATABASE_URI
db.init_app(app)
app.register_blueprint(todo_page)
app.register_blueprint(CalendarMonthly_page)
app.register_blueprint(assignment_page)
@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        new_Task = Todo(content=task_content)
        try:
            db.session.add(new_Task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"
        
    else:
        tasks = Todo.query.order_by(desc(Todo.date_created)).all()
        
        return render_template("dashboard.html", tasks=tasks)

if __name__ == '__main__':
    app.run(debug = True)
    

