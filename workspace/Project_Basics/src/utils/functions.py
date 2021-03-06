# -*- coding: utf-8 -*-
import os, io, shutil
import time
import datetime
import openpyxl
from src.utils.config import Configuracion
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains  import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select   
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

import allure
from PIL import Image
  
import re
import json

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import pytest


dia = time.strftime("%Y-%m-%d")  # formato aaaa/mm/dd
hora = time.strftime("%H%M%S")  # formato 24 houras


class CommonFunctions:
    
#ACCEDER AL CONF.PROPERTIES
#     propsFile = 'conf.properties'
#     propsSeparador = "="
#     keys = CommonFunctions.setProps(propsFile, propsSeparador)

    @staticmethod
    def setProps(propsFile, propsSeparator):
        keysValues = {}
        with open(propsFile) as f:
            for line in f:
                if not line.startswith("#"):
                    if propsSeparator in line:
                        name, value = line.split(propsSeparator, 1)
                        keysValues[name.strip()] = value.strip()
        return keysValues

    # 20170419 - EJV


    # 20170419 - EJV
    # managePaths: Funcion para la administracion de directorios de evidencias.
    def managePaths(self, pathToValidate):
        if not os.path.exists(pathToValidate):
            os.makedirs(pathToValidate)
        else:
            pass

    @staticmethod
    def dateToStr(strFormat):
        strDate = datetime.datetime.today().strftime(strFormat)
        return strDate
    
    def increment(self, value, increment=1):
        value += increment
        return value

    def initBaseCounters(self):
        baseCounter = {} 
        for base in self.__class__.__bases__:
            baseCounter[base.__name__ ] = 0
        return baseCounter 
    
    def setValueBaseCounter(self, baseName):
        self.evidenciaSSBaseCounters[baseName ] = self.increment(self.evidenciaSSBaseCounters[baseName ])
        return self.evidenciaSSBaseCounters[baseName ] 
    
    @staticmethod
    def getOsEnvVar(osVar):
        if os.environ.get(osVar) is None:
            return ""
        else:
            return os.environ[osVar]

    def abrirNavegador(self, URL):
       
        navegador = Configuracion.Navegador
        
        if navegador == ("CHROME"):
            options = Options()
            options.add_argument('--start-maximized')
            self.driver = webdriver.Chrome(chrome_options=options)
            self.driver.implicitly_wait(10)
            self.dir_navegador = "Chrome"
            self.driver.get(URL)
            return self.driver
        
        if navegador == ("CHROME_headless"):
            
            options = Options()
            options.add_argument('headless')
            options.add_argument('--start-maximized')
            self.driver = webdriver.Chrome(chrome_options=options)
            self.driver.implicitly_wait(10)
            self.dir_navegador = "Chrome Headless"
            self.driver.get(URL)
            return self.driver

        elif navegador == ("FIREFOX"):
            self.driver = webdriver.Firefox(firefox_binary='C:\\TestFramework\\FirefoxPortable\\FirefoxPortable.exe')
            self.driver.maximize_window()
            self.driver.implicitly_wait(10)
            self.dir_navegador = "Firefox"
            self.driver.get(URL)
            return self.driver 

        elif navegador == ("IE"):
            self.driver = webdriver.Ie()
            self.driver.maximize_window()
            self.driver.implicitly_wait(10)
            self.dir_navegador = "Internet Explorer"
            self.driver.get(URL)
            return self.driver

        else:
            pytest.skip("NO SE PUDO INICIALIZAR EL DRIVER")   
    
        

    def elementIsPresent(self, by , strElement, waitLoad="S"):
        self.driver.implicitly_wait(20)          
        # print("elementIsPresent - waitLoad: " + waitLoad)
        
        if waitLoad == "S":
            self.waitStopLoad()
    
        for i in range(115):
            # print("elementIsPresent: " + strElement)
            try:
                if self.is_element_present(by, strElement):  break
            except: pass
            time.sleep(1)
        else: self.fail("Tiempo de espera (" + str(i) + "s) superado para elemento: " + strElement)
        self.driver.implicitly_wait(20)
        
        
    def elementIsPresentEnebledDisplayed(self, strElement):        
        self.driver.implicitly_wait(20) 
        for i in range(15):
            # print("Esperando que elemento este activo: " + strElement)
            try:
                if self.is_element_present(By.XPATH, strElement) and self.driver.find_element_by_xpath(strElement).is_enabled()  and self.driver.find_element_by_xpath(strElement).is_displayed():  break
                # if self.is_element_present(by, strElement):  break
            except: pass
            time.sleep(1)
        else: self.fail("Tiempo de espera elemento activo (" + str(i) + "s) superado para elemento: " + strElement)        
        self.driver.implicitly_wait(20) 


    def waitStopLoad(self, timeLoad=8):
        print ("waitStopLoad: Inicia")
        try:
                totalWait = 0
                while (totalWait < timeLoad):
                    print("Cargando ... intento: " + str(totalWait))
                    time.sleep(1)
                    totalWait = totalWait + 1
        except: 
            print ("waitStopLoad: Carga Finalizada ... ")                

    
            
    def waitElementIsLoad(self, xpath):
        
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            
        except TimeoutException:
        
            print (u"waitElementIsLoad: No presente " + xpath)
            return False
        
        print (u"waitElementIsLoad: Se mostró el elemento " + xpath)
        return True

    def waitElementIsLoad_CSS(self, strElementLoad):
        self.driver.implicitly_wait(20) 
        try:
            # print ("waitElementIsLoad: " + strElementLoad)
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, strElementLoad)))
            elem = self.driver.find_element(By.CSS_SELECTOR, strElementLoad)
            
            while ((not(elem.is_displayed())) or (not (elem.is_enabled()))):
                pass
            
        except:
            print ("Exception waitElementIsLoad: " + strElementLoad)  
            raise TimeoutException
        self.driver.implicitly_wait(20)           
    
    def waitElementIsLoad_Class(self, strElementLoad):
        self.driver.implicitly_wait(20) 
        try:
            # print ("waitElementIsLoad: " + strElementLoad)
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, strElementLoad)))
            elem = self.driver.find_element(By.CLASS_NAME, strElementLoad)
            
            while ((not(elem.is_displayed())) or (not (elem.is_enabled()))):
                pass
            
        except:
            print ("Exception waitElementIsLoad: " + strElementLoad)  
            raise TimeoutException
        self.driver.implicitly_wait(20)  
                
    def quitDriver(self):
        self.driver.quit()

        
    # =============================================================================================
    # =============================================================================================        
    # 20170621 - UNIFICAR CODE


    def waitClick(self, strXPATH):
        self.clickElement(strXPATH)
        self.waitStopLoad()    
    
#     def clickElemtPopUp (self, strXPATH): 
#         wait = WebDriverWait(self.driver, 30)
#         wait.until(EC.presence_of_element_located((By.XPATH, strXPATH)))        
#         elem = self.driver.waitF    

    def clikElemtNotDisplayXPATH(self, strXPATH):
#         print (strXPATH)
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.presence_of_element_located((By.XPATH, strXPATH)))        
        elem = self.driver.find_element(By.XPATH, strXPATH)    
        while (not elem.is_displayed()):
            pass
             
        while (not elem.is_enabled()):
            pass

        self.driver.execute_script("$(arguments[0]).click();", elem)            
        
    def clickElementWait (self, strXPATH):
        self.clikElemtNotDisplayXPATH(strXPATH)
        self.waitStopLoad()
       
    def clickElement(self, strXPATH):
        
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.presence_of_element_located((By.XPATH, strXPATH)))
        elem = self.driver.find_element(By.XPATH, strXPATH)
        while (not(elem.is_enabled())):
            pass
        while (not(elem.is_displayed())) :
            pass

        
        elem.click()
        
    def clickInputText (self, strXPATHPoint, strValue):
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.presence_of_element_located((By.XPATH, strXPATHPoint)))    
        elem = self.driver.find_element(By.XPATH, strXPATHPoint)
        while (not(elem.is_displayed())):
            pass
        while (not(elem.is_enabled())):
            pass
        elem.click()
        elem.clear()
        elem.send_keys(strValue)
        

    def endTabPage(self):
        windows = self.driver.window_handles
        self.driver.close();
        self.driver.switch_to.window(windows[0])
        
    def compareText(self, stringA, stringB):

        print ("mensaje a comparar   ")
        print (stringA)
        print (stringB)

        if(stringA == stringB):        
            assert (True)
        else:
            print (stringA + " **ES DISTINTO A **" + stringB)
            assert (False)        
    
    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True
    
    def check_exists_by_CSS(self, css):
        try:
            self.driver.find_element_by_css_selector(css)
        except NoSuchElementException:
            return False
        return True
    
    def buscar_texto(self, texto):
        if (texto in self.driver.page_source):
            print ("Esta presente el Elemento: " + texto)
        else:
            print ("No esta presente el Elemento: " + texto)
        
    
    def DesplazarHaciaElemento(self, elemento):
        #VARIABLES SCREENSHOTS  
        element = self.driver.find_element_by_xpath(elemento)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.capturarPantalla()

    # =============================================================================================
    # IR A UN ELEMENTO / ESPERAR QUE UN ELEMENTO SE VISUALICE
    #************************** CDA - FUNCTIONS **************************
    # =============================================================================================        
    
    def ir_a_xpath(self, elemento):
        try:
            localizador = self.driver.find_element(By.XPATH, elemento)  
            self.driver.execute_script("arguments[0].scrollIntoView();", localizador)
            
        except TimeoutException:
            
            print (u"ir_a_xpath: No presente " + elemento)
            return False
        
        print (u"ir_a_xpath: Se desplazó al elemento, " + elemento)
        return True
    
        self.capturarPantalla()
    
    def ir_a_id(self, elemento):
        try:
            localizador = self.driver.find_element(By.ID, elemento)  
            self.driver.execute_script("arguments[0].scrollIntoView();", localizador)
            
        except TimeoutException:
            
            print (u"ir_a_xpath: No presente " + elemento)
            return False
        
        print (u"ir_a_xpath: Se desplazó al elemento, "+ elemento)
        return True
    
        self.capturarPantalla()
    
    
    def esperar_ID(self, ID): #Esperar que un elemento sea visible 
        try:
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.visibility_of_element_located((By.ID, ID)))
            
        except TimeoutException:
        
            print (u"esperar_Xpath: No presente " + ID)
            return False
        
        print (u"esperar_Xpath: Se mostró el elemento " + ID)
        return True
    
    
    def esperar_Xpath(self, xpath): #Esperar que un elemento sea visible 
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            
            totalWait = 0
            while (totalWait < 1):
                print("Cargando ... intento: " + str(totalWait))
                time.sleep(1)
                totalWait = totalWait + 1
            
        except TimeoutException:
        
            print (u"esperar_Xpath: No presente " + xpath)
            return False
        
        print (u"esperar_Xpath: Se mostró el elemento " + xpath)
        return True
    
    def esperar_Name(self, name): #Esperar que un elemento sea visible 
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.visibility_of_element_located((By.NAME, name)))
            
        except TimeoutException:
        
            print (u"esperar_Xpath: No presente " + name)
            return False
        
        print (u"esperar_Xpath: Se mostró el elemento " + name)
        return True   

    def esperar_CSS(self, CSS): #Esperar que un elemento sea visible 
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, CSS)))
            
        except TimeoutException:
        
            print (u"esperar_CSS: No presente " + CSS)
            return False
        
        print (u"esperar_CSS: Se mostró el elemento " + CSS)
        return True
    
    def esperar_Link(self, LINK): #Esperar que un elemento sea visible 
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, LINK)))
            
        except TimeoutException:
        
            print (u"esperar_Link: No presente " + LINK)
            return False
        
        print (u"esperar_Link: Se mostró el elemento " + LINK)
        return True

    # =============================================================================================
    # MANIPULAR ELEMENTOS DEL DOM
    #**************************CDA - FUNCTIONS**************************
    # =============================================================================================        
    def Xpath_elements(self, xpath):
        localizador = self.driver.find_element_by_xpath(xpath)
        return localizador
    
    def CSS_elements(self, css):
        localizador = self.driver.find_element_by_css_selector(css)
        return localizador
    
    def ID_elements(self, ID):
        localizador = self.driver.find_element_by_id(ID)
        return localizador
    
    def Name_elements(self, name):
        localizador = self.driver.find_element_by_name(name)
        return localizador
    
    def Link_elements(self, link):
        localizador = self.driver.find_element_by_partial_link_text(link)
        return localizador
    
    # =============================================================================================
    # CLIQUEAR ELEMENTOS DESDE EL JAVASCRIPT
    #**************************CDA - FUNCTIONS**************************
    # =============================================================================================        
    
    def JS_Click_Xpath(self, xpath):
        localizador = self.driver.find_element_by_xpath(xpath)
        self.driver.execute_script("arguments[0].click();", localizador)
    
    def JS_Click_CSS(self, css):
        localizador = self.driver.find_element_by_css_selector(css)
        self.driver.execute_script("arguments[0].click();", localizador)
    
    def JS_Click_ID(self, ID):
        localizador = self.driver.find_element_by_id(ID)
        self.driver.execute_script("arguments[0].click();", localizador)

    def JS_Click_Link(self, link):
        localizador = self.driver.find_element_by_partial_link_text(link)
        self.driver.execute_script("arguments[0].click();", localizador)
  
    # =============================================================================================
    # SELECCIONAR UN ELEMENTO DE LA LISTA POR TEXTO O POSICION
    #**************************CDA - FUNCTIONS**************************
    # =============================================================================================        
       
    
    def select_elements_id(self, ID):
        select = Select(self.driver.find_element_by_id(ID))
        return select
    
    def select_elements_xpath(self, xpath):
        select = Select(self.driver.find_element_by_xpath(xpath))
        return select
    
    def select_elements_css(self, css):
        select = Select(self.driver.find_element_by_css_selector(css))
        return select
    
    #USO

#       select by visible text
#       select.select_by_visible_text('Banana')
        
#       select by value 
#       select.select_by_value('1')

    # =============================================================================================
    # Captura de Pantalla
    #**************************CDA - FUNCTIONS**************************
    # =============================================================================================        
       

    # nomenclatura de la evidencia: número_caso_de_prueba + hora [hh:mm:ss]
    def capturarPantalla(self):

        
        def hora_Actual():
            hora = time.strftime("%H%M%S")  # formato 24 houras
            return hora
        
        GeneralPath = Configuracion.hbPfPathEvidencia
        DriverTest = Configuracion.Navegador
        TestCase = self.__class__.__name__
        horaAct = hora
        path = GeneralPath + dia + "\\" + TestCase + "\\" + DriverTest + "\\" +  horaAct + "\\"

        if not os.path.exists(path): # si no existe el directorio lo crea

            os.makedirs(path)

        img = path + TestCase + "_(" + str(hora_Actual()) + ")" + ".png"
        
        print (u"Se guardo la captura en " + img)
        
        self.driver.get_screenshot_as_file(img)
        
        return img
    
    def capturar_Pantalla(self, Descripcion):
        IMAGEN = self.capturarPantalla()
        CAPTURA = Image.open(IMAGEN, mode="r")
        ImageProcess = io.BytesIO()
        CAPTURA.save(ImageProcess, format= "PNG")
        ImageProcess = ImageProcess.getvalue()
        allure.attach(ImageProcess, Descripcion, attachment_type=allure.attachment_type.PNG)
        
    # =============================================================================================
    # Verificar Texto en los Elementos y Verificar un Xpath
    #**************************CDA - FUNCTIONS**************************
    # =============================================================================================        
        
    def verificarTexto_xpath(self, xpath, TEXTO): #devuelve true o false
        try:
            wait = WebDriverWait(self.driver, 15)
            wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath), TEXTO))
        except TimeoutException:
            print (u"Verificar Texto: Texto No presente " + xpath + " el texto, " + TEXTO)
            return False
        print (u"Verificar Texto: Se visualizó en, " + xpath + " el texto, " + TEXTO)
        return True
    
    def verificarTexto_css(self, CSS, TEXTO): #devuelve true o false
        try:
            wait = WebDriverWait(self.driver, 15)
            wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, CSS), TEXTO))
        except TimeoutException:
            print (u"Verificar Texto: Texto No presente " + CSS + " el texto, " + TEXTO)
            return False
        print (u"Verificar Texto: Se visualizó en, " + CSS + " el texto, " + TEXTO)
        return True
    
    def verificarTexto_ID(self, ID, TEXTO): #devuelve true o false
        try:
            wait = WebDriverWait(self.driver, 15)
            wait.until(EC.text_to_be_present_in_element((By.ID, ID), TEXTO))
        except TimeoutException:
            print (u"Verificar Texto: Texto No presente " + ID  + " el texto, " + TEXTO)
            return False
        print (u"Verificar Texto: Se visualizó en, " + ID  + " el texto, " + TEXTO)
        return True
    
    def verificarTexto_link(self, link, TEXTO): #devuelve true o false
        try:
            wait = WebDriverWait(self.driver, 15)
            wait.until(EC.text_to_be_present_in_element((By.LINK_TEXT, link), TEXTO))
        except TimeoutException:
            print (u"Verificar Texto: Texto No presente " + link  + " el texto, " + TEXTO)
            return False
        print (u"Verificar Texto: Se visualizó en, " + link  + " el texto, " + TEXTO)
        return True
    
    def verificar_xpath(self, xpath): #devuelve true o false
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            print (u"Verificar: Elemento No presente " + xpath)
            return False
        print (u"Verificar: Se visualizo el elemento, "+ xpath)
        return True

    def verificar_ID(self, ID): #devuelve true o false
        try:
            self.driver.find_element_by_id(ID)
        except NoSuchElementException:
            print (u"Verificar: Elemento No presente "+ ID)
            return False
        print (u"Verificar: Se visualizo el elemento, "+ ID)
        return True
    
    def verificar_CSS(self, CSS): #devuelve true o false
        try:
            self.driver.find_element_by_css_selector(CSS)
        except NoSuchElementException:
            print (u"Verificar: Elemento No presente " + CSS)
            return False
        print (u"Verificar: Se visualizo el elemento, "+ CSS)
        return True
    
    def cerrar_alerta_gettext(self):
        self.accept_next_alert = True
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    

    def mouse_over_id(self, ID):
        element = self.driver.find_element_by_id(ID)
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()

    def mouse_over_xpath(self, xpath):
        element = self.driver.find_element_by_xpath(xpath)
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()
        
    def mouse_over_css(self, css):
        element = self.driver.find_element_by_css_selector(css)
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()  
    
    
    def waitLoginElements(self, xpath):
        
        try:
            wait = WebDriverWait(self.driver, 2)
            wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            
        except TimeoutException:
            print (u"waitLoginElements: No presente " + xpath)
            return False
            
        print (u"waitLoginElements: Se mostró el elemento "+ xpath)
        return True
    
    def waitLoginElements_Link(self, xpath):
        
        try:
            wait = WebDriverWait(self.driver, 2)
            wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, xpath)))
            
        except TimeoutException:
            print (u"waitLoginElements: No presente " + xpath)
            return False
            
        print (u"waitLoginElements: Se mostró el elemento "+ xpath)
        return True
    
    def waitLoginElementsCSS(self, CSS):
        
        try:
            wait = WebDriverWait(self.driver, 2)
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, CSS)))
            
        except TimeoutException:
            print (u"waitLoginElementsCSS: No presente " + CSS)
            return False
            
        print (u"waitLoginElementsCSS: Se mostró el elemento " + CSS)
        return True
    
    def LeerCelda(self, celda):
        wb = openpyxl.load_workbook(Configuracion.Excel)
        sheet = wb["DataTest"]
        hoja= sheet
        valor= hoja[celda].value
        print ("El valor de la celda es: " + valor)
        return valor
    
    def EscribirCelda(self, celda, valor):
        wb = openpyxl.load_workbook(Configuracion.Excel)
        hoja = wb.active
        hoja[celda]= valor
        wb.save(Configuracion.Excel)
        print ("Se escribio en la celda " + str(celda) + " el valor: " + str (valor))
    
    
    def Assert_xpath(self, xpath):
        try:
            
            wait = WebDriverWait(self.driver, 2)
            wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            
        except TimeoutException:
            print (u"Assert_xpath: Elemento No presente " + xpath)
            self.assertTrue(False)
            
        print (u"Assert_xpath: Se visualizo el elemento, "+ xpath)
        self.assertTrue(True)
 
    def Assert_CSS(self, CSS):
        try:
            
            wait = WebDriverWait(self.driver, 2)
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, CSS)))
            
        except TimeoutException:
            print (u"Assert_xpath: Elemento No presente " + CSS)
            self.assertTrue(False)
            
        print (u"Assert_xpath: Se visualizo el elemento, "+ CSS)
        self.assertTrue(True)    
        
    def Modificar_XML_Enviroments(self):
        
        print ("--------------------------------------")
        print ("Estableciendo Datos del Reporte...")
        JOB_NAME = os.environ['JOB_NAME']
        NODE_NAME = os.environ['NODE_NAME']
        NAVEGADOR = Configuracion.Navegador
        print (NODE_NAME)
        print (JOB_NAME)
        print (NAVEGADOR)
        print ("--------------------------------------")

        Enviroment = open('../utils/environment.xml', 'w')
        Template = open('../utils/environment_Template.xml', 'r')
        
        with Template as f:
            texto = f.read()
            
            texto = texto.replace("JOB_NAME", JOB_NAME)
            texto = texto.replace("NODE_NAME", NODE_NAME)
            texto = texto.replace("NAVEGADOR", NAVEGADOR)
        
        with Enviroment as f:
            f.write(texto)
             
        Enviroment.close()    
        Template.close()

        time.sleep(5) 
        
        shutil.rmtree("../allure-results")
        
        try:
            os.makedirs("../allure-results")
        except OSError:
            pass
        
        shutil.copy("../utils/environment.xml","../allure-results")
        
    # 20171018 - EJV - ENVIO DE MAILS 
    @staticmethod
    def send_mail(send_from, send_to, subject, text, files=None,
                  server="127.0.0.1", port="25",  username=None, password=None):
        assert isinstance(send_to, list)
    
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Bcc'] = COMMASPACE.join(["Ernesto Verbanaz <verbanaz@gmail.com>"]) 
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
    
        msg.attach(MIMEText(text))
    
        for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After office close
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)
    
    
        smtp = smtplib.SMTP(server, port)
        
        smtp.set_debuglevel(False)
        smtp.login(username, password)   
        smtp.default_port     
        
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()   
        
    def mailing(self, Adjuntos, PRODUCTO, JENKINS):
        import socket
        
        strTimeSubject = self.dateToStr("%Y-%m-%d %H:%M")
        strTimeStart = self.dateToStr("%Y-%m-%d %H:%M")
        
        #
        msgAsunto = "Resumen Automatizado CRM del dia: " + strTimeSubject
        msgFrom = "prueba.homologacion@itau.com.ar"
        msgTO = ["mervindiazlugo@gmail.com" , "mervin.diaz@itau.com.ar", "Testing.Factory@itau.com.ar", "gustavo.martorano@itau.com.ar", "ernesto.verbanaz@itau.com.ar", "verbanaze@gmail.com" ]
        #msgTO = ["ernesto.verbanaz@itau.com.ar"] 
        msgBody = ('''
                Esta notificacion fue generada de forma automatica, al concluir el proceso de ejecucion de pruebas automatizadas en el ambiente de homologacion,
                para la version Portal de ''' + PRODUCTO +'''
                
                Inicio Proceso: {0}
                Final Proceso: {1}
                Hostname: {2}
                
                
                --> (#) Adjuntos los indicadores correspondientes, en formato HTML. (#) <--
                
                Para verel historial de ejecuciones visite:
                '''+ JENKINS +'''
                    
                  
                ''')
        time.sleep(20)
        msgAttachments = [Adjuntos]
        
        #
        smtpHost = "correo.sis.ad.bia.itau"
        smtpPort = "2525"
        smtpUser = "SISTEMA/SRV_HOMO"
        smtpPass = "QsdRwe*17"

        #
        strTimeStop = self.dateToStr("%Y-%m-%d %H:%M")
        
        #
        msgBody = msgBody.format(strTimeStart, strTimeStop, socket.gethostname())
        
        #
        self.send_mail(msgFrom, msgTO , msgAsunto, msgBody, msgAttachments, smtpHost, smtpPort, smtpUser, smtpPass)