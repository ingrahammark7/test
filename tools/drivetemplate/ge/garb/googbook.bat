set FOOBAR=%TIME:~6,2%%TIME:~3,2%%TIME:~1,1%%DATE:~4,2%%DATE:~7,2%%DATE:~10,2%
mkdir .\crawls\%FOOBAR%
move *_*_*.pdf crawls\%FOOBAR%\