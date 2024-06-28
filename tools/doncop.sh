cd sdcard/dcim/
find . -xdev -type f | cut -d "/" -f 2 | sort | uniq -c | sort -n