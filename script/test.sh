#!/bin/bash

NAME="ZYAttention"    # Name of the application
DJANGODIR=`pwd`   #Django project directory
DJANGODIR=${DJANGODIR}"/"${NAME}

USER=ubuntu                     # the user to run as
GROUP=ubuntu                     # the group to run as
NUM_WORKERS=2         # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=AttTest.settings # which settings file should Django use
DJANGO_WSGI_MODULE=${NAME}.wsgi                 # WSGI module name
echo $DJANGO_WSGI_MODULE

SHELL_DIR=`dirname $0`
SHELL_DIR=`pwd`${SHELL_DIR:1}
echo $SHELL_DIR
