from executive.app_info import db

class Project(db.Model):
   project_id = db.Column('id', db.Integer, primary_key = True)
   name = db.Column('name', db.String(100))
   parent = db.Column('parent_id', db.ForeignKey(project_id))
   
   def __init__(self, name, parent):
       self.name = name
       self.parent = parent
   
class Action(db.Model):
    action_id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(100))
    deadline = db.Column('deadline', db.DateTime)
    project = db.Column('project_id', db.ForeignKey(Project.project_id), nullable=True)
    completed = db.Column('completed', db.Boolean, default=False)
    context = db.Column('context', db.String(100), nullable=True)
    
    def __init__(self, name, deadline, project, completed, context):
       self.name = name
       self.deadline = deadline
       self.project = project
       self.completed = completed
       self.context = context

class ScheduledAction(db.Model):
    __tablename__ = 'scheduledaction'
    scheduledaction_id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(100))
    cron = db.Column('cron', db.String(100))
    lastcompleted = db.Column('lastcompleted', db.DateTime, nullable=True)
    
    def __init__(self, name, cron, lastcompleted):
       self.name = name
       self.cron = cron
       self.lastcompleted = lastcompleted
   
if __name__ == '__main__':
    db.create_all()