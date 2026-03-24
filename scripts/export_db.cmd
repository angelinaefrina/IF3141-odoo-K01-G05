@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "PROJECT_DIR=%%~fI"
set "DUMP_DIR=%PROJECT_DIR%\dump"

docker compose version >nul 2>&1
if %errorlevel%==0 (
	set "DC=docker compose"
) else (
	docker-compose --version >nul 2>&1
	if %errorlevel%==0 (
		set "DC=docker-compose"
	) else (
		echo Error: neither "docker compose" nor "docker-compose" is available.
		exit /b 1
	)
)

set "OUT_FILE=%~1"
if "%OUT_FILE%"=="" (
	for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "TS=%%I"
	set "OUT_FILE=%DUMP_DIR%\odoo_backup_%TS%.dump"
)

pushd "%PROJECT_DIR%" || exit /b 1
if not exist "%DUMP_DIR%" mkdir "%DUMP_DIR%"

echo Starting db container...
%DC% up -d db || goto :error

echo Exporting database to: %OUT_FILE%
%DC% exec -T db pg_dump -U odoo -d postgres -Fc > "%OUT_FILE%" || goto :error

echo Done. Backup file: %OUT_FILE%
popd
exit /b 0

:error
echo Export failed.
popd
exit /b 1
