# -*- coding: utf-8 -*-
from src.pages.Inicio import Inicio
from src.utils.functions import CommonFunctions as Selenium

class login(Selenium):
    
    def rutina_logueo(self):
        self.Xpath_elements(Inicio.txt_Usuario_xpath).send_keys(self.user)
        
        self.Xpath_elements(Inicio.txt_Password_xpath).send_keys(self.passWord )
                    
        self.capturar_Pantalla(u'ESPERAR EL INICIO DE LA APP')
        
        self.Xpath_elements(Inicio.btn_BotonInicio_xpath).click()
        
        self.waitStopLoad(3)
        
        
        self.comprobacion_logueo()
        
    def comprobacion_logueo(self):
    
        error = self.waitLoginElements(Inicio.lbl_MensajeError_xpath)
        logueo_ok = self.waitLoginElements(Inicio.lbl_UsuarioLogueado_xpath)
                     
        if logueo_ok == True:
            print "*****************************"
            print "Se ha logueado correctamente"
            print "*****************************"
            
            self.capturar_Pantalla(u'USUARIO YA LOGUEADO')

        if error == True:
            mensaje = self.Xpath_elements(Inicio.lbl_MensajeError_xpath).text
            self.capturar_Pantalla(u'USUARIO INVALIDO')
            print "*****************************"
            print mensaje
            print "*****************************"
            self.assertFalse(error)
                    
                    
                    