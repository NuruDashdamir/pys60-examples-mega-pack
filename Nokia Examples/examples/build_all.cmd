@echo off

REM ---------
REM Build file for Python for Series 60 examples
REM ---------

del build /s /f /q
rmdir build\examples\extension_example
rmdir build\examples
rmdir build

mkdir build
mkdir build\examples

REM ADD EXAMPLE FILES HERE:
xcopy dumbfeedparser.py build\examples
xcopy rssreader.py build\examples 
xcopy simplebtconsole.py build\examples
xcopy SMS_example.py build\examples
xcopy Sports_diary.py build\examples
xcopy weather_info.py build\examples
xcopy weather_maps.py build\examples
xcopy applicationskeleton.py build\examples
xcopy ..\..\python-port-s60\scripts\default.py build\examples
xcopy ..\..\python-port-s60\scripts\filebrowser.py build\examples
xcopy ..\snake\snake.py build\examples
xcopy ..\tests\keyviewer.py build\examples
xcopy ..\tests\ball.py build\examples
xcopy ..\imgviewer\imgviewer.py build\examples
xcopy ..\..\python-ext-s60\calendar\test_calendar.py build\examples
xcopy ..\..\python-ext-s60\contacts\test_contacts.py build\examples
xcopy ..\..\python-ext-s60\example build\examples\extension_example /i /s /e
xcopy ..\..\python-app-s60\fileserver build\examples\fileserver /i /s /e

cd build

call zip -R Examples.zip *