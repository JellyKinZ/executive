"""
Created on Mon May 17 10:01:18 2021

@author: jelle
"""

from executive.app_info import app, db
from executive.actions.decide_f import DecisionMaker
from executive.actions.models_f import Project, Action, ScheduledAction
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from pytz import timezone

@app.route('/')
def home():            
    d = DecisionMaker()
    decision = d.run()
    decision = decision.replace('\n', '<br/>')
    return render_template('index.html', 
                           projects = Project.query.all(), 
                           actions = Action.query.all(),
                           scheduled_actions = ScheduledAction.query.all(),
                           decision = decision)

@app.route('/add_project', methods = ['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        # Invalidations
        if not request.form['name']:
            flash('Please enter a valid name.', 'error')
            return render_template('add_project.html', projects = Project.query.all())
        projects = Project.query.all()
        if len(projects) > 0:
            if request.form['name'] in [x.name for x in projects]:
                flash('This project name already exists.', 'error')
                return render_template('add_project.html', projects = Project.query.all())
        # Add project to database
        project = (Project(request.form['name'], request.form['parent']) 
                   if request.form['parent'] else Project(request.form['name'], None))
        db.session.add(project)
        db.session.commit()
        flash('Project was successfully added.')
        return redirect(url_for('home'))
    return render_template('add_project.html', projects = Project.query.all())

@app.route('/add_task', methods = ['GET', 'POST'])
def add_action():
    if request.method == 'POST':
        deadline_date = datetime(int(request.form['deadline'][:4]),
                                 int(request.form['deadline'][5:7]),
                                 int(request.form['deadline'][8:10]),
                                 23, 59, 59)
        # Invalidations
        actions = Action.query.filter(Action.name == request.form['name'],
                                      Action.project == request.form['project'],
                                      Action.deadline == deadline_date).all()
        if len(actions) > 0:
            flash('This exact task already exists.', 'error')
            return render_template('add_action.html', projects = Project.query.all())
        # Add action to database
        action = (Action(request.form['name'], deadline_date,
                        request.form['project'], False, request.form['context']) 
                  if request.form['project'] != "None" else Action(request.form['name'], deadline_date,
                                                                   None, False, request.form['context']))
        db.session.add(action)
        db.session.commit()
        flash('Task was successfully added.')
        return redirect(url_for('home'))
    return render_template('add_action.html', projects = Project.query.all())

@app.route('/add_scheduled_action', methods = ['GET', 'POST'])
def add_scheduled_action():
    if request.method == 'POST':
        cron = str(request.form['minute'] + " " + request.form['hour'] 
                   + " " + request.form['day_of_month'] + " " + request.form['month'] 
                   + " " + request.form['weekday'] + " " + request.form['year'])
        # Invalidations
        scheduled_actions = ScheduledAction.query.filter(ScheduledAction.name == request.form['name'],
                                                         ScheduledAction.cron == cron).all()
        if len(scheduled_actions) > 0:
            flash('This exact scheduled action already exists.', 'error')
            return render_template('add_scheduled_action.html')
        # Add action to database
        scheduled_action = ScheduledAction(request.form['name'], cron, None)
        db.session.add(scheduled_action)
        db.session.commit()
        flash('Scheduled action was successfully added.')
        return redirect(url_for('home'))
    return render_template('add_scheduled_action.html')

@app.route('/finish_action', methods = ['GET', 'POST'])
def finish_action():
    if request.method == 'GET':
        projects = Project.query.all()
        project = request.args.get("Projects")
        if project and project != "None":
            project = int(project)
            actions = Action.query.filter(Action.project == str(project), Action.completed == False).all()
        else:
            actions = Action.query.filter(Action.project == None, Action.completed == False).all()
    if request.method == 'POST':
        action = Action.query.filter(Action.action_id == request.form['action']).first()
        action.completed = True
        db.session.merge(action)
        db.session.commit()
        flash('Action was successfully updated.')
        return redirect(url_for('home'))
    return render_template('finish_action.html', projects = projects, project = project, actions = actions)

@app.route('/finish_scheduled_action', methods = ['GET', 'POST'])
def finish_scheduled_action():
    if request.method == 'POST':
        scheduled_action = ScheduledAction.query.filter(ScheduledAction.scheduledaction_id 
                                                        == request.form['scheduled_action']).first()
        scheduled_action.lastcompleted = datetime.now(timezone('Europe/Amsterdam'))
        db.session.merge(scheduled_action)
        db.session.commit()
        flash('Scheduled action was successfully updated.')
        return redirect(url_for('home'))
    return render_template('finish_scheduled_action.html', scheduled_actions = ScheduledAction.query.all())

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)