@echo off
set "INSTALL_DIR=%~dp0"
if "%~2"=="" (
    echo %1 > %TEMP%\diffpro_file1.txt
    echo File 1 selected: %1
) else (
    set /p file1=<%TEMP%\diffpro_file1.txt
    start "" "%INSTALL_DIR%DiffPro.exe" "%file1%" "%1"
)