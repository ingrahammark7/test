termux-setup-storage
rm todo.txt
lsof>lsof.txt
list=`ls`
for foo in $list
do
if grep -Fxq "$foo" lsof.txt
then
echo not
else
"$foo">>todo.txt
done
todo=`cat todo.txt`
for file in todo;
do
cp -fr "$file" storage/shared/documents/ && rm -r "$file";
done