#!/bin/bash

MEMCACHEDPID=$(ps aux | grep 'memcached' | head -1 | cut -d " " -f 2)

#for old kernels - deprecated now
#echo -17 > /proc/$MEMCACHEDPID/oom_adj

#for newer kernels
echo -1000 > /proc/$MEMCACHEDPID/oom_score_adj

