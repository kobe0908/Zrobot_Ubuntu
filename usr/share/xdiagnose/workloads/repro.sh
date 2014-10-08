#!/bin/bash

INFO=$(wmctrl -d)
WORKAREA_WIDTH=$(echo "${INFO}"| awk '{sub(/x[0-9]+/, "", $9); print $9}')
WORKAREA_HEIGHT=$(echo "${INFO}"| awk '{sub(/[0-9]+x/, "", $9); print $9}')
FULLSCREEN=${WORKAREA_WIDTH}x${WORKAREA_HEIGHT}

XVT=$(sudo fgconsole)

chws() {
	wmctrl -o $(($WORKAREA_WIDTH * $1)),0
}

#for x in `seq 1 3`; do
#	echo "System will suspend now.  Please wake it up again."
#	sudo pm-suspend
#	sleep 5
#done

chws 0
for x in `seq 1 10`; do
gnome-terminal &
done

sleep 5

chws 1
glxgears -geometry $FULLSCREEN >/dev/null &
glxgears >/dev/null &

sleep 5

chws 2
gnome-terminal --geometry=$FULLSCREEN &

sleep 5

chws 3
totem $(perl -e 'print "/usr/share/example-content/Ubuntu_Free_Culture_Showcase/SpiritOfUbuntu.ogv " x 30;') &

sleep 5

while true; do
	chws 4
	chws 0
done
