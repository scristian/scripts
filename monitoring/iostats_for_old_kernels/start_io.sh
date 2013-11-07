dmesg -c
pkill klogd
echo 1 > /proc/sys/vm/block_dump
while true; do sleep 1; dmesg -c; done | perl iodump

