while true;
do (
lab=$(date +%s)
tar czvf "$lab".tar * --remove-files
for i in $(seq 1 1000);
do
(tail -c 1G "$lab".tar >"$lab"_split.part$i.tar && truncate -s -1G "$lab".tar;)
mkdir /storage/emulated/0/Download
mv "$lab"_split.part$i.tar ~/storage/shared/Download/
find ~/storage/shared/Download -delete -maxdepth 1 -size 0c
mkdir /storage/emulated/0/Download
find * -delete -size 0c
done
);
sleep 60;
done