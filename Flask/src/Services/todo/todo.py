from flask import Blueprint
from ..mod import *

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
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == "POST":
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
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        if request.form.get("Check") == "on":
            task.completed = 1
        else:

            task.completed = 0
        try:
            db.session.commit()
            return redirect('/dashboard')
        except:
            return "there was a problem updating that task"
