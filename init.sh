DISPLAY=:0.0 lxterminal -e "python photobooth.py" &
DISPLAY=:0.0 matchbox-keyboard photobooth &
sleep 1
DISPLAY=:0.0 wmctrl -r "LXTerminal" -e 0,0,0,800,300
DISPLAY=:0.0 wmctrl -r "Keyboard" -e 0,0,250,800,300

