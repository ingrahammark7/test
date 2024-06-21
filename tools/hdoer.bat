set ANDROID_SERIAL=R5CW72XTACH
set FOO=%TIME:~6,2%%TIME:~3,2%%TIME:~1,1%%DATE:~4,2%%DATE:~7,2%%DATE:~10,2%
adb pull sdcard/DCIM/Screenshots e:\ge\garb\smalll5345\%FOO%\
rd /s /q e:\ge\garb\smalll5345\%FOO%\.tmp
rd /s /q e:\ge\garb\smalll5345\%FOO%\.adblocker_1dm
adb pull sdcard/Download e:\ge\garb\smalll5345\%TIME:~6,2%%TIME:~3,2%%TIME:~1,1%%DATE:~4,2%%DATE:~7,2%%DATE:~10,2%
adb shell rm -f -rR -v sdcard/Download/*
adb shell rm -f -rR -v sdcard/DCIM/Screenshots/*

