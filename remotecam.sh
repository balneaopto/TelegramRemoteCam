#!/bin/bash
# Run an app as daemon / service
# Change the next 3 lines to suit where you install your script and what you want to call it
DAEMON=/usr/bin/python3
DAEMON_NAME=remotecam
# Add any command line options for your daemon here
ARGS="$HOME/remotecam/remotecam3x.py"
# This next line determines what user the script runs as.
# Root generally not recommended but necessary if you are using the Raspberry Pi GPIO from Python.
DAEMON_USER="$USER"
# The process ID of the script when it runs is stored here:
PIDFILE="$HOME/remotecam/$DAEMON_NAME.pid"
. /lib/lsb/init-functions
do_start () {
    log_daemon_msg "Starting system $DAEMON_NAME daemon"
    start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --chuid $DAEMON_USER --exec $DAEMON $ARGS
    #  no background option for test only
    #start-stop-daemon --start --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --chuid $DAEMON_USER --exec $DAEMON $ARGS
    log_end_msg $?
}
do_stop () {
    log_daemon_msg "Stopping system $DAEMON_NAME"
    start-stop-daemon --stop --pidfile $PIDFILE --retry 10
    log_end_msg $?
}

case "$1" in

    start|stop)
        do_${1}
        ;;

    restart|reload|force-reload)
        do_stop
        do_start
        ;;

    status)
        status_of_proc "$DAEMON_NAME" "$DAEMON" && exit 0 || exit $?
        ;;
    *)
        echo "Usage: /etc/init.d/$DAEMON_NAME {start|stop|restart|status}"
        exit 1
        ;;

esac
exit 0