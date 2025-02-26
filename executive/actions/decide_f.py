"""The script of greatness!"""

from executive.actions.models_f import Project, Action, ScheduledAction
from executive.app_info import db
from executive.tools.cron import CronHandler
from datetime import datetime
import pytz

class DecisionMaker(object):
    def run(self):
        action = self._maintenanceaction() or self._timedaction() or self._nextaction()
        decision = self._printout(action)
        return decision

    def _maintenanceaction(self):
        empty_project = self._empty_project()
        existing_projects = Project.query.all()
        existing_actions = Action.query.filter(Action.name == "Add a first project").all()
        if len(existing_projects) == 0:
            if len(existing_actions) > 0:
                return None
            return self.__newprojectaction()
        elif empty_project:
            return self.__fillprojectaction(empty_project)

    def __newprojectaction(self):        
        return self._new(
            "Add a first project",
            datetime.today())

    def __fillprojectaction(self, project):
        lastcompletednotice = ""
        lastdone = Action.query.filter(Action.project==project.project_id,
                                        Action.completed == True).order_by(Action.deadline.desc()).first()
        if lastdone:
            lastcompletednotice += "\nLast completed action: {lastdone.name} at ".format(**locals()) + datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        return self._new(
            "Add an action to project {project.project_id}: {project.name}".format(**locals()) + lastcompletednotice,
            datetime.today(),
            project = project
            )        

    def _timedaction(self):
        actions = ScheduledAction.query.all()
        for action in actions:
            cron = CronHandler(action.cron)
            lastenabled = cron.lastenabled()
            if not lastenabled:
                return None
            else:
                action.timeenabled = datetime(lastenabled.year,
                                              lastenabled.month,
                                              lastenabled.day,
                                              lastenabled.hour,
                                              lastenabled.minute)
            if action.lastcompleted:
                lastcompleted = action.lastcompleted.astimezone(pytz.timezone('Europe/Amsterdam'))
            else:
                return action
            if lastcompleted < lastenabled:
                return action

    def _nextaction(self):
        actions = Action.query.filter(Action.completed == False).all()
        nextaction = actions[0] 
        for a in actions:
            if a.deadline < nextaction.deadline:
                nextaction = a
        return nextaction

    def _new(self, name, deadline, project = None):
        nextaction = (Action(
            name = name,
            deadline = deadline,
            completed = False,
            project = project.project_id,
            context = "None") if project else Action(
                name = name,
                deadline = deadline,
                completed = False,
                project = None,
                context = "None"))
        db.session.add(nextaction)
        db.session.commit()
        return nextaction

    def _empty_project(self):
        for p in Project.query.all():
            if Action.query.filter(Action.project == p.project_id, Action.completed == False).count() == 0:
                if Project.query.filter(Project.parent == p.project_id).count() == 0:
                    return p
        return None

    def _printout(self, action):
        _class = action.__class__
        if _class == ScheduledAction:
            decision = "Scheduled action [{action.scheduledaction_id}] \n Time: {action.timeenabled} \n Name: {action.name}".format(**locals())
        else:
            upcoming = self._upcoming()
            if upcoming:
                decision = "Next scheduled action: {upcoming[1].name} at {upcoming[0]}".format(**locals())

        if _class == Action:
            if action.project and action.project != "None":
                project_str = self._getparents(Project.query.filter(Project.project_id == action.project).first())
            else:
                project_str = "None"
            decision = "Task ID: {action.action_id} \n Deadline: {action.deadline} \n Name: {action.name} \n Project: {project_str}".format(**locals())
        print(decision)
        return decision

    def _upcoming(self):
        """What timed action is next up?"""
        actions = ScheduledAction.query.all()
        _nexttimes = []
        for a in actions:
            _next = CronHandler(a.cron).nextenabled()
            if _next:
                _nexttimes.append((_next, a))
        if _nexttimes:
            #return the first time for action along with the action
            return list(sorted(_nexttimes, key = lambda x: x[0]))[0] 
           
    def _getparents(self, project):
        if not project.parent or project.parent == "None":
            return "> " + project.name
        else:
            parent = Project.query.filter(Project.project_id == project.parent).first()
            return self._getparents(parent) + "\n> " + project.name


if __name__ == "__main__":
    d = DecisionMaker()
    d.run()

