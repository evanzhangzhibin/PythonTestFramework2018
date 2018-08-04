# PythonTestFrameWork2018
Este Framework Selenium Basado en Python, incluye Allure Framework 2, pillow, pytest y otras hierbas.

#################################
 VARIABLES DE ENTORNO
#################################

ALLURE_SRC
C:\Program Files\Java\jdk1.8.0_111

PATH
%ALLURE_HOME%;C:\TestFramework\allure-2.7.0\lib

PYTHONPATH
C:\TestFramework\python36;C:\TestFramework\python36\Lib;C:\TestFramework\python36\Lib\site-packages;C:\TestFramework\python36\libs;C:\TestFramework\python36\Scripts;

######################################
EJECUTAR PRUEBAS CON RESULTADOS ALLURE 
######################################
cd C:\TestFramework\workspace\Project_Basics\src\tests
SET PATH=%PATH%;%PYTHONPATH%;

@echo off
echo. ##################### PRUEBAS #####################

C:\TestFramework\python36\python.exe -m pytest tst_001.py --alluredir ..\allure-results

############################################################
############### GENERAR UN REPORTE #########################
############################################################

SET PATH=%PATH%;%PYTHONPATH%;
C:\TestFramework\allure-2.7.0\bin\allure.bat generate C:\TestFramework\workspace\Project_Basics\src\allure-results --output C:\TestFramework\workspace\Project_Basics\src\allure-report --clean && C:\TestFramework\allure-2.7.0\bin\allure.bat open --port 5000


############### Librerias #########################
allure-pytest (2.5.0)
allure-python-commons (2.5.0)
attrs (17.3.0)
colorama (0.3.9)
enum34 (1.1.6)
et-xmlfile (1.0.1)
jdcal (1.3)
lxml (4.1.1)
namedlist (1.7)
openpyxl (2.4.9)
Pillow (5.2.0)
pip (9.0.1)
pluggy (0.6.0)
py (1.5.2)
pytest (3.3.1)
selenium (3.8.0)
setuptools (38.2.4)
six (1.11.0)
unittest-xml-reporting (2.1.0)
wheel (0.30.0)
