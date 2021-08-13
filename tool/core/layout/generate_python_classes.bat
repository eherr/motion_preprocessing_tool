@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
for /r %%f in (.\*.ui) do (
	set file=%%f
	set outfile=!file:~0,-3!_ui
	echo !outfile!
	pyside2-uic %%f -o "!outfile!.py"
)
