modprobe can
dmesg | grep -i vcan
/sbin/ip link set $1 up type can bitrate $2
ifconfig | grep $1
insmod $3
dmesg | grep -i isotp