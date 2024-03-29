from flask import Blueprint

from src.Models.models import *
from datetime import datetime
from sqlalchemy import asc, desc

calendar_monthly_page = Blueprint('Calendar', __name__, template_folder="templates") #add routing functionality to assignment page

@calendar_monthly_page.route("/createEvent", methods = ["GET","POST"]) #create event and update the database accordingly
def createEvent():
    if request.method == "POST":
        title = request.form['eventTitle']
        date = request.form.get("eventDate")
        time = request.form.get("eventTime")
        dt = datetime.strptime(date + " " + time,"%Y-%m-%d %H:%M")
        location_of_event = request.form['eventLocation']
        endTime_of_event = request.form['eventEndTime']
        newEvent = Event(title = title, dateTime_of_event = dt, location_of_event = location_of_event, endTime_of_event = endTime_of_event)
        
        try:
            db.session.add(newEvent)
            db.session.commit()
            return redirect("/calendar")
            
        except:
            return "There was an issue adding your task"
    else:
        Events = Event.query.order_by(Event.dateTime_of_event).all()
        return render_template("Calendar/createEvent.html", Events=Events)

@calendar_monthly_page.route("/editEvent/<int:id>", methods = ["GET","POST"]) 
def editEvent(id):
    #edit events that exist in the calendar and update in the calendar; refresh
    task_to_update = Event.query.get_or_404(id)
    if request.method == "POST":
        task_to_update.title = request.form['eventTitle']
        date = request.form.get("eventDate")
        time = request.form.get("eventTime")[:5]
        dt = datetime.strptime(date + " " + time,"%Y-%m-%d %H:%M")
        task_to_update.dateTime_of_event = dt
        task_to_update.location_of_event = request.form['eventLocation']

        try:
            db.session.commit()
            return redirect("/calendar")
        except:
            return "There was an issue updating your event"

    else:
        task_to_update = Event.query.get_or_404(id)
        return render_template("Calendar/editEvent.html",task_to_update = task_to_update)
        
@calendar_monthly_page.route("/deleteEvent/<int:id>", methods = ["POST"])
def deleteEvent(id):
    #delete the event from the calendar and refresh accordingly
    task_to_delete = Event.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/calendar')
    except:
        return "there was a problem deleting that task"
        
@calendar_monthly_page.route('/calendar', methods = ["GET"])
def index():
    #refresh the webpage with existing events
    Events = Event.query.order_by(asc(Event.dateTime_of_event)).all()
    return render_template("Calendar/CalendarMonthly.html", Events = Events)
