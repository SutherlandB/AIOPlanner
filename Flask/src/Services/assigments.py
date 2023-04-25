from flask import Flask, render_template, url_for, request, redirect, flash, Blueprint
#from ..mod import *
from src.Models.models import *


assignment_page = Blueprint('assignments', __name__, template_folder="templates") #add routing functionality to assignment page

@assignment_page.route('/delete_assignment/<int:id>' ) #delete assignments from database for assignments
def delete_assignment(id):
    to_delete = AssignmentTracker.query.get_or_404(id)
    #update database and refresh webpage
    try:
        db.session.delete(to_delete)
        db.session.commit()
        return redirect('/assignments')
    except:
        return "there was a problem deleting that task"
    
@assignment_page.route('/add_item', methods = ['POST'])
def new():
    #check if input is valid or a duplicate
    if not request.form['title'] or not request.form['due_date']:
       return redirect('/assignments')
    else:
       new_title = request.form['title']
       new_course = request.form['course']
       input_date_str = request.form['due_date']
       new_date = datetime.strptime(input_date_str, "%Y-%m-%d").date()
       assignment = AssignmentTracker(title=new_title, course=new_course,
          due_date=new_date)
       #update database and refresh webpage
       db.session.add(assignment)
       db.session.commit()
       
       return redirect('/assignments')
   
@assignment_page.route('/update_form/<int:id>')
def update_form(id):
    assignment = db.session.get(AssignmentTracker, id)
    #place the assignment into displayed content box
    return render_template('Assignments/home.html', update_assignment_id=id, update_assignment_title=assignment.title, update_assignment_due_date=assignment.due_date)

    
@assignment_page.route('/update_assignment/<int:id>', methods=['POST'])
def update_assignment(id):
    #reassign assignment object with new content and update database
    title = request.form['title']
    due_date = request.form['due_date']
    new_date = datetime.strptime(due_date, "%Y-%m-%d").date()
    assignment = db.session.get(AssignmentTracker, id)
    assignment.title = title
    assignment.due_date = new_date
    #update database and refresh webpage
    db.session.commit()
    return redirect('/assignments')


@assignment_page.route('/checkbox_assingment/<int:id>', methods = ['POST', 'GET'])
def checkbox_assingment(id):
    task = AssignmentTracker.query.get_or_404(id)
    #hit the checkbox and refresh the webpage with the updated content 
    if request.method == "POST":
        #update database and refresh webpage
        if request.form.get("Check") == "on":
            task.completed = 1
        else:     
            task.completed = 0
        try:
            db.session.commit()
            return redirect('/assignments')
        except:
            return "there was a problem updating that task"

@assignment_page.route('/assignments', methods = ["GET"])
def index():
    completed = request.args.get('completed', 'all')
    if completed == 'not_completed':
        assignments = AssignmentTracker.query.filter_by(completed=False).all()
    elif completed == 'completed':
        assignments = AssignmentTracker.query.filter_by(completed=True).all()
    else:
        assignments = AssignmentTracker.query.order_by(AssignmentTracker.due_date).all()
    #render the webpage with existing assignments showing 
    return render_template('Assignments/home.html', AssignmentTracker=assignments, completed=completed)
