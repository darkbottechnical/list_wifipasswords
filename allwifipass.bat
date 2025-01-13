@echo off

for /f "tokens=2delims=:" %%a in ('netsh wlan show profile ^|findstr ":"') do (
    set "ssid=%%~a"
    call :getpwd "%%ssid:~1%%"
)
:getpwd
set "ssid=%*"
for /f "tokens=2delims=:" %%b in ('netsh wlan show profile name^="%ssid:"=%" key^=clear ^| findstr /C:"Key Content"') do (
    echo SSID: %ssid% PASS: %%b
)