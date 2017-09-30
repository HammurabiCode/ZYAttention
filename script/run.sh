#/bin/bash

NAME="ZYAttention"    # Name of the application
SHELL_DIR=`dirname $0`
SHELL_DIR=`pwd`${SHELL_DIR:1}
DJANGODIR=${SHELL_DIR}"/../Proj"

USER=ubuntu                     # the user to run as
GROUP=ubuntu                     # the group to run as
NUM_WORKERS=2         # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=AttTest.settings # which settings file should Django use
DJANGO_WSGI_MODULE=AttTest.wsgi                 # WSGI module name
 
echo "Starting $NAME as `whoami`"
 
# Activate the virtual environment
cd $DJANGODIR
source ../venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
 
# Create the run directory if it doesn't exist
# RUNDIR=$(dirname $SOCKFILE)
# test -d $RUNDIR || mkdir -p $RUNDIR
 
# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $NUM_WORKERS \
    --user=$USER --group=$GROUP \
    --log-level=debug \
    --bind=0.0.0.0:8000
    # --bind=unix:$SOCKFILE
