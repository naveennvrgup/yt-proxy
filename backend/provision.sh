virtualenv env -p=python3 
pip install -r requirements.txt
source env/bin/activate
python manage.py migrate
python manage.py shell < load-database.py
python manage.py runserver 0.0.0.0:5556
