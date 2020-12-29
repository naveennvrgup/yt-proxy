virtualenv env -p=python3 
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py shell < load-database.py
python manage.py runserver 0.0.0.0:5556
