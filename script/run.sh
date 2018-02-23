#!/bin/sh
# kill -HUP 15073
NAME="ZY-02"
DJANGODIR=~/Project/ZY-02-Attention/AttProj # Django project directory
NUM_WORKERS=1 # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=AttProj.settings # which settings file should Django use
DJANGO_WSGI_MODULE=AttProj.wsgi # WSGI module name
 
echo "Starting $NAME as `whoami`"
 
# Activate the virtual environment
cd $DJANGODIR
. ../venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
 
 
# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--bind=0.0.0.0:8082 \
--log-file=-

# cd DataServer
# gunicorn -w1 -b0.0.0.0:8080 DataServer.wsgi

