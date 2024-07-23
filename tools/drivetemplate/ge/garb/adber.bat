
set FOO=%TIME:~6,2%%TIME:~3,2%%TIME:~1,1%%DATE:~4,2%%DATE:~7,2%%DATE:~10,2%
mkdir e:\ge\garb\smalll5345\%FOO%
del s.txt
adb shell ls sdcard/DCIM/Screenshots > s.txt
for /F "tokens=*" %%A in (s.txt) do (
adb pull sdcard/DCIM/Screenshots/"%%A" e:\ge\garb\smalll5345\%FOO%\ && adb shell rm -r sdcard/DCIM/Screenshots/'%%A'
)
adb pull sdcard/DCIM/Screenshots e:\ge\garb\smalll5345\%FOO%\ && adb shell rm -r sdcard/DCIM/Screenshots
del s.txt
rd /s /q e:\ge\garb\smalll5345\%FOO%\.tmp
rd /s /q e:\ge\garb\smalll5345\%FOO%\.adblocker_1dm
adb shell ls sdcard/Download/ > s.txt
for /F "tokens=*" %%A in (s.txt) do ( 
adb pull sdcard/Download/"%%A" e:\ge\garb\smalll5345\%FOO%\ && adb shell rm -r sdcard/Download/'%%A'
)
adb pull sdcard/Download  e:\ge\garb\smalll5345\%FOO%\ && adb shell rm -r sdcard/Download/
del s.txt
