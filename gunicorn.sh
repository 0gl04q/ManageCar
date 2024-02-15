#!/bin/bash
source /var/www/ManageCar/env/bin/activate
exec gunicorn -c "/var/www/ManageCar/ManageCar/gunicorn_config.py" ManageCar.wsgi