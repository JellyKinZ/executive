"""
Created on Mon May 17 10:01:18 2021

@author: jelle
"""

from executive.app_info import app, db
from executive.actions.models_f import Project
from flask import render_template, request, redirect, url_for, flash

@app.route('/')
def home():
    return render_template('index.html', projects = Project.query.all())

@app.route('/addproject', methods = ['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter a valid name.', 'error')
        projects = Project.query.all()
        if request.form['name'] in [x.name for x in projects]:
            flash('This project name already exists.', 'error')
        if request.form['parent'] not in [str(x.project_id) for x in projects]:
            flash('Please enter a valid parent project name.', 'error')
        else:
            project = (Project(request.form['name'], request.form['parent']) 
                       if request.form['parent'] else Project(request.form['name'], None))
            db.session.add(project)
            db.session.commit()
            flash('Project was successfully added')
            return redirect(url_for('home'))
    return render_template('add_project.html', projects = Project.query.all())

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)