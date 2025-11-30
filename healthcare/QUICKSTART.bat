@echo off
REM Quick Start Script for Healthcare System Frontend (Windows)
REM Run this batch file to set up the frontend quickly

title Healthcare System - Modern Frontend - Quick Start

echo ================================================================================
echo          Healthcare System - Modern Frontend - Quick Start
echo ================================================================================
echo.

REM Check if in healthcare directory
if not exist "manage.py" (
    echo WARNING: Not in healthcare directory!
    echo Please navigate to the healthcare folder and run this script again.
    pause
    exit /b 1
)

echo [1/4] Running Django Migrations...
python manage.py migrate
if errorlevel 1 (
    echo WARNING: Migrations failed!
    pause
    exit /b 1
)
echo [DONE] Migrations complete
echo.

echo [2/4] Collecting Static Files...
python manage.py collectstatic --noinput
if errorlevel 1 (
    echo WARNING: Static collection failed!
    pause
    exit /b 1
)
echo [DONE] Static files collected
echo.

echo [3/4] Checking Django Setup...
python manage.py check
if errorlevel 1 (
    echo WARNING: Django check failed!
    pause
    exit /b 1
)
echo [DONE] Django check passed
echo.

echo [4/4] Verifying Frontend Files...
if exist "..\templates\base.html" (
    echo [OK] Frontend templates found
) else (
    echo [ERROR] Frontend templates not found!
    pause
    exit /b 1
)
if exist "..\static\css\style.css" (
    echo [OK] Frontend CSS found
) else (
    echo [ERROR] Frontend CSS not found!
    pause
    exit /b 1
)
echo.

echo ================================================================================
echo SETUP COMPLETE - Healthcare System is Ready!
echo ================================================================================
echo.
echo NEXT STEPS:
echo.
echo 1. Create a superuser (if not already created):
echo    python manage.py createsuperuser
echo.
echo 2. Start the development server:
echo    python manage.py runserver
echo.
echo 3. Open your browser and visit:
echo    http://127.0.0.1:8000/
echo.
echo DOCUMENTATION FILES:
echo   * FRONTEND_README.md - Complete feature documentation
echo   * FRONTEND_SETUP.md - Detailed setup instructions
echo   * FRONTEND_VERIFICATION.md - Testing checklist
echo   * IMPLEMENTATION_SUMMARY.md - Implementation overview
echo.
echo ================================================================================
echo.
pause
