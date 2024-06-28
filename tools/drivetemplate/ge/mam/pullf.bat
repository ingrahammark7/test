set ANDROID_SERIAL=%1
set pat=%2
REM save path
set p2=%3
REM device
set p3=%4
REM working file
set p4=%5
REM external drive base dir
set p5=%6
REM external drive letter
set p6=%7
REM drive direc
set ff1=%p3%%ANDROID_SERIAL%.txt
if exist "%ff1%" del "%ff1%"
%p5%
cd %p4%
cd %p6%
adb pull %pat%
adb shell rm -r %pat%
exit