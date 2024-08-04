while true;
do (
rm f4.txt
cd /data/data/com.termux/files/home/
ls *.mp4 *.m4a *.webm *.mkv >f4.txt
while read foo; do
(mkdir /storage/emulated/0/Download
mv "$foo" storage/downloads/mov1/);
done <f4.txt
rm f4.txt
);
mv storage/downloads/all_cookies.txt .;
sleep 60;
done