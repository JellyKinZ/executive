# -*- coding: utf-8 -*-
"""
Created on Mon May 17 10:01:18 2021

@author: jelle
"""

from executive.app_info import app
from executive.actions.models_f import Project

@app.route('/')
def home():
    projects = Project.query.all()
    project = projects[0]
    return "Top project: " + project.name
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)