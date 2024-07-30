:x
set FOO=%TIME:~6,2%%TIME:~3,2%%TIME:~1,1%%DATE:~4,2%%DATE:~7,2%%DATE:~10,2%
del lsof.txt
adb shell lsof > lsof.txt
find /c "mov1" lsof.txt >NUL
if %errorlevel% equ 1 goto notfound
echo found
goto done
:notfound
echo notfound
adb pull sdcard/download/mov1 e:/ge/garb/smalll5345/%FOO%/ && adb shell rm -r sdcard/download/mov1
adb shell mkdir sdcard/download/mov1
del lsof.txt
goto done
:done
cd e:/ge/garb/smalll5345/
for /f "delims=" %%i in ('dir /b /ad') do rd "%%i"
cd "%%i"
for /f "delims=" %%i in ('dir /b /ad') do rd "%%i"
cd e:/ge/garb/
timeout /t 30
goto x