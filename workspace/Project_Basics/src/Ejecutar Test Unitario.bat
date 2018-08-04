cd C:\ITAU_Tools\QA_Automation\workspace\Clarity_Prod\src\tests
SET PATH=%PATH%;%PYTHONPATH%;%PYTHON_HOME%;%SELENIUM_WEBDRIVERS%;%JDK_HOME%;%FUNK_PATH%;


C:\ITAU_Tools\QA_Automation\Python27\python.exe -m pytest tst_001.py --alluredir ..\allure-results
PAUSE
