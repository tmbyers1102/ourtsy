1. download or fork project from github onto desktop
2. open project in text editor and make sure you are on the project's level
3. create a venv for the project (python -m venv venv)
4. activate venv (source venv/bin/activate)
5. download dependancies (pip install -r requirements.txt)
6. run initial migration (python manage.py migrate)
7. create the superuser if you'll need to get into admin (python manage.py createsuperuser)
8. finally! run server (python manage.py runserver)




* none of the database items are there but the tables exist and the media files are existent in the folder structure so you could make the items again.
