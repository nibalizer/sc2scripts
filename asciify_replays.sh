#!/bin/bash

# shell script to ensure that all files have only ascii

dir=$1

if [ -z $dir ]; then
    echo "Please provide a target dir"
    exit 1
fi

mkdir ${dir}/asciid

save_IFS=$IFS

IFS='
'
for file in `find $dir`; do
    echo "$file"
    mv $file ${dir}/asciid/`date +%s-%N`.SC2Replay
done

IFS=$save_IFS
