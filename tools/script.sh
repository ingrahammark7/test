#!/bin/bash
rm todo.txt
rm lsof.txt
rm lis.txt
lsof>lsof.txt
ls . -I storage -I script.sh  >lis.txt
export fofo='lsof.txt'
filename='lis.txt'
for foo in $(cat lis.txt); do
if grep -Fq "$foo" lsof.txt 
then
echo foo
else
echo "$foo">>todo.txt
fi
done;
for foo in $(cat todo.txt); do
((tar -cf /data/data/com.termux/files/home/storage/downloads/"$foo".tar "$foo") || continue) && rm -r "$foo";
done;
