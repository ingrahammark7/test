set ANDROID_SERIAL=%1
set pat=%2
set p2=%3
set ff1=c:/games/%ANDROID_SERIAL%.txt
if exist "%ff1%" del "%ff1%"
adb shell lsof > %ff1%
exit