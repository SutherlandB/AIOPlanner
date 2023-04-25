from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy() #global database that each function can use


class Todo(db.Model): #class for Todo tasks
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))

    def __repr__(self):
        return '<Task %r>' % self.id
    
class Event(db.Model): #class for events
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    dateTime_of_event = db.Column(db.DateTime, default = datetime.utcnow)
    location_of_event = db.Column(db.String(200), nullable = False)
    endTime_of_event = db.Column(db.String(200), nullable = False)
    def __repr__(self):
        return '<Event %r>' % self.id

class AssignmentTracker(db.Model): #class for AssignmentTracker
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    course = db.Column(db.Text)
    due_date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Assignment %r>' % self.id

class List(db.Model): #class for List 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    To_do_Entry = db.Relationship('Todo', backref='List')
    
    def __repr__(self):
        return f'<List "{self.content[:20]}...">'