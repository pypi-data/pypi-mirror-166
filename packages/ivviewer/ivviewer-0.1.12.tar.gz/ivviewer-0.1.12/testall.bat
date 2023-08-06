@echo off
setlocal EnableDelayedExpansion
if exist venv rd /S /Q venv
python -m venv venv
venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\python -m pip install -r requirements.txt
echo --- Run all tests ---
for /D %%f in (ivviewer\*) do (
echo Test %%f
venv\Scripts\python _test.py %%f
)
pause