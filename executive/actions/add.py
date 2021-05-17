from executive.actions.models import Action, Project
from datetime import date
from time import strptime

class AddAction(object):
    options = [
        'name', 'deadline', 'project', 'context']
    def run(self):
        options = self._getoptions()
        self._add(options)

    def _getoptions(self):
        options = {}
        for option in self.options:
            options[option] = input("{option}? \n > ".format(**locals())).strip()
        if 'project' in options.keys():
            if options['project']:
                options['project'] = Project[options['project']]
            else:
                options['project'] = None
        return options

    def _add(self, options):
        action = Action(**options) 
        action.save()

if __name__ == "__main__":
    AddAction().run()














