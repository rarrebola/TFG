from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create your tests here.
class TestsSegundaIteracion(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(TestsSegundaIteracion, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(TestsSegundaIteracion, self).tearDown()

    # Salida del sistema
    def test01_salida_del_sistema(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="dropdownMenu1"]').click() # Button dropdown del navbar
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/ul/li[6]/a').click() # Cerrar sesión

        assert 'He olvidado mi contraseña' in selenium.page_source

    # Búsqueda de rutas con éxito
    def test02_buscar_rutas_con_exito(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('Sevilla')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click() # Lupa
        selenium.implicitly_wait(20)

        enlace = selenium.find_element_by_xpath('//*[@id="rutas"]/ul/li/a')

        assert enlace.text == 'Cordoba y Sevilla en un fin de semana'

    # Búsqueda de rutas con parámetro vacío
    def test03_buscar_rutas_parametro_vacio(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa

        assert 'Timeline' in selenium.page_source

    # Búsqueda de rutas sin coincidencias
    def test04_buscar_ruta_sin_coincidencias(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('asdfa')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa

        assert 'No se han encontrado coincidencias' in selenium.page_source

    # Seguimiento de rutas correcto
    def test04_seguir_ruta_correctamente(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('a')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa

        enlace = selenium.find_element_by_xpath('//*[@id="rutas"]/ul/li[1]/a') # Primera ruta de la lista
        ruta = enlace.text
        enlace.click()
        selenium.implicitly_wait(20)
        selenium.find_element_by_xpath('/html/body/a').click() # Seguir ruta
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click() # Mi perfil
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/div/div/ul/li[2]/a').click()  # Rutas seguidas
        selenium.implicitly_wait(10)

        assert ruta in selenium.page_source

    # Seguir una ruta anteriormente seguida
    def test05_seguir_ruta_antes_seguida(self):
        selenium = self.selenium
        selenium.get('http://localhost:8000/219/seguirRuta/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.implicitly_wait(20)

        selenium.get('http://localhost:8000/219/seguirRuta/')

        assert 'Dejar de seguir' in selenium.page_source

    # Seguir ruta creada por sí mismo
    def test06_seguir_ruta_creada_el_mismo(self):
        selenium = self.selenium
        selenium.get('http://localhost:8000/219/seguirRuta/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        selenium.implicitly_wait(20)

        selenium.get('http://localhost:8000/219/seguirRuta/')

        assert 'Dejar de seguir' not in selenium.page_source

    # Dejar de seguir ruta correctamente
    def test07_dejar_de_seguir_ruta(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click()  # Mi perfil
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/div/div/ul/li[2]/a').click()  # Rutas seguidas
        selenium.implicitly_wait(10)
        enlace = selenium.find_element_by_xpath('//*[@id="rutas_seguidas"]/div/table/tbody/tr[1]/td/a') # Primera ruta de la lista de seguidas
        ruta = enlace.text
        enlace.click()
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/a').click() # Dejar de seguir
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click()  # Mi perfil
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/div/div/ul/li[2]/a').click()  # Rutas seguidas
        selenium.implicitly_wait(10)

        assert ruta not in selenium.page_source

    # Dejar de seguir una ruta que no se seguía anteriormente
    def test08_dejar_de_seguir_ruta_no_seguida(self):
        selenium = self.selenium
        selenium.get('http://localhost:8000/219/seguirRuta/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.implicitly_wait(20)

        selenium.get('http://localhost:8000/219/dejarDeSeguirRuta/')

        selenium.implicitly_wait(20)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click()  # Mi perfil
        selenium.find_element_by_xpath('/html/body/div/div/ul/li[2]/a').click()  # Rutas seguidas

        assert 'Irlanda en dos semanas' not in selenium.page_source

    # Dejar de seguir una ruta creada por el propio usuario
    def test09_dejar_de_seguir_ruta_creada_por_el_mismo(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        selenium.get('http://localhost:8000/219/dejarDeSeguirRuta/')

        assert 'Seguir' not in selenium.page_source

    # Búsqueda de usuarios con éxito
    def test10_buscar_rutas_con_exito(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('sbalmes')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa
        selenium.find_element_by_xpath('/html/body/div/ul/li[2]/a').click() #Usuarios

        usuario = selenium.find_element_by_xpath('//*[@id="usuarios"]/ul/li/a')

        assert usuario.text == 'sbalmes'

    # Búsqueda de usuarios con parámetro vacío
    def test11_buscar_rutas_parametro_vacio(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa

        assert 'Timeline' in selenium.page_source

    # Búsqueda de rutas sin coincidencias
    def test12_buscar_ruta_sin_coincidencias(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('asdfa')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa
        selenium.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()  # Usuarios

        assert 'No se han encontrado coincidencias' in selenium.page_source

    # Seguimiento de usuarios correcto
    def test13_seguir_usuario_correctamente(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('a')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa
        selenium.find_element_by_xpath('/html/body/div/ul/li[2]/a').click() #Usuarios
        selenium.implicitly_wait(10)
        enlace = selenium.find_element_by_xpath('//*[@id="usuarios"]/ul/li[1]/a') #Primer usuario de la lista
        usuario = enlace.text
        enlace.click()
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/a').click() #Seguir
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click()  # Mi perfil
        selenium.find_element_by_xpath('/html/body/div/div/ul/li[3]/a').click()  # Usuarios seguidos

        assert usuario in selenium.page_source

    # Seguir usuario seguido anteriormente
    def test14_seguir_usuario_seguido_anteriormente(self):
        selenium = self.selenium
        selenium.get('http://localhost:8000/219/seguirRuta/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.implicitly_wait(20)

        selenium.get('http://localhost:8000/107/seguirUsuario/')

        assert 'Dejar de seguir' in selenium.page_source

    # Seguirse a sí mismo
    def test15_seguirse_si_mismo(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        selenium.get('http://localhost:8000/107/seguirUsuario/')

        assert 'Dejar de seguir' not in selenium.page_source

    # Dejar de seguir a un usuario correctamente
    def test16_dejar_de_seguir_usuario(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click() # Mi perfil
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/div/div/ul/li[3]/a').click() # Usuarios seguidos
        selenium.find_element_by_xpath('//*[@id="usuarios_seguidos"]/div/table/tbody/tr/td/a').click() # Primer usuario de la lista
        selenium.find_element_by_xpath('/html/body/a').click() # Dejar de seguir

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click()  # Mi perfil
        selenium.find_element_by_xpath('/html/body/div/div/ul/li[3]/a').click()  # Usuarios seguidos

        assert 'rarrebola' not in selenium.page_source

    # Dejar de seguir un usuario que no estaba siendo seguido
    def test17_dejar_de_seguir_usuario_no_seguido(self):
        selenium = self.selenium
        selenium.get('http://localhost:8000/219/seguirRuta/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.implicitly_wait(20)
        selenium.get('http://localhost:8000/107/dejarDeSeguirUsuario/')
        selenium.implicitly_wait(20)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click()  # Mi perfil
        selenium.find_element_by_xpath('/html/body/div/div/ul/li[3]/a').click() # Usuarios seguidos

        assert 'rarrebola' not in selenium.page_source

    # Dejar de seguirse a sí mismo
    def test18_dejar_seguirse_si_mismo(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        selenium.get('http://localhost:8000/107/dejarDeSeguirUsuario/')

        assert 'Seguir' not in selenium.page_source

    # Modificar Perfil correctamente
    def test29_modificar_perfil_correctamente(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click() # Mi perfil
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/a[1]').click() # Editar perfil

        alias = selenium.find_element_by_xpath('//*[@id="id_alias"]')
        antigua_password = selenium.find_element_by_xpath('//*[@id="id_password"]')
        nueva_password =  selenium.find_element_by_xpath('//*[@id="id_nuevaPassword"]')
        confirmacion_password = selenium.find_element_by_xpath('//*[@id="id_confirmacionPassword"]')
        email = selenium.find_element_by_xpath('//*[@id="id_email"]')
        confirmacion_email = selenium.find_element_by_xpath('//*[@id="id_confirmacionEmail"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        alias.clear()
        alias.send_keys('prueba11')
        antigua_password.clear()
        antigua_password.send_keys('12345678')
        nueva_password.send_keys('123456789')
        confirmacion_password.send_keys('123456789')
        email.clear()
        email.send_keys('prueba11@socialroute.com')
        confirmacion_email.send_keys('prueba11@socialroute.com')
        submit.send_keys(Keys.RETURN)

        selenium.implicitly_wait(10)

        assert 'prueba11' in selenium.page_source

    # Cancelar modificacion perfil
    def test19_cancelar_modificar_perfil(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click()  # Mi perfil
        selenium.implicitly_wait(20)
        selenium.find_element_by_xpath('/html/body/a[1]').click()  # Editar perfil
        selenium.find_element_by_xpath('/html/body/div/form/a').click() # Volver
        selenium.implicitly_wait(10)

        assert 'prueba1' in selenium.page_source

    # Modificar perfil sin completar los campos obligatorios
    def test20_modificar_perfil_campos_incompletos(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click()  # Mi perfil
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/a[1]').click()  # Editar perfil

        alias = selenium.find_element_by_xpath('//*[@id="id_alias"]')
        antigua_password = selenium.find_element_by_xpath('//*[@id="id_password"]')
        nueva_password = selenium.find_element_by_xpath('//*[@id="id_nuevaPassword"]')
        confirmacion_password = selenium.find_element_by_xpath('//*[@id="id_confirmacionPassword"]')
        email = selenium.find_element_by_xpath('//*[@id="id_email"]')
        confirmacion_email = selenium.find_element_by_xpath('//*[@id="id_confirmacionEmail"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        alias.clear()
        antigua_password.clear()
        nueva_password.clear()
        confirmacion_password.clear()
        email.clear()
        confirmacion_email.clear()
        submit.send_keys(Keys.RETURN)

        assert 'Editar perfil' in selenium.page_source

    # Modificar perfil introduciendo un alias que ya existe
    def test21_modificar_perfil_alias_existe(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click()  # Mi perfil
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/a[1]').click()  # Editar perfil

        alias = selenium.find_element_by_xpath('//*[@id="id_alias"]')
        antigua_password = selenium.find_element_by_xpath('//*[@id="id_password"]')
        nueva_password = selenium.find_element_by_xpath('//*[@id="id_nuevaPassword"]')
        confirmacion_password = selenium.find_element_by_xpath('//*[@id="id_confirmacionPassword"]')
        email = selenium.find_element_by_xpath('//*[@id="id_email"]')
        confirmacion_email = selenium.find_element_by_xpath('//*[@id="id_confirmacionEmail"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        alias.clear()
        alias.send_keys('rarrebola')
        antigua_password.clear()
        antigua_password.send_keys('12345678')
        nueva_password.clear()
        nueva_password.send_keys('12345678')
        confirmacion_password.clear()
        confirmacion_password.send_keys('12345678')
        email.clear()
        email.send_keys('prueba@socialroute.com')
        confirmacion_email.clear()
        confirmacion_email.send_keys('prueba@socialroute.com')
        submit.send_keys(Keys.RETURN)

        assert 'Ya existe un usuario con ese alias, introduzca otro' in selenium.page_source

    # Modificar el perfil introduciendo una contraseña actual no válida
    def test22_modificar_perfil_password_no_valida(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click()  # Mi perfil
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/a[1]').click()  # Editar perfil

        alias = selenium.find_element_by_xpath('//*[@id="id_alias"]')
        antigua_password = selenium.find_element_by_xpath('//*[@id="id_password"]')
        nueva_password = selenium.find_element_by_xpath('//*[@id="id_nuevaPassword"]')
        confirmacion_password = selenium.find_element_by_xpath('//*[@id="id_confirmacionPassword"]')
        email = selenium.find_element_by_xpath('//*[@id="id_email"]')
        confirmacion_email = selenium.find_element_by_xpath('//*[@id="id_confirmacionEmail"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        alias.clear()
        alias.send_keys('prueba1')
        antigua_password.clear()
        antigua_password.send_keys('asdfasdfasdfadfad')
        nueva_password.clear()
        nueva_password.send_keys('12345678')
        confirmacion_password.clear()
        confirmacion_password.send_keys('12345678')
        email.clear()
        email.send_keys('prueba@socialroute.com')
        confirmacion_email.clear()
        confirmacion_email.send_keys('prueba@socialroute.com')
        submit.send_keys(Keys.RETURN)

        assert 'La contraseña introducida no es válida' in selenium.page_source

    # Modificar perfil cuyas contraseñas no coinciden
    def test23_modificacion_perfil_contraseñas_no_coinciden(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click()  # Mi perfil
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/a[1]').click()  # Editar perfil

        alias = selenium.find_element_by_xpath('//*[@id="id_alias"]')
        antigua_password = selenium.find_element_by_xpath('//*[@id="id_password"]')
        nueva_password = selenium.find_element_by_xpath('//*[@id="id_nuevaPassword"]')
        confirmacion_password = selenium.find_element_by_xpath('//*[@id="id_confirmacionPassword"]')
        email = selenium.find_element_by_xpath('//*[@id="id_email"]')
        confirmacion_email = selenium.find_element_by_xpath('//*[@id="id_confirmacionEmail"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        alias.clear()
        alias.send_keys('prueba1')
        antigua_password.clear()
        antigua_password.send_keys('12345678')
        nueva_password.clear()
        nueva_password.send_keys('11111111')
        confirmacion_password.clear()
        confirmacion_password.send_keys('44444444')
        email.clear()
        email.send_keys('prueba@socialroute.com')
        confirmacion_email.clear()
        confirmacion_email.send_keys('prueba@socialroute.com')
        submit.send_keys(Keys.RETURN)

        assert 'Las contraseñas no coinciden' in selenium.page_source

    # Modificar perfil cuyos emails no coinciden
    def test24_modificar_perfil_emails_no_coinciden(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click()  # Mi perfil
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/a[1]').click()  # Editar perfil

        alias = selenium.find_element_by_xpath('//*[@id="id_alias"]')
        antigua_password = selenium.find_element_by_xpath('//*[@id="id_password"]')
        nueva_password = selenium.find_element_by_xpath('//*[@id="id_nuevaPassword"]')
        confirmacion_password = selenium.find_element_by_xpath('//*[@id="id_confirmacionPassword"]')
        email = selenium.find_element_by_xpath('//*[@id="id_email"]')
        confirmacion_email = selenium.find_element_by_xpath('//*[@id="id_confirmacionEmail"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        alias.clear()
        alias.send_keys('prueba1')
        antigua_password.clear()
        antigua_password.send_keys('12345678')
        nueva_password.clear()
        nueva_password.send_keys('12345678')
        confirmacion_password.clear()
        confirmacion_password.send_keys('12345678')
        email.clear()
        email.send_keys('prueba@socialroute.es')
        confirmacion_email.clear()
        confirmacion_email.send_keys('prueba@socialroute.com')
        submit.send_keys(Keys.RETURN)

        assert 'Los emails no coinciden' in selenium.page_source

    # Modificar perfil e-mail en uso
    def test25_modificar_perfil_email_usado(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click()  # Mi perfil
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/a[1]').click()  # Editar perfil

        alias = selenium.find_element_by_xpath('//*[@id="id_alias"]')
        antigua_password = selenium.find_element_by_xpath('//*[@id="id_password"]')
        nueva_password = selenium.find_element_by_xpath('//*[@id="id_nuevaPassword"]')
        confirmacion_password = selenium.find_element_by_xpath('//*[@id="id_confirmacionPassword"]')
        email = selenium.find_element_by_xpath('//*[@id="id_email"]')
        confirmacion_email = selenium.find_element_by_xpath('//*[@id="id_confirmacionEmail"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        alias.clear()
        alias.send_keys('prueba1')
        antigua_password.clear()
        antigua_password.send_keys('12345678')
        nueva_password.clear()
        nueva_password.send_keys('12345678')
        confirmacion_password.clear()
        confirmacion_password.send_keys('12345678')
        email.clear()
        email.send_keys('rocarrpas@uma.es')
        confirmacion_email.clear()
        confirmacion_email.send_keys('rocarrpas@uma.es')
        submit.send_keys(Keys.RETURN)

        assert 'El email que desea usar ya está siendo usado, introduzca otro' in selenium.page_source

    # Modificar perfil introduciendo una contraseña demasiado corta
    def test26_modificar_perfil_password_demasiado_corta(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click()  # Mi perfil
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/a[1]').click()  # Editar perfil

        alias = selenium.find_element_by_xpath('//*[@id="id_alias"]')
        antigua_password = selenium.find_element_by_xpath('//*[@id="id_password"]')
        nueva_password = selenium.find_element_by_xpath('//*[@id="id_nuevaPassword"]')
        confirmacion_password = selenium.find_element_by_xpath('//*[@id="id_confirmacionPassword"]')
        email = selenium.find_element_by_xpath('//*[@id="id_email"]')
        confirmacion_email = selenium.find_element_by_xpath('//*[@id="id_confirmacionEmail"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        alias.clear()
        alias.send_keys('prueba1')
        antigua_password.clear()
        antigua_password.send_keys('12345678')
        nueva_password.clear()
        nueva_password.send_keys('1')
        confirmacion_password.clear()
        confirmacion_password.send_keys('1')
        email.clear()
        email.send_keys('prueba@socialroute.com')
        confirmacion_email.clear()
        confirmacion_email.send_keys('prueba@socialroute.com')
        submit.send_keys(Keys.RETURN)

        assert 'Este campo debe tener al menos 8 caracteres' in selenium.page_source

    # Modificar perfil introduciendo un e-mail sin arroba
    def test27_modificar_perfil_email_erroneo(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click()  # Mi perfil
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/a[1]').click()  # Editar perfil

        alias = selenium.find_element_by_xpath('//*[@id="id_alias"]')
        antigua_password = selenium.find_element_by_xpath('//*[@id="id_password"]')
        nueva_password = selenium.find_element_by_xpath('//*[@id="id_nuevaPassword"]')
        confirmacion_password = selenium.find_element_by_xpath('//*[@id="id_confirmacionPassword"]')
        email = selenium.find_element_by_xpath('//*[@id="id_email"]')
        confirmacion_email = selenium.find_element_by_xpath('//*[@id="id_confirmacionEmail"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        alias.clear()
        alias.send_keys('prueba1')
        antigua_password.clear()
        antigua_password.send_keys('12345678')
        nueva_password.clear()
        nueva_password.send_keys('12345678')
        confirmacion_password.clear()
        confirmacion_password.send_keys('12345678')
        email.clear()
        email.send_keys('pruebasocialroute.com')
        confirmacion_email.clear()
        confirmacion_email.send_keys('pruebasocialroute.com')
        submit.send_keys(Keys.RETURN)

        assert 'Introduzca un e-mail válido' in selenium.page_source

    # Modificar perfil introduciendo caracteres no alfanumericos en el alias
    def test28_modificar_perfil_alias_no_alfanumerico(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba1')
        password.send_keys('12345678')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click()  # Mi perfil
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/a[1]').click()  # Editar perfil

        alias = selenium.find_element_by_xpath('//*[@id="id_alias"]')
        antigua_password = selenium.find_element_by_xpath('//*[@id="id_password"]')
        nueva_password = selenium.find_element_by_xpath('//*[@id="id_nuevaPassword"]')
        confirmacion_password = selenium.find_element_by_xpath('//*[@id="id_confirmacionPassword"]')
        email = selenium.find_element_by_xpath('//*[@id="id_email"]')
        confirmacion_email = selenium.find_element_by_xpath('//*[@id="id_confirmacionEmail"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        alias.clear()
        alias.send_keys('prueba1?')
        antigua_password.clear()
        antigua_password.send_keys('12345678')
        nueva_password.clear()
        nueva_password.send_keys('12345678')
        confirmacion_password.clear()
        confirmacion_password.send_keys('12345678')
        email.clear()
        email.send_keys('prueba@socialroute.com')
        confirmacion_email.clear()
        confirmacion_email.send_keys('prueba@socialroute.com')
        submit.send_keys(Keys.RETURN)

        assert 'Solo se permiten caracteres alfanuméricos' in selenium.page_source

    # Cancelar borrado del perfil
    def test30_cancelar_borrar_perfil(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba11')
        password.send_keys('123456789')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click()  # Mi perfil
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/a[2]').click() # Eliminar perfil
        selenium.switch_to.alert.dismiss()

        assert 'prueba11' in selenium.page_source

    # Borrar perfil correctamente
    def test31_borrar_perfil(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba11')
        password.send_keys('123456789')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/a').click()  # Mi perfil
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/a[2]').click()  # Eliminar perfil
        selenium.switch_to.alert.accept()

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('prueba11')
        password.send_keys('123456789')
        submit.send_keys(Keys.RETURN)

        assert 'Usuario o contraseña no válido(s)' in selenium.page_source
