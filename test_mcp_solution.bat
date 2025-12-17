@echo off
echo Quick MCP Test Suite (Windows Batch)
echo ========================================

echo.
echo [1] Health Checks...
curl -s http://localhost:8000/ 
echo.
curl -s http://localhost:8001/
echo.

echo [2] Basic Data...
echo Total consultants:
curl -s http://localhost:8000/konsulenter
echo.

echo [3] Core Functionality...
echo.
echo All consultants:
curl -s "http://localhost:8001/tilgjengelige-konsulenter/sammendrag"
echo.

echo 60%+ availability:
curl -s "http://localhost:8001/tilgjengelige-konsulenter/sammendrag?min_tilgjengelighet_prosent=60"
echo.

echo Python developers:
curl -s "http://localhost:8001/tilgjengelige-konsulenter/sammendrag?p%%C3%%A5krevd_ferdighet=python"
echo.

echo CRITICAL TEST - 60%+ Python developers (should be 3):
curl -s "http://localhost:8001/tilgjengelige-konsulenter/sammendrag?min_tilgjengelighet_prosent=60&p%%C3%%A5krevd_ferdighet=python"
echo.

echo Test complete!
pause