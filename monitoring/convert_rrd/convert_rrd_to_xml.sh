#!/bin/bash
for j in $(ls -d */)
do
        cd $j
        for i in $(ls *.rrd)
        do
                RRD=$(echo $i | sed s/\.rrd/\.xml/)
                rrdtool dump $i $RRD
        done
        cd ..
done 
