set FOO=%TIME:~6,2%%TIME:~3,2%%TIME:~1,1%%DATE:~4,2%%DATE:~7,2%%DATE:~10,2%
adb pull sdcard/download/mov1 e:/ge/garb/smalll5345/%FOO%/ && adb shell rm -r sdcard/download/mov1
adb shell mkdir sdcard/download/mov1