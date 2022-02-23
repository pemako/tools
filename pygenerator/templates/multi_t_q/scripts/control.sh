#!/bin/bash

VERSION=__BUILD_VERSION__
export VERSION

CURRDIR=$(dirname "$0")
BASEDIR=$(
  cd "$CURRDIR"
  cd ..
  pwd
)
NAME="multi_t_q"
CMD="main.py"

if [ "$1" = "-d" ]; then
  shift
  EXECUTEDIR=$1
  shift
else
  EXECUTEDIR=$BASEDIR
fi

if [ ! -d "$EXECUTEDIR" ]; then
  echo "ERROR: $EXECUTEDIR is not a dir"
  exit
fi

if [ ! -d "$EXECUTEDIR"/logs ]; then
  mkdir "$EXECUTEDIR"/logs
fi

cd "$EXECUTEDIR"

PID_FILE="$EXECUTEDIR"/logs/"$NAME".pid

check_pid() {
  RETVAL=1
  if [ -f $PID_FILE ]; then
    PID=$(cat $PID_FILE)
    if [[ $(uname) == 'Darwin' ]]; then
      vmmap $PID &>/dev/null
    else
      ls /proc/$PID &>/dev/null
    fi
    if [ $? -eq 0 ]; then
      RETVAL=0
    fi
  fi
}

check_running() {
  PID=0
  RETVAL=0
  check_pid
  if [ $RETVAL -eq 0 ]; then
    echo "$NAME is running as $PID, we'll do nothing"
    exit
  fi
}

start() {
  check_running
  echo "starting $NAME ..."
  nohup "$BASEDIR"/"$NAME"/"$CMD" -d "$EXECUTEDIR" 2>"$EXECUTEDIR"/logs/"$NAME".err >"$EXECUTEDIR"/logs/"$NAME".out &
  PID=$!
  echo $PID >"$EXECUTEDIR"/logs/"$NAME".pid
  sleep 1
}

stop() {
  check_pid
  if [ $RETVAL -eq 0 ]; then
    echo "$NAME is running as $PID, stopping it..."
    kill -15 $PID
    sleep 1
    echo "done"
  else
    echo "$NAME is not running, do nothing"
  fi

  while true; do
    check_pid
    if [ $RETVAL -eq 0 ]; then
      echo "$NAME is running, waiting it's exit..."
      sleep 1
    else
      echo "$NAME is stopped safely, you can restart it now"
      break
    fi
  done

  if [ -f $PID_FILE ]; then
    rm $PID_FILE
  fi
}

status() {
  check_pid
  if [ $RETVAL -eq 0 ]; then
    echo "$NAME is running as $PID ..."
  else
    echo "$NAME is not running"
  fi
}

RETVAL=0
case "$1" in
start)
  start $@
  status
  ;;
stop)
  stop
  ;;
restart)
  stop
  start $@
  ;;
status)
  status
  ;;
*)
  echo "Version: $VERSION"
  echo "Usage: $0 [-d EXECUTION_PATH] {start|stop|restart|status}"
  RETVAL=1
  ;;
esac

exit $RETVAL
