
# Altered Datum API | Django Rest API App for React Blog App

This project is implementation for the following topics related to technologies used with Django

-Implemented Complete Auth Using Django Custom Auth Model.
    
1. Implemented custom Auth Model and its Manager
2. Implemented custom error View for customizing Templates
3. Login. SingUp, Logout, Account Views Implemented
4. In built views of PasswordChangeDoneView, PasswordChangeView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetView, PasswordResetCompleteView
5. Build Custom Templates for These Inbuilt Views

-Implemented Social Login using drf-social-oauth2, which combines normal auth and social auth 

1. you can integrate different social accounts with an already created normal account using simple email registration
2. manage your account and profile

-Implemented Crud Operations with Django Rest Framework 

1. crud operations for Blog Model over REST API
2. Build API Documentations using COREAPI (SWAGGER)

-Deployed on Heroku

1. Used Heroku Postgres 
2. Used AWS S3 Bucket for static and media files
## Tech Stack

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Glossary/HTML5)
[![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Javascript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)](https://www.javascript.com/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/docs/)
[![AWS](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)](https://www.heroku.com/)
[![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://www.github.com/)

## Demo

Backend Available at: https://django-project-api-crud-graphq.herokuapp.com/

FrontEnd Available at: https://react-materialui-complete.herokuapp.com/

Note: Both the projects are running on Free dynos of Heroku so Please makesure before accessing Frontend Project 
    awake the Backend by visiting the backend link


admin login details:--
email: admin@arpansahu.me
password: showmecode
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Installation

Installing Pre requisites

```bash
  pip install -r requirements.txt

```

Making Migrations and Migrating them.

```bash
  python manage.py makemigrations
  python manage.py migrate

```

Creating Super User

```bash
  python manage.py createsuperuser

```

Run Server
```bash
  python manage.py runserver

```

## Tech Stack

**Client:** HTML, Jinja, CSS, BootStrap, Jquery

**Server:** Django, Django Rest Framework, Gunicorn, GraphQL, Heroku


## Deployment on Heroku

Installing Heroku Cli from : https://devcenter.heroku.com/articles/heroku-cli
Create your account in Heroku.

Inside your project directory

Login Heroku CLI
```bash
  heroku login

```

Create Heroku App

```bash
  heroku create [app_name]

```

Push Heroku App
```
    git push heroku master
```

Configure Heroku App Env Variables
```bash
  heroku config:set GITHUB_USERNAME=joesmith

```
Configuring Django App for Heroku

Install whitenoise 
```
pip install whitenoise 
```

Include it in Middlewares.
```
MIDDLEWARE = [
    # ...
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ...
]
```

Create Procfile and include this code snippet in it.
```
release: ./release-tasks.sh
web: gunicorn djangoProject.wsgi
```

Create release-task.sh for running multilple commands in run: section of procfile
```
python manage.py makemigrations
python manage.py migrate
```

Make relase-task.sh executable
```
chmod +x release-tasks.sh 
```

## Documentation

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Glossary/HTML5)
[![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Javascript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)](https://www.javascript.com/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/docs/)
[![AWS](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)](https://www.heroku.com/)
[![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://www.github.com/)

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

SECRET_KEY=

DEBUG=

DB_HOST=

DB_NAME=

DB_USER=

DB_PASSWORD=

DB_PORT=

SMTP_SERVER=

SMTP_PORT=

SMTP_PASSWORD=

SMTP_EMAIL=

DOMAIN=

AWS_ACCESS_KEY_ID=

AWS_SECRET_ACCESS_KEY=

AWS_STORAGE_BUCKET_NAME=
