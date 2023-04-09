from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from datetime import datetime
from src.Models.models import *
from src.Services.todo.todo import todo_page
from src.Services.calendar import calendar_monthly_page 
from src.Services.assigments import assignment_page 
from src.Services.list import list_page

class App():
    app = Flask(__name__)
    instance = None
    def __init__(self):
        self.instantiate()

    def instantiate(self):
        if self.instance ==  None:
            self.instance = self
        self.register()

    def register(self):
        #config file
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        #initialize SQLALCHEMY_DATABASE_URI
        db.init_app(self.app)
        self.app.register_blueprint(todo_page)
        self.app.register_blueprint(calendar_monthly_page)
        self.app.register_blueprint(assignment_page)
        self.app.register_blueprint(list_page)
        with self.app.app_context():
            db.create_all()
        
    

    
    @app.route('/')
    def index():
        return render_template("Landing/landing.html")

    @app.route('/dashboard', methods = ['POST', 'GET'])
    def dashboard():
        if request.method == "POST":
            task_content = request.form['content']
            new_Task = Todo(content=task_content)
            try:
                db.session.add(new_Task)
                db.session.commit()
                return redirect('/dashboard')
            except:
                return "There was an issue adding your task"
            
        else:
            tasks = Todo.query.order_by(desc(Todo.date_created)).all()
            events = Event.query.order_by(Event.dateTime_of_event).all()
            return render_template("dashboard.html", tasks=tasks, Events = events)


if __name__ == '__main__':
    app = App()
    app.app.run(debug = True)
    

