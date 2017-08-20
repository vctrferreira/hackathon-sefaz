# README #


### What is this repository for? ###

* This is the API service to Participa - Iceberg Team based python 3.5.3 with django 1.11
* Version 0.1

### How do I get set up? ###

* Clone this repositore
* Run 'pip freeze -r pip-freeze.txt' to install python deps
* Dependencies DB is Postgres and Redis
* Database configuration in settings.py
* Run tests with command 'python manage.py test'
* Development:
	** Run traditionl django manager with 'python manager.py runserver'
* Deployment: 
	- Change django settings debug to false
	- Run in gunicorn server
	- Run celery with nohup 'nohup celery -A participa worker -l info &'


### Contribution guidelines ###

* Tests coverage minimum 90% of application
