@echo off
echo Building SANS Timer executable...
echo.

REM Check if PyInstaller is installed
pip show pyinstaller > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller is not installed. Installing now...
    pip install pyinstaller
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install PyInstaller. Please install it manually with:
        echo pip install pyinstaller
        pause
        exit /b 1
    )
)

REM Delete and recreate the icon
echo Generating digital timer icon...
if exist "timer_icon.ico" (
    echo Removing existing icon...
    del /f timer_icon.ico
)
echo Creating new icon...
python create_icon.py
if not exist "timer_icon.ico" (
    echo WARNING: Could not create icon file. The executable will use the default icon.
) else (
    echo Icon created successfully.
)

REM Check if the executable is running and terminate it
echo Checking if SANS_Timer.exe is running...
tasklist /FI "IMAGENAME eq SANS_Timer.exe" 2>NUL | find /I /N "SANS_Timer.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo SANS_Timer.exe is running. Attempting to terminate it...
    taskkill /F /IM SANS_Timer.exe
    if "%ERRORLEVEL%"=="0" (
        echo Successfully terminated SANS_Timer.exe.
    ) else (
        echo WARNING: Failed to terminate SANS_Timer.exe. 
        echo Please close the application manually before continuing.
        pause
    )
)

REM Delete existing build and dist directories if they exist
echo Cleaning up previous build files...
if exist "build" (
    echo Removing build directory...
    rd /s /q build
    
    REM Verify build directory was deleted
    if exist "build" (
        echo ERROR: Failed to delete build directory. Please check permissions and try again.
        pause
        exit /b 1
    )
)

if exist "dist" (
    echo Removing dist directory...
    rd /s /q dist
    
    REM Verify dist directory was deleted
    if exist "dist" (
        echo ERROR: Failed to delete dist directory. Please check permissions and try again.
        echo This may be because the executable is still running.
        pause
        exit /b 1
    )
)
echo Cleanup complete.
echo.

REM Generate a simple spec file
echo Generating spec file...
python simple_spec.py

REM Build the executable
echo Building executable...
pyinstaller --clean simple.spec

echo.
if %ERRORLEVEL% EQU 0 (
    echo Build successful! The executable is located in the dist folder.
    echo You can run SANS_Timer.exe from there.
) else (
    echo Build failed. Please check the error messages above.
)

pause 