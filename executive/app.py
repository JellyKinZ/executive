"""
Created on Mon May 17 10:01:18 2021

@author: jelle
"""

from executive.app_info import app, db
from executive.actions.models_f import Project, Action, ScheduledAction
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime

@app.route('/')
def home():
    return render_template('index.html', 
                           projects = Project.query.all(), 
                           actions = Action.query.all())

@app.route('/add_project', methods = ['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        # Invalidations
        if not request.form['name']:
            flash('Please enter a valid name.', 'error')
        projects = Project.query.all()
        if request.form['name'] in [x.name for x in projects]:
            flash('This project name already exists.', 'error')
        if request.form['parent'] not in [str(x.project_id) for x in projects]:
            flash('Please enter a valid parent project name.', 'error')
        else: # Add project to database
            project = (Project(request.form['name'], request.form['parent']) 
                       if request.form['parent'] else Project(request.form['name'], None))
            db.session.add(project)
            db.session.commit()
            flash('Project was successfully added')
            return redirect(url_for('home'))
    return render_template('add_project.html', projects = Project.query.all())

@app.route('/add_project_task', methods = ['GET', 'POST'])
def add_action():
    if request.method == 'POST':
        # Invalidations
        # Same name + deadline in same project should not be allowed?
        # Add action to database
        deadline_date = datetime(int(request.form['deadline'][:4]),
                                   int(request.form['deadline'][5:7]),
                                   int(request.form['deadline'][8:10]), 
                                   23, 59, 59)
        action = Action(request.form['name'], deadline_date,
                        request.form['project'], False, request.form['context'])
        db.session.add(action)
        db.session.commit()
        flash('Action was successfully added')
        return redirect(url_for('home'))
    return render_template('add_action.html', projects = Project.query.all())

@app.route('/add_scheduled_action', methods = ['GET', 'POST'])
def add_scheduled_action():
    if request.method == 'POST':
        # Invalidations
        # Same name + same exact cron should not be allowed?
        # Add action to database
        scheduled_action = ScheduledAction(request.form['name'], request.form['minute'], request.form['hour'],
                           request.form['day_of_month'], request.form['month'], request.form['weekday'], None)
        db.session.add(scheduled_action)
        db.session.commit()
        flash('Scheduled action was successfully added')
        return redirect(url_for('home'))
    return render_template('add_scheduled_action.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)