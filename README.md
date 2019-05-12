# Desafio GNK

### install lib psycopg2 to PostgreSQL
- pip install psycopg2
### Install Redis and Celery
- Redis (pip install redis)
- starting Redis: redis-server
- Celery (pip install celery)
- starting Celery: celery -A desafio_gnk worker --loglevel=info
### Heroku
- url: https://desafio-gnk.herokuapp.com
- user: admin
- pwd: admin@123
### Other installed libs. For more detail: requirements.txt in the root path
- amqp
- astroid
- autopep8
- billiard
- celery
- dj-database-url
- Django
- django-heroku
- django-searchable-select
- gunicorn
- isort
- kombu
- lazy-object-proxy
- mccabe
- psycopg2
- pycodestyle
- pylint
- pylint-django
- pylint-plugin-utils
- pytz
- redis
- six
- sqlparse
- typed-ast
- vine
- whitenoise
- wrapt