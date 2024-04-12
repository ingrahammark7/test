set ANDROID_SERIAL=%1
set pat=%2
set p2=%3
set ff1=%p2%
if exist "%ff1%" del "%ff1%"
adb shell ls %pat% > %ff1%
exit