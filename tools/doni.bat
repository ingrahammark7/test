del temp.txt
adb shell < doncop.sh > temp.txt
For /f "eol=; delims=," %%i in (temp.txt) do (
set a=%%i
set "b=%a:~3,4%"
echo %b%
echo %a:~8,6%
)
For /f "eol=; delims=," %%i in (temp.txt) do (
set a=%%i
set "b=%a:~3,4%"
echo %b%
echo %a:~8,6%
if %b%==1000 (
e:
cd e:/ge/garb/smalll5345/
mkdir fail1
cd fail1
adb pull sdcard/dcim/%a:~8,6%
adb shell rm -r sdcard/dcim/%a:~8,6%
)
)
del temp.txt