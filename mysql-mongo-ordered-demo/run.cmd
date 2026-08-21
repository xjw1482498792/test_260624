@echo off
setlocal

set "JDK_HOME=%JAVA_HOME%"
if not defined JDK_HOME (
  for /f "tokens=2,*" %%A in ('reg query HKCU\Environment /v JAVA_HOME 2^>nul ^| findstr JAVA_HOME') do set "JDK_HOME=%%B"
)

if not exist "%JDK_HOME%\bin\javac.exe" (
  echo JDK not found. Check JAVA_HOME.
  exit /b 1
)

set "PROJECT_DIR=%~dp0"
if not exist "%PROJECT_DIR%out" mkdir "%PROJECT_DIR%out"

"%JDK_HOME%\bin\javac.exe" -encoding UTF-8 -source 1.8 -target 1.8 -d "%PROJECT_DIR%out" "%PROJECT_DIR%src\OrderedSyncDemo.java"
if errorlevel 1 exit /b 1

"%JDK_HOME%\bin\java.exe" -cp "%PROJECT_DIR%out" OrderedSyncDemo
if errorlevel 1 exit /b 1

endlocal
