set ANDROID_SERIAL=R5CTB2C1LJA
set FOO=%TIME:~6,2%%TIME:~3,2%%TIME:~1,1%%DATE:~4,2%%DATE:~7,2%%DATE:~10,2%
adb pull storage/sdcard0/DCIM/Screenshots e:\ge\garb\smalll5345\%FOO%\
rd /s /q e:\ge\garb\smalll5345\%FOO%\.tmp
rd /s /q e:\ge\garb\smalll5345\%FOO%\.adblocker_1dm
adb shell ls sdcard/Download/ > s.txt
for /F "tokens=*" %%A in (s.txt) do ( 
adb pull sdcard/Download/%%A && adb shell rm -r sdcard/Download/%%A
)
adb pull storage/sdcard0/Download e:\ge\garb\smalll5345\%TIME:~6,2%%TIME:~3,2%%TIME:~1,1%%DATE:~4,2%%DATE:~7,2%%DATE:~10,2%
del s.txt
