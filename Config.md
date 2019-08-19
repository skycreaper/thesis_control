## virtualenv
    pip install virtualenv
    virtualenv env3 --python=python3
    cd env3
    source bin/activate
    pip install Django==2.2

## Install
    Create db thesis_control

    python manage.py makemigrations users
    python manage.py makemigrations academic
    python manage.py migrate users
    python manage.py migrate academic

    python manage.py migrate
    
    python manage.py runserver

    python manage.py createsuperuser

## static template
    python manage.py collectstatic
