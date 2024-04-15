#!/bin/bash
termux-setup-storage -y
rm todo.txt
rm lsof.txt
rm lis.txt
lsof>lsof.txt
ls .>lis.txt
export fofo='lsof.txt'
filename='lis.txt'
for foo in $(cat lis.txt); do
if grep -Fxq "$foo" lsof.txt 
then
echo foo
else
echo "$foo">>todo.txt
fi
done;
for foo in $(cat todo.txt); do
cp -rf "$foo" storage/shared/documents/ && rm -r "$foo";
done