# A simple Task Manager
Task Manager desinged to manage the task of departments within organiztion
## Quick Setup
### install the latest version of python 
#### run this command
```git clone https://github.com/Esmat-Farjad/task_manager.git```
### install virtual environment
```pip install virtualenv```
### create virtual environment
```virtualenv .venv(name_of_virtualenv)```
## Activate virtual environment
### for windows
```.venv\Scripts\activate```
### for Mac and linux
```source .venv\bin\activate```
### create superuser (admin)
```python manage.py createsuperuser```
### run migrations
```python manage.py migrate```
### run the project
```python manage.py runserver```
