@echo off
title Family Finance Management Portal
cls
echo ========================================================
echo   HomeLedger - Family Finance Management Portal
echo ========================================================
echo.
echo Building project...
dotnet build
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Build failed. Please check errors above.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Starting web server at http://localhost:5000 ...
echo Press Ctrl+C in this window anytime to stop the server.
echo.
dotnet .\bin\Debug\net10.0\HomeLedgerApp.dll --urls "http://localhost:5000"
pause
