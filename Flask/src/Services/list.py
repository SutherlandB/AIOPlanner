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
        #render the List if request method is GET
        Lists = List.query.order_by(List.date_created).all()
        return render_template('List/List.html', Lists=Lists)
#create the List with valid content 
@list_page.route("/createList", methods = ['POST', 'GET'])
def createList():
    if request.method == "POST":
        #add the created list to the ordered list titles
        allListNames = List.query.order_by(List.title).all()
        #if the form has content, add it to the database, otherwise refresh and do nothing
        if not request.form['textList']:
               return redirect('/Lists')
        for i in allListNames:
            if request.form['textList'] == i.title:
                return redirect('/Lists')
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

#create a task within a List's box 
@list_page.route("/createNewTask/<int:id>", methods=['POST'])
def createNewTask(id):
    listToAdd = List.query.get_or_404(id)
    content = request.form['textBox']
    task = Todo(content = content, list_id = id)
    #input validation for content in the list's tasks
    if not request.form['textBox']:
           return redirect('/Lists')
    try:
        #add content to the database and refresh
        db.session.add(task)
        db.session.commit()
        return redirect('/Lists')
    except:
        return "there was a problem"
    
#delete the list's task and refresh to reflect the updated status
@list_page.route("/delete_task/<int:id>")
def deleteListTask(id):
    task_to_delete = Todo.query.get_or_404(id)
    #delete the list task and update the database
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/Lists')
    except:
        return "there was a problem deleting that task"
    
#edit the task's content, update the content, refresh and update the user interface
@list_page.route("/editListEvent/<int:id>", methods = ["GET", "POST"])
def updateListEvent(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == "POST":
        task_content = request.form["edit_content"]
        if not request.form['edit_content']:
               return redirect('/Lists')
        task_to_update.content = task_content
        try:
            db.session.commit()
            return redirect('/Lists')
        except:
            return "there was a problem updating that task"
    else:
        return render_template('List/editList.html', task_to_update=task_to_update)
    
#checkbox should be updated depending on the state, updated in the database and refreshed
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
        
#delete the list with all of its contents and refresh 
@list_page.route("/deleteList/<int:id>/")
def deleteList(id):
    task_to_delete = List.query.get_or_404(id)
    try:
        
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/Lists')
    except:
        return "there was a problem deleting that list"

    