set foobar=%TIME:~6,2%%TIME:~3,2%%TIME:~1,1%%DATE:~4,2%%DATE:~7,2%%DATE:~10,2%
if EXIST image.* tar -cf %FOOBAR%.image image.* 
del image.* 
if EXIST document.* tar -cf %FOOBAR%.document document.*
del document.*
if EXIST file.* tar -cf %FOOBAR%.file file.*
del file.*
if EXIST download.* tar -cf %FOOBAR%.down download.*
del download.*
if EXIST data.* tar -cf %FOOBAR%.data data.*
del data.*
if EXIST report.* tar -cf %FOOBAR%.report report.*
del report.*
if EXIST "Wayback Machine" tar -cf %FOOBAR%.way "Wayback Machine"
del "Wayback Machine"
if EXIST "Quora" tar -cf %FOOBAR%.quora "Quora"
del "Quora"
mkdir crawls\wayba%FOOBAR%
move *wayback* crawls\wayba%FOOBAR%
if EXIST main.* tar -cf %FOOBAR%.main main.*
del main.*
if EXIST full.* tar -cf %FOOBAR%.full full.*
del full.*
if EXIST master.* tar -cf %FOOBAR%.master master.*
del master.*
if EXIST chart.* tar -cf %FOOBAR%.chart chart.*
del chart.*




