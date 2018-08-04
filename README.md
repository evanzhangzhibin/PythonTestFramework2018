# PythonTestFrameWork2018
Este Framework Selenium Basado en Python, incluye Allure Framework 2, pillow, pytest y otras hierbas.

###############################################################
##################### VARIABLES DE ENTORNO #####################
###############################################################

ALLURE_SRC
C:\Program Files\Java\jdk1.8.0_111

PATH
%ALLURE_HOME%;C:\TestFramework\allure-2.7.0\lib

PYTHONPATH
C:\TestFramework\python36;C:\TestFramework\python36\Lib;C:\TestFramework\python36\Lib\site-packages;C:\TestFramework\python36\libs;C:\TestFramework\python36\Scripts;

##################################################################################
##################### EJECUTAR PRUEBAS CON RESULTADOS ALLURE #####################
##################################################################################
cd C:\TestFramework\workspace\Project_Basics\src\tests
SET PATH=%PATH%;%PYTHONPATH%;

@echo off
echo. ##################### PRUEBAS #####################

C:\TestFramework\python36\python.exe -m pytest tst_001.py --alluredir ..\allure-results

##################################################################################
############################# GENERAR UN REPORTE #################################
##################################################################################

SET PATH=%PATH%;%PYTHONPATH%;
C:\TestFramework\allure-2.7.0\bin\allure.bat generate C:\TestFramework\workspace\Project_Basics\src\allure-results --output C:\TestFramework\workspace\Project_Basics\src\allure-report --clean && C:\TestFramework\allure-2.7.0\bin\allure.bat open --port 5000
