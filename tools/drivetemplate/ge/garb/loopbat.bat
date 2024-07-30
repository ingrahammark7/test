:x
set FOO=%TIME:~6,2%%TIME:~3,2%%TIME:~1,1%%DATE:~4,2%%DATE:~7,2%%DATE:~10,2%
del lsof.txt
adb shell lsof > lsof.txt
mkdir e:\ge\garb\smalll5345\%FOO%
del s.txt
adb shell ls sdcard/Download/ > s.txt
for /F "tokens=*" %%A in (s.txt) do ( 
find /c %%A lsof.txt >NUL
if %errorlevel% equ 1 goto notfound
echo found
goto done
:notfound
echo notfound
adb pull sdcard/Download/"%%A" e:\ge\garb\smalll5345\%FOO%\ && adb shell rm -r sdcard/Download/'%%A'
:done
)
del s.txt
del lsof.txt
adb pull sdcard/Download  e:\ge\garb\smalll5345\%FOO%\ && adb shell rm -r sdcard/Download/
timeout /t 30
goto x
