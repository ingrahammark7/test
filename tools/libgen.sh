export torr='/data/data/com.termux/files/home/storage/shared/dcim'
cd "$torr"
rm f.txt
rm files.txt
ls -d */ > f.txt;
sed 's/.$//' f.txt > f1.txt;
mv f1.txt f.txt;
for foo in $(cat f.txt); do
cd "${torr}/${foo}";
export co=$(find . -type f | wc -l);
echo "$co"
if [ "$co" -ge 1000 ];
then
(
cd "$torr";
echo "$foo" >> "${torr}"/files.txt;
)
else
echo foo
fi
done;
cd "${torr}";
for foo in $(cat files.txt); do
mv "$foo" ~/storage/downloads/
done;
