for i in $(seq 1 1000);
do
(tail -c 1G foof.tar >foof_split_$i && truncate -s -1G foof.tar;)
done
