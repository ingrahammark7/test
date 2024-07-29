rm f4.txt
cd ~
ls *.mp4 *.m4a *.webm >f4.txt
while read foo; do
(mv "$foo" storage/downloads/mov1/);
done <f4.txt
rm f4.txt