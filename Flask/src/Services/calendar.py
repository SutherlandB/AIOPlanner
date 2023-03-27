from flask import Blueprint

from src.Models.models import *
from datetime import datetime

CalendarMonthly_page = Blueprint('Calendar', __name__, template_folder="templates")

@CalendarMonthly_page.route("/createEvent", methods = ["GET","POST"])
def createEvent():
    if request.method == "POST":
        newEvent = Event()
        newEvent.title = request.form['eventTitle']
        date = request.form.get("eventDate")
        time = request.form.get("eventTime")

        dt = datetime.strptime(date + " " + time,"%Y-%m-%d %H:%M")
        
        newEvent.dateTime_of_event = dt
        newEvent.location_of_event = request.form['eventLocation']
        print(newEvent.title)
        print(newEvent.dateTime_of_event)

        try:
            db.session.add(newEvent)
            db.session.commit()
            return render_template("Calendar/CalendarMonthly.html")
            
        except:
            return "There was an issue adding your task"
    else:
        Events = Event.query.order_by(Event.dateTime_of_event).all()
        return render_template("Calendar/createEvent.html", Events=Events)
        
       
        
   
   

