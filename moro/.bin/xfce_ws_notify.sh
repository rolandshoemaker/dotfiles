#!/bin/bash

OIFS="${IFS}"
NIFS=$'\n'
IFS="${NIFS}"

cur_ws_num() {
	echo $( wmctrl -d | grep \* | cut -d' ' -f1 )
}

cur_ws_name() {
	local ws_num=$1
	local lines=0
	local ws_names=$(xfconf-query -c xfwm4 -p /general/workspace_names | tail -n +3)
	for LINE in ${ws_names}; do
		if [ "$lines" -eq "$ws_num" ]; then
			notify-send -t 900 WS "$LINE" --icon=utilities-terminal
			break
		fi
		lines=`expr $lines + 1`
	done
}

run_ws_checkr() {
	local current_ws=$( cur_ws_num )
	local now_ws

	while true; do
		sleep 0.5
		now_ws=$( cur_ws_num)
		if [ "$current_ws" -ne "$now_ws" ]; then
			current_ws=$now_ws
			cur_ws_name $current_ws
		fi
	done
}

do_lock() {
	local lockfile="/tmp/.xfce_ws_notify.$USER.lock"
	if ( set -o noclobber; echo "merpderp locked" > $lockfile ) 2> /dev/null; then
		trap 'rm -f "$lockfile"; exit $?' INT TERM EXIT
		run_ws_checkr
	else
		echo "xfce_ws_notify is already running/didn't quit cleanly"
	fi
}

do_lock

IFS="${OIFS}"
