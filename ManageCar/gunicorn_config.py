command = '/var/www/ManageCar/env/bin/gunicorn'
python_path = '/var/www/ManageCar/ManageCar'
bind = '0.0.0.0:8001'
workers = 5
user = 'www'
raw_env = 'DJANGO_SETTINGS_MODULE=ManageCar.settings'