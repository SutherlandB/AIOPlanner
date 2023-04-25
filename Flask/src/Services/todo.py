from flask import Blueprint
from flask import Flask, render_template, url_for, request, redirect, flash, Blueprint
#from ..mod import *
from src.Models.models import *
from sqlalchemy import asc, desc


todo_page = Blueprint('dashboard', __name__, template_folder="templates")

@todo_page.route('/delete/<int:id>' )
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/dashboard')
    except:
        return "there was a problem deleting that task"

@todo_page.route('/update/<int:id>', methods = ['POST', 'GET'] )
#reassign assignment object with new content and update database
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == "POST":
        if not request.form['content']:
               return redirect('/dashboard')
        task_content = request.form["content"]
        task_to_update.content = task_content
        
        try:
            db.session.commit()
            return redirect('/dashboard')
        except:
            return "there was a problem updating that task"
    else:
        return render_template('update.html', task_to_update=task_to_update)

@todo_page.route('/checkbox/<int:id>', methods = ['POST', 'GET'])
def checkbox(id):
    #update if the task has been completed or not 
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        if request.form.get("Check") == "on":
            task.completed = 1
        else:
            task.completed = 0
        try:
            #commit change and update
            db.session.commit()
            return redirect('/dashboard')
        except:
            return "there was a problem updating that task"
