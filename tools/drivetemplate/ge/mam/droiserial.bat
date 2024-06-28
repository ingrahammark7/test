setlocal disabledelayedexpansion
del temp1.txt
adb devices > temp.txt
For /f "delims=	" %%i in (temp.txt) do (
set ANDROID_SERIAL=%%i
)