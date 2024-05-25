#!/bin/bash
#Define Web Root Directory below.
WEB_ROOT=/root/judgewebsite

#Define Python Virtual Environment below.
VENV_ROOT=/data/judgewebsite/.venv

#PID File location.
PIDFILE=$WEB_ROOT/gunicorn/gunicorn.pid

# !!!  ATTENTION: Change Environment Setting Here  !!!
# !!! Use wrong environment file will cause failure !!!
# Non-production: gunicorn/qa.py && env/env_qa.sh
# PRODUCTION: gunicorn/prod.py && env/env_prod.sh
CONFIG_FILE=$WEB_ROOT/gunicorn/qa.py
source $WEB_ROOT/env/env_qa.sh

cd $WEB_ROOT

case "$1" in
start)
   echo starting gunicorn...
   $VENV_ROOT/bin/gunicorn -c $CONFIG_FILE
   ;;
stop)
   echo stopping gunicorn...
   if [ -e $PIDFILE ]; then
      /usr/bin/kill -TERM `cat $PIDFILE`
   else
      echo gunicorn is NOT running
   fi
   ;;
restart)
   echo restarting gunicorn...
   if [ -e $PIDFILE ]; then
      /usr/bin/kill -HUP `cat $PIDFILE`
   else
      echo gunicorn is NOT running
   fi
   ;;
status)
   if [ -e $PIDFILE ]; then
      echo gunicorn is running, pid=`cat $PIDFILE`
   else
      echo gunicorn is NOT running
      exit 1
   fi
   ;;
*)
   echo "Usage: $0 {start|stop|restart|status}"
esac

exit 0
