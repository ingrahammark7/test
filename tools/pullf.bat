set ANDROID_SERIAL=%1
set pat=%2
set p2=%3
set p3=%4
set p4=%5
set p5=%6
set ff1=%p3%%ANDROID_SERIAL%.txt
if exist "%ff1%" del "%ff1%"
cd %p5%
cd %p4%
adb pull %pat%
adb shell rm -r %pat%
exit