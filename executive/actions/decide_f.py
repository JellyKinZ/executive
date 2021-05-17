"""The script of greatness!"""

from executive.actions.models_f import Action, ScheduledAction, Project
from executive.app_info import db
from executive.tools.cron import CronHandler
from datetime import datetime, date, timedelta
import pytz
import re

class DecisionMaker(object):
    def run(self):
        action = self._maintenanceaction() or self._timedaction() or self._nextaction()
        decision = self._printout(action)
        return decision

    def _maintenanceaction(self):
        empty_project = self._empty_project()
        if len(Project.query.all()) == 0:
            return self.__newprojectaction()
        elif empty_project:
            return self.__fillprojectaction(empty_project)

    def __newprojectaction(self):        
        return self._new(
            "Add a first project using 'ex addproject (name) [parent id]'",
            datetime.today())

    def __fillprojectaction(self, project):
        lastcompletednotice = ""
        lastdone = Action.query.filter(Action.project_id==project.id, Action.completed == True).order_by(Action.deadline.desc())
        if lastdone:
            lastcompletednotice += "\nlast completed action: {lastdone[0].name} at {lastdone[0].deadline}".format(**locals())
        return self._new(
            "Add an action to project {project.id}: {project.name}".format(**locals()) + lastcompletednotice,
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
        actions = Action.query.all().where(Action.completed == False)
        nextaction = actions[0] 
        for a in actions:
            if a.deadline < nextaction.deadline:
                nextaction = a
        return nextaction

    def _new(self, name, deadline, project = None):
        nextaction = Action(
            name = name,
            deadline = deadline,
            project = project)
        nextaction.save()
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
            decision = "[{action.scheduledaction_id}]: {action.timeenabled}: {action.name}".format(**locals())
        else:
            upcoming = self._upcoming()
            if upcoming:
                decision = "Next scheduled action: {upcoming[1].name} at {upcoming[0]}".format(**locals())

        if _class == Action:
            if action.project_id:
                project_str = self._getparents(Project[action.project_id])
            else:
                project_str = ""
            decision = "{project_str} \n {action.id}: {action.deadline}: {action.name}".format(**locals())
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
            return list(sorted(_nexttimes))[0] #return the first time for action along with the action

    def _getparents(self, project):
        if not hasattr(project, 'parent_id') or not project.parent_id:
            return "> " + project.name
        else:
            parent = Project[project.parent_id]
            return self._getparents(parent) + "\n> " + project.name


if __name__ == "__main__":
    d = DecisionMaker()
    d.run()

