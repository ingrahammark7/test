:x
set FOO=%TIME:~6,2%%TIME:~3,2%%TIME:~1,1%%DATE:~4,2%%DATE:~7,2%%DATE:~10,2%
del lsof.txt
adb shell lsof > lsof.txt
mkdir e:\ge\garb\smalll5345\%FOO%
del s.txt
adb shell ls sdcard/Download/ > s.txt
for /F "tokens=*" %%A in (s.txt) do ( 
adb pull sdcard/Download/"%%A" e:\ge\garb\smalll5345\%FOO%\ && adb shell rm -r sdcard/Download/'%%A'
)
del s.txt
del lsof.txt
adb pull sdcard/Download/  e:\ge\garb\smalll5345\%FOO%\ && adb shell rm -r sdcard/Download/
e:
cd e:\ge\garb\smalll5345\%FOO%\
for /f "delims=" %%i in ('dir /b /ad') do rd "%%i"
cd e:\ge\garb
timeout /t 30
goto x
