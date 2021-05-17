# -*- coding: utf-8 -*-

from flask import Flask as f
from flask_sqlalchemy import SQLAlchemy
from executive.app_info import app

db = SQLAlchemy(app)

class Project(db.Model):
   project_id = db.Column('id', db.Integer, primary_key = True)
   name = db.Column('name', db.String(100))
   parent = db.Column(db.ForeignKey(project_id))
   
class Action(db.Model):
    action_id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(100))
    deadline = db.Column('deadline', db.DateTime)
    project = db.Column('project', db.ForeignKey(Project.project_id), nullable=True)
    completed = db.Column('completed', db.Boolean, default=False)
    context = db.Column('context', db.String(100), nullable=True)

class ScheduledAction(db.Model):
    scheduledaction_id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(100))
    cron = db.Column('cron', db.String(100))
    lastcompleted = db.Column('lastcompleted', db.DateTime, nullable=True)
   
if __name__ == '__main__':
    db.create_all()