modprobe vcan
dmesg | grep -i vcan
ip link add dev $1 type vcan
ip link set up $1
ifconfig | grep $1
insmod $2
dmesg | grep -i isotp