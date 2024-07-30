while true;
do (
lab=$(date +%s)
tar czvf "$lab".tar * --remove-files
for i in $(seq 1 1000);
do
(tail -c 1G "$lab".tar >"$lab"_split.part$i.tar && truncate -s -1G "$lab".tar;)
mv "$lab"_split.part$i.tar ~/storage/shared/Download/
done
);
sleep 60;
done