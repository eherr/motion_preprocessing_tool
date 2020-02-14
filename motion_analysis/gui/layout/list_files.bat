@echo off 
for /r %%f in (.\*.ui) do (
	set b=%%f
	echo %%b%%
)
PAUSE