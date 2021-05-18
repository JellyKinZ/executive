executive
=========

Preserve your precious executive function with a web application incorporating a task system that decides for you.

**Installation**
=========

Install Python 3.8 or higher from here: https://www.python.org/downloads/

**Pull everything from Github**

`git clone https://github.com/JellyKinZ/executive /path/to/executive`

**Make sure your pythonpath contains the directory you just pulled**

unix: `export PYTHONPATH=/path/to/executive`

windows: `set export PYTHONPATH=/path/to/executive`

**Install dependencies**

`pip install pytz`
`pip install flask`
`pip install flask-sqlalchemy`

**on mac you may have some locale issues**

  `export LC_ALL=en_US.UTF-8`
  `export LANG=en_us.UTF-8`
  
**New Usage**
=========

```
$ python app.py (easier within Python IDE)

Open internet browser and go to: http://localhost:5000/
```

**Old Usage**
=========

```
$ python executive/actions/decide.py
 
 1: 2020-09-07: Add a first project using 'ex addproject (name) [parent id]'
$ python executive/actions/addproject.py demo
created project 1: demo
$ python executive/actions/decide.py
> demo 
 2: 2020-09-07: Add an action to project 1: demo
$ python executive/actions/add.py
name? 
 > demonstrate usage of executive
deadline? 
 > 2020-10-01
project? 
 > 1
context? 
 > 
$ python executive/actions/decide.py
 
 1: 2020-09-07: Add a first project using 'ex addproject (name) [parent id]'
$ python executive/actions/done.py 1
Well done!
Set action 'Add a first project using 'ex addproject (name) [parent id]'' to completed.
call decide.py for your next action
$ python executive/actions/decide.py
> demo 
 2: 2020-09-07: Add an action to project 1: demo
$ python executive/actions/done.py 2
Well done!
Set action 'Add an action to project 1: demo' to completed.
call decide.py for your next action
$ python executive/actions/decide.py
> demo 
 3: 2020-10-01: demonstrate usage of executive
$ python executive/actions/add.py
name? 
 > come up with some backlog items for executive
deadline? 
 > 2020-10-02
project? 
 > 1
context? 
 > 
$ python executive/actions/add.py
name? 
 > have someone do a test run of the installation instructions
deadline? 
 > 2020-10-03
project? 
 > 1
context? 
 > 
$ python executive/actions/decide.py
> demo 
 3: 2020-10-01: demonstrate usage of executive
$ python executive/actions/done.py 3
Well done!
Set action 'demonstrate usage of executive' to completed.
call decide.py for your next action
```



