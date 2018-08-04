cd C:\TestFramework\workspace\Project_Basics\src\tests
SET PATH=%PATH%;%PYTHONPATH%;

@echo off
echo. ##################### PRUEBAS #####################


C:\TestFramework\python36\python.exe -m pytest tst_001.py --alluredir ..\allure-results

pause