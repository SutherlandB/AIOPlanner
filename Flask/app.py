from sqlalchemy import asc, desc
from datetime import datetime
from src.Models.models import *
from src.Services.todo import todo_page
from src.Services.calendar import calendar_monthly_page 
from src.Services.assigments import assignment_page 
from src.Services.list import list_page

class App(): #driver class to initiate an instance of the application
    app = Flask(__name__)
    instance = None
    def __init__(self):
        self.instantiate()

    def instantiate(self): #register the application for starting database 
        if self.instance ==  None:
            self.instance = self
        self.register()

    def register(self):
        #config file
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        #initialize SQLALCHEMY_DATABASE_URI
        db.init_app(self.app)
        #register the blueprint of all methods for database to be updated
        self.app.register_blueprint(todo_page)
        self.app.register_blueprint(calendar_monthly_page)
        self.app.register_blueprint(assignment_page)
        self.app.register_blueprint(list_page)
        #start the database application
        with self.app.app_context():
            db.create_all()
        
    

    #route to the landing page 
    @app.route('/')
    def index():
        return render_template("Landing/landing.html")

    #dashboard page route
    @app.route('/dashboard', methods = ['POST', 'GET'])
    def dashboard():
        if request.method == "POST":
            task_content = request.form['content']
            if len(request.form['content']) < 1:
                   return redirect('/dashboard')
            new_Task = Todo(content=task_content)
            #if the content is valid to add to the TO-DO list, update the database and refresh website
            try:
                db.session.add(new_Task)
                db.session.commit()
                return redirect('/dashboard')
            except:
                return "There was an issue adding your task"
            
        else:
            #show the tasks on the dashboard
            tasks = Todo.query.order_by(desc(Todo.date_created)).all()
            events = Event.query.order_by(Event.dateTime_of_event).all()
            return render_template("dashboard.html", tasks=tasks, Events = events)


if __name__ == '__main__':
    #run the app in main
    app = App()
    app.app.run(debug = True)
    

