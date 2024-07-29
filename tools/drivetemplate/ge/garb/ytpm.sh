while true;
do (
rm f4.txt
cd /data/data/com.termux/files/home/
ls *.mp4 *.m4a *.webm >f4.txt
while read foo; do
(mv "$foo" storage/downloads/mov1/);
done <f4.txt
rm f4.txt
);
sleep 60;
done