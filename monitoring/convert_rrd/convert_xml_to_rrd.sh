#!/bin/bash
for j in $(ls -d */)
do
        cd $j
        echo $j
        for i in $(ls *.xml)
        do
                RRD=$(echo $i | sed s/\.xml/\.rrd/)
                rrdtool restore $i $RRD
        done
        cd ..
done 
