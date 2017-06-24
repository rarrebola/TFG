from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create your tests here.
class TestsPrimeraIteracion(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(TestsPrimeraIteracion, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(TestsPrimeraIteracion, self).tearDown()

    # Registrar una cuenta de usuario con éxito
    def test01_registrar_cuenta_correctamente(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')
        selenium.find_element_by_xpath('/html/body/a').click() # ¿No tienes cuenta? Regístrate

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        confirmacionPassword = selenium.find_element_by_id('id_confirmacionPassword')
        email = selenium.find_element_by_id('id_email')
        confirmacionEmail = selenium.find_element_by_id('id_confirmacionEmail')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]') # Registrarse

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        confirmacionPassword.send_keys('12345678')
        email.send_keys('prueba1@socialroute.com')
        confirmacionEmail.send_keys('prueba1@socialroute.com')

        submit.send_keys(Keys.RETURN)

        assert 'No hay ninguna actualización' in selenium.page_source

    # Registro de una cuenta de usuario ya registrada
    def test02_registrar_cuenta_ya_registrada(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')
        selenium.find_element_by_xpath('/html/body/a').click()  # ¿No tienes cuenta? Regístrate

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        confirmacionPassword = selenium.find_element_by_id('id_confirmacionPassword')
        email = selenium.find_element_by_id('id_email')
        confirmacionEmail = selenium.find_element_by_id('id_confirmacionEmail')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Registrarse

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        confirmacionPassword.send_keys('12345678')
        email.send_keys('prueba@socialroute.com')
        confirmacionEmail.send_keys('prueba@socialroute.com')

        submit.send_keys(Keys.RETURN)

        assert 'Ya existe un perfil con ese alias' in selenium.page_source

    # Registro de una cuenta cuyas contraseñas no coinciden
    def test03_registrar_cuenta_contraseñas_no_coinciden(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')
        selenium.find_element_by_xpath('/html/body/a').click()  # ¿No tienes cuenta? Regístrate

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        confirmacionPassword = selenium.find_element_by_id('id_confirmacionPassword')
        email = selenium.find_element_by_id('id_email')
        confirmacionEmail = selenium.find_element_by_id('id_confirmacionEmail')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Registrarse

        alias.send_keys('prueba')
        password.send_keys('12345678')
        confirmacionPassword.send_keys('87654321')
        email.send_keys('prueba@socialroute.com')
        confirmacionEmail.send_keys('prueba@socialroute.com')

        submit.send_keys(Keys.RETURN)

        assert 'Las contraseñas no coinciden' in selenium.page_source

    # Registro de una cuenta cuyos e-mails no coinciden
    def test04_registrar_cuenta_emails_no_coinciden(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')
        selenium.find_element_by_xpath('/html/body/a').click()  # ¿No tienes cuenta? Regístrate

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        confirmacionPassword = selenium.find_element_by_id('id_confirmacionPassword')
        email = selenium.find_element_by_id('id_email')
        confirmacionEmail = selenium.find_element_by_id('id_confirmacionEmail')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Registrarse

        alias.send_keys('prueba')
        password.send_keys('12345678')
        confirmacionPassword.send_keys('12345678')
        email.send_keys('prueba@socialroute.com')
        confirmacionEmail.send_keys('prueba@socialroute.es')

        submit.send_keys(Keys.RETURN)

        assert 'Los emails no coinciden' in selenium.page_source

    # Registro de una cuenta sin completar los campos obligatorios
    def test05_registrar_cuenta_sin_completar_campos_obligatorios(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')
        selenium.find_element_by_xpath('/html/body/a').click()  # ¿No tienes cuenta? Regístrate

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        confirmacionPassword = selenium.find_element_by_id('id_confirmacionPassword')
        email = selenium.find_element_by_id('id_email')
        confirmacionEmail = selenium.find_element_by_id('id_confirmacionEmail')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Registrarse

        alias.send_keys('')
        password.send_keys('')
        confirmacionPassword.send_keys('')
        email.send_keys('')
        confirmacionEmail.send_keys('')

        submit.send_keys(Keys.RETURN)

        assert 'Registro de usuario' in selenium.page_source

    # Registro de una cuenta cuya contraseña es de menos de 8 caracteres
    def test06_registrar_cuenta_password_demasiado_corto(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')
        selenium.find_element_by_xpath('/html/body/a').click()  # ¿No tienes cuenta? Regístrate

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        confirmacionPassword = selenium.find_element_by_id('id_confirmacionPassword')
        email = selenium.find_element_by_id('id_email')
        confirmacionEmail = selenium.find_element_by_id('id_confirmacionEmail')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Registrarse

        alias.send_keys('prueba')
        password.send_keys('123')
        confirmacionPassword.send_keys('123')
        email.send_keys('prueba@socialroute.com')
        confirmacionEmail.send_keys('prueba@socialroute.com')

        submit.send_keys(Keys.RETURN)

        assert 'Este campo debe tener al menos 8 caracteres' in selenium.page_source

    # Registro de un usuario introduciendo un e-mail sin arroba
    def test07_registrar_cuenta_email_sin_arroba(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')
        selenium.find_element_by_xpath('/html/body/a').click()  # ¿No tienes cuenta? Regístrate

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        confirmacionPassword = selenium.find_element_by_id('id_confirmacionPassword')
        email = selenium.find_element_by_id('id_email')
        confirmacionEmail = selenium.find_element_by_id('id_confirmacionEmail')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Registrarse

        alias.send_keys('prueba')
        password.send_keys('12345678')
        confirmacionPassword.send_keys('12345678')
        email.send_keys('pruebasocialroute.com')
        confirmacionEmail.send_keys('pruebasocialroute.com')

        submit.send_keys(Keys.RETURN)

        assert 'Introduzca un e-mail válido' in selenium.page_source

    # Registro de un usuario introduciendo un alias que no es alfanumérico
    def test08_registrar_cuenta_alias_no_alfanumerico(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')
        selenium.find_element_by_xpath('/html/body/a').click()  # ¿No tienes cuenta? Regístrate

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        confirmacionPassword = selenium.find_element_by_id('id_confirmacionPassword')
        email = selenium.find_element_by_id('id_email')
        confirmacionEmail = selenium.find_element_by_id('id_confirmacionEmail')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Registrarse

        alias.send_keys('prueba-')
        password.send_keys('12345678')
        confirmacionPassword.send_keys('12345678')
        email.send_keys('prueba@socialroute.com')
        confirmacionEmail.send_keys('prueba@socialroute.com')

        submit.send_keys(Keys.RETURN)

        assert 'Solo se permiten caracteres alfanuméricos' in selenium.page_source

    # Registro de un usuario introduciendo un e-mail que ya está siendo utilizado
    def test09_registrar_cuenta_email_ya_registrado(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')
        selenium.find_element_by_xpath('/html/body/a').click()  # ¿No tienes cuenta? Regístrate

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        confirmacionPassword = selenium.find_element_by_id('id_confirmacionPassword')
        email = selenium.find_element_by_id('id_email')
        confirmacionEmail = selenium.find_element_by_id('id_confirmacionEmail')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Registrarse

        alias.send_keys('prueba')
        password.send_keys('12345678')
        confirmacionPassword.send_keys('12345678')
        email.send_keys('prueba1@socialroute.com')
        confirmacionEmail.send_keys('prueba1@socialroute.com')

        submit.send_keys(Keys.RETURN)

        assert 'El e-mail que ha introducido ya está en uso' in selenium.page_source

    # Acceso correcto al sistema
    def test10_acceso_correcto(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]') # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        assert 'Timeline' in selenium.page_source

    # Acceso al sistema introduciendo datos erróneos
    def test11_acceso_sistema_datos_erroneos(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('123123123')
        submit.send_keys(Keys.RETURN)

        assert 'Usuario o contraseña no válido(s)' in selenium.page_source

    # Creación de una ruta correctamente
    def test12_crear_ruta_correctamente(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        #Crear nueva ruta
        selenium.find_element_by_xpath('//*[@id="nueva-ruta"]').click() #Crear una nueva ruta
        titulo = selenium.find_element_by_xpath('//*[@id="id_titulo"]')
        descripcion =  selenium.find_element_by_xpath('//*[@id="id_descripcion"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        titulo.send_keys('Ruta de prueba')
        descripcion.send_keys('Descripción')
        submit.send_keys(Keys.RETURN)

        assert 'Ruta de prueba' in selenium.page_source

    # Creación de una ruta con datos incompletos
    def test13_creacion_ruta_campos_incompletos(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        # Crear nueva ruta
        selenium.find_element_by_xpath('//*[@id="nueva-ruta"]').click()  # Crear una nueva ruta
        titulo = selenium.find_element_by_xpath('//*[@id="id_titulo"]')
        descripcion = selenium.find_element_by_xpath('//*[@id="id_descripcion"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        titulo.send_keys('')
        descripcion.send_keys('')
        submit.send_keys(Keys.RETURN)

        assert 'Crear/editar ruta' in selenium.page_source

    # Cancelación de la creación de una ruta
    def test14_cancelar_creación_ruta(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        # Crear nueva ruta
        selenium.find_element_by_xpath('//*[@id="nueva-ruta"]').click()  # Crear una nueva ruta
        selenium.find_element_by_xpath('/html/body/div/form/a').click() # Volver

        assert 'Timeline' in selenium.page_source

    # Modificar una ruta correctamente
    def test15_modificar_ruta_correctamente(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="rutas_creadas"]/div/table/tbody/tr[1]/td/a').click() # Ruta de entre las rutas creadas
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/div[2]/a[3]').click() # Editar

        titulo =  selenium.find_element_by_xpath('//*[@id="id_titulo"]')
        descripcion =  selenium.find_element_by_xpath('//*[@id="id_descripcion"]')
        submit =  selenium.find_element_by_xpath('/html/body/div/form/input[2]') # Guardar

        titulo.clear()
        titulo.send_keys('Ruta de prueba modificada')
        descripcion.clear()
        descripcion.send_keys('Descripción modificada')
        submit.send_keys(Keys.RETURN)

        assert 'Ruta de prueba modificada' in selenium.page_source

    # Modificar una ruta con los campos vacíos
    def test16_modificar_ruta_campos_vacios(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath(
            '//*[@id="rutas_creadas"]/div/table/tbody/tr[1]/td/a').click()  # Ruta de entre las rutas creadas
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/div[2]/a[3]').click()  # Editar

        titulo = selenium.find_element_by_xpath('//*[@id="id_titulo"]')
        descripcion = selenium.find_element_by_xpath('//*[@id="id_descripcion"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Guardar

        titulo.clear()
        descripcion.clear()
        submit.send_keys(Keys.RETURN)

        assert 'Crear/editar ruta' in selenium.page_source

    # Cancelar la modificación de una ruta
    def test17_cancelar_modificacion_ruta(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="rutas_creadas"]/div/table/tbody/tr[1]/td/a').click()  # Ruta de entre las rutas creadas
        selenium.find_element_by_xpath('/html/body/div[2]/a[3]').click()  # Editar
        selenium.find_element_by_xpath('/html/body/div/form/a').click() # Volver

        selenium.implicitly_wait(20)

        assert 'Creada' in selenium.page_source

    # Cancelar el borrado de una ruta
    def test18_cancelar_borrado_ruta(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath(
            '//*[@id="rutas_creadas"]/div/table/tbody/tr[1]/td/a').click()  # Ruta de entre las rutas creadas
        selenium.find_element_by_xpath('/html/body/div[2]/a[2]').click() #Borrar
        selenium.switch_to.alert.dismiss()  # Se rechaza el borrado de la ruta

        assert 'Creada' in selenium.page_source

    # Borrar una ruta con éxito
    def test27_borrar_ruta_correctamente(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath(
            '//*[@id="rutas_creadas"]/div/table/tbody/tr[1]/td/a').click()  # Ruta de entre las rutas creadas
        selenium.find_element_by_xpath('/html/body/div[2]/a[2]').click()  # Borrar
        selenium.switch_to.alert.accept()  # Se acepta el borrado de la ruta

        assert 'Timeline' in selenium.page_source

    # Crear un día correctamente
    def test19_crear_dia_correctamente(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath(
            '//*[@id="rutas_creadas"]/div/table/tbody/tr[1]/td/a').click()  # Ruta de entre las rutas creadas
        selenium.find_element_by_xpath('/html/body/div[2]/a[4]').click() # Añadir día
        titulo = selenium.find_element_by_xpath('//*[@id="id_titulo"]')
        descripcion =  selenium.find_element_by_xpath('//*[@id="id_descripcion"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        titulo.send_keys('Día de prueba')
        descripcion.send_keys('Descripcion')
        submit.send_keys(Keys.RETURN)

        selenium.implicitly_wait(20)

        assert 'Día de prueba' in selenium.page_source

    # Creación de un día con campos obligatorios incompletos
    def test20_crear_dia_campos_incompletos(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath(
            '//*[@id="rutas_creadas"]/div/table/tbody/tr[1]/td/a').click()  # Ruta de entre las rutas creadas
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/div[2]/a[4]').click()  # Añadir día
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        submit.send_keys(Keys.RETURN)

        assert 'Crear/editar día' in selenium.page_source

    # Cancelación de la creación de un día
    def test21_cancelar_crear_dia(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath(
            '//*[@id="rutas_creadas"]/div/table/tbody/tr[1]/td/a').click()  # Ruta de entre las rutas creadas
        selenium.find_element_by_xpath('/html/body/div[2]/a[4]').click()  # Añadir día
        selenium.find_element_by_xpath('/html/body/div/form/a').click() #Volver

        selenium.implicitly_wait(20)

        assert 'Creada' in selenium.page_source

    # Modificar un día correctamente
    def test22_modificar_dia_correctamente(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="rutas_creadas"]/div/table/tbody/tr[1]/td/a').click()  # Ruta de entre las rutas creadas
        selenium.find_element_by_xpath('/html/body/div[2]/div/table/tbody/tr[1]/td[1]/a').click() # Día de entre los días de la ruta
        selenium.implicitly_wait(20)
        selenium.find_element_by_xpath('/html/body/div[2]/p/a[3]').click()  # Editar

        titulo = selenium.find_element_by_xpath('//*[@id="id_titulo"]')
        descripcion = selenium.find_element_by_xpath('//*[@id="id_descripcion"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        titulo.clear()
        titulo.send_keys('Día de prueba modificado')
        descripcion.clear()
        descripcion.send_keys('Descripción modificada')
        submit.send_keys(Keys.RETURN)
        selenium.implicitly_wait(20)

        assert 'Día de prueba modificado' in selenium.page_source

    # Modificar un día con los campos obligatorios vacíos
    def test23_modificar_dia_campos_incompletos(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath(
            '//*[@id="rutas_creadas"]/div/table/tbody/tr[1]/td/a').click()  # Ruta de entre las rutas creadas
        selenium.find_element_by_xpath(
            '/html/body/div[2]/div/table/tbody/tr[1]/td[1]/a').click()  # Día de entre los días de la ruta
        selenium.implicitly_wait(20)
        selenium.find_element_by_xpath('/html/body/div[2]/p/a[3]').click()  # Editar

        titulo = selenium.find_element_by_xpath('//*[@id="id_titulo"]')
        descripcion = selenium.find_element_by_xpath('//*[@id="id_descripcion"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        titulo.clear()
        descripcion.clear()
        submit.send_keys(Keys.RETURN)

        assert 'Crear/editar día' in selenium.page_source

    # Cancelar la modificación del día
    def test24_cancelar_modificar_dia(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath(
            '//*[@id="rutas_creadas"]/div/table/tbody/tr[1]/td/a').click()  # Ruta de entre las rutas creadas
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath(
            '/html/body/div[2]/div/table/tbody/tr[1]/td[1]/a').click() # Día de entre los días de la ruta
        selenium.implicitly_wait(20)
        selenium.find_element_by_xpath('/html/body/div[2]/p/a[3]').click()  # Editar
        selenium.find_element_by_xpath('/html/body/div/form/a').click() # Volver
        selenium.implicitly_wait(20)

        assert 'Añadir lugares de interés' in selenium.page_source

    # Cancelar borrar día
    def test25_cancelar_borrar_dia(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath(
            '//*[@id="rutas_creadas"]/div/table/tbody/tr[1]/td/a').click()  # Ruta de entre las rutas creadas
        selenium.find_element_by_xpath(
            '/html/body/div[2]/div/table/tbody/tr[1]/td[1]/a').click()  # Día de entre los días de la ruta
        selenium.implicitly_wait(20)
        selenium.find_element_by_xpath('/html/body/div[2]/p/a[2]').click() # Borrar
        selenium.switch_to.alert.dismiss()

        assert 'Día de prueba modificado' in selenium.page_source

    # Borrar día correctamente
    def test26_borrar_dia(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath(
            '//*[@id="rutas_creadas"]/div/table/tbody/tr[1]/td/a').click()  # Ruta de entre las rutas creadas
        selenium.find_element_by_xpath(
            '/html/body/div[2]/div/table/tbody/tr[1]/td[1]/a').click()  # Día de entre los días de la ruta
        selenium.implicitly_wait(20)
        selenium.find_element_by_xpath('/html/body/div[2]/p/a[2]').click()  # Borrar
        selenium.switch_to.alert.accept()

        assert 'Día de prueba modificado' not in selenium.page_source