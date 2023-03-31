from flask import Flask, render_template, url_for, request, redirect, flash, Blueprint
#from ..mod import *
from src.Models.models import *
from sqlalchemy import asc, desc

list_page = Blueprint('list', __name__, template_folder="templates")
@list_page.route("/Lists", methods = ['POST', 'GET'])
def Lists():
    if request.method == "POST":
        pass
    else:
        Lists = List.query.order_by(List.date_created).all()
        return render_template('List/List.html', Lists=Lists)
@list_page.route("/createList", methods = ['POST', 'GET'])
def createList():
    if request.method == "POST":
        title = request.form['textList']
        newList = List(title = title)
        
        try:
            db.session.add(newList)
            db.session.commit()
            return redirect("/Lists")
        except:
            return "There was an issue adding your task"
    else:
        
        return render_template('List/createList.html')

@list_page.route("/createNewTask/<int:id>", methods=['POST'])
def createNewTask(id):
    listToAdd = List.query.get_or_404(id)
    content = request.form['textBox']
    task = Todo(content = content, list_id = id)
    try:
        db.session.add(task)
        db.session.commit()
        return redirect('/Lists')
    except:
        return "there was a problem"
@list_page.route("/delete_task/<int:id>")
def deleteListTask(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/Lists')
    except:
        return "there was a problem deleting that task"
@list_page.route("/editListEvent/<int:id>", methods = ["GET", "POST"])
def updateListEvent(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == "POST":
        task_content = request.form["edit_content"]
        task_to_update.content = task_content
        try:
            db.session.commit()
            return redirect('/Lists')
        except:
            return "there was a problem updating that task"
    else:
        return render_template('List/editList.html', task_to_update=task_to_update)
    
@list_page.route('/checkboxList/<int:id>', methods = ['POST', 'GET'])
def checkbox(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        if request.form.get("Check") == "on":
            task.completed = 1
        else:
            task.completed = 0
        try:
            db.session.commit()
            return redirect('/Lists')
        except:
            return "there was a problem"

    