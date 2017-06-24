from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# Create your tests here.
class TestsCuartaIteracion(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(TestsCuartaIteracion, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(TestsCuartaIteracion, self).tearDown()

    # Crear lugares de interés correctamente
    def test01_crear_lugar_interes_correctamente(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="dropdownMenu1"]').click() # Button Dropdown del Navbar
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/div/ul/li[2]/a').click() # Crear lugar de interés

        nombre = selenium.find_element_by_xpath('//*[@id="id_nombre"]')
        direccion = selenium.find_element_by_xpath('//*[@id="id_direccion"]')
        localidad = selenium.find_element_by_xpath('//*[@id="id_localidad"]')
        descripcion = selenium.find_element_by_xpath('//*[@id="id_descripcion"]')
        horario = selenium.find_element_by_xpath('//*[@id="id_horario"]')
        precio = selenium.find_element_by_xpath('//*[@id="id_precio"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        nombre.send_keys('Castillo de Gibralfaro')
        direccion.send_keys('Castillo de Gibralfaro')
        localidad.send_keys('Málaga')
        descripcion.send_keys('El castillo de Gibralfaro o alcázar de Gibralfaro es una fortificación situada en la ciudad española de Málaga')
        horario.send_keys('Todos los días de 9:00 a 20:00')
        precio.send_keys('5.00')
        submit.send_keys(Keys.RETURN)

        assert 'Timeline' in selenium.page_source

    # Cancelar crear lugar de interés
    def test02_cancelar_crear_lugar_interes(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="dropdownMenu1"]').click()  # Button Dropdown del Navbar
        selenium.find_element_by_xpath(
            '//*[@id="bs-example-navbar-collapse-1"]/ul/div/ul/li[2]/a').click()  # Crear lugar de interés
        selenium.find_element_by_xpath('/html/body/div/form/a').click() # Volver

        assert 'Timeline' in selenium.page_source

    # Crear lugar de interés con los campos obligatorios vacíos
    def test03_crear_lugar_interes_campos_vacios(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="dropdownMenu1"]').click()  # Button Dropdown del Navbar
        selenium.find_element_by_xpath(
            '//*[@id="bs-example-navbar-collapse-1"]/ul/div/ul/li[2]/a').click()  # Crear lugar de interés

        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        submit.send_keys(Keys.RETURN)

        assert 'Crear lugar de interés' in selenium.page_source

    # Crear un lugar de interés que ya existe
    def test04_crear_lugar_interes_ya_existe(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="dropdownMenu1"]').click()  # Button Dropdown del Navbar
        selenium.find_element_by_xpath(
            '//*[@id="bs-example-navbar-collapse-1"]/ul/div/ul/li[2]/a').click()  # Crear lugar de interés

        nombre = selenium.find_element_by_xpath('//*[@id="id_nombre"]')
        direccion = selenium.find_element_by_xpath('//*[@id="id_direccion"]')
        localidad = selenium.find_element_by_xpath('//*[@id="id_localidad"]')
        descripcion = selenium.find_element_by_xpath('//*[@id="id_descripcion"]')
        horario = selenium.find_element_by_xpath('//*[@id="id_horario"]')
        precio = selenium.find_element_by_xpath('//*[@id="id_precio"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')

        nombre.send_keys('Castillo de Gibralfaro')
        direccion.send_keys('Castillo de Gibralfaro')
        localidad.send_keys('Málaga')
        descripcion.send_keys(
            'El castillo de Gibralfaro o alcázar de Gibralfaro es una fortificación situada en la ciudad española de Málaga')
        horario.send_keys('Todos los días de 9:00 a 20:00')
        precio.send_keys('5.00')
        submit.send_keys(Keys.RETURN)

        assert 'El lugar de interés ya existe' in selenium.page_source

    # Modificar lugar de interés correctamente
    def test05_modificar_lugar_interes_correctamente(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('Castillo de Gibralfaro')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click() # Lupa
        selenium.find_element_by_xpath('/html/body/div/ul/li[3]/a').click() # Lugares de interés
        selenium.find_element_by_xpath('//*[@id="lugares_de_interes"]/ul/li[1]/a').click() # Primer lugar de interés de la lista
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/div[2]/a[2]').click() # Editar

        descripcion = selenium.find_element_by_xpath('//*[@id="id_descripcion"]')
        horario = selenium.find_element_by_xpath('//*[@id="id_horario"]')
        precio = selenium.find_element_by_xpath('//*[@id="id_precio"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]') # Guardar

        descripcion.clear()
        descripcion.send_keys('Descripción modificada')
        horario.clear()
        horario.send_keys('Horario modificado')
        precio.clear()
        precio.send_keys('2')

        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('Castillo de Gibralfaro')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa
        selenium.find_element_by_xpath('/html/body/div/ul/li[3]/a').click()  # Lugares de interés
        selenium.find_element_by_xpath(
            '//*[@id="lugares_de_interes"]/ul/li[1]/a').click()  # Primer lugar de interés de la lista
        selenium.implicitly_wait(10)

        assert 'Descripción modificada' in selenium.page_source

    # Cancelar modificación lugar de interés
    def test06_cancelar_modificar_lugar_interes(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('Castillo de Gibralfaro')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa
        selenium.find_element_by_xpath('/html/body/div/ul/li[3]/a').click()  # Lugares de interés
        selenium.find_element_by_xpath(
            '//*[@id="lugares_de_interes"]/ul/li[1]/a').click()  # Primer lugar de interés de la lista
        selenium.find_element_by_xpath('/html/body/div[2]/a[2]').click()  # Editar
        selenium.find_element_by_xpath('/html/body/div/form/a').click() # Volver
        selenium.implicitly_wait(10)
        assert 'Valoraciones' in selenium.page_source

    # Modificar lugar de interés sin completar los campos obligatorios
    def test07_modificar_lugar_interes_campos_obligatorios_vacios(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('Castillo de Gibralfaro')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa
        selenium.find_element_by_xpath('/html/body/div/ul/li[3]/a').click()  # Lugares de interés
        selenium.find_element_by_xpath(
            '//*[@id="lugares_de_interes"]/ul/li[1]/a').click()  # Primer lugar de interés de la lista
        selenium.find_element_by_xpath('/html/body/div[2]/a[2]').click()  # Editar

        descripcion = selenium.find_element_by_xpath('//*[@id="id_descripcion"]')
        horario = selenium.find_element_by_xpath('//*[@id="id_horario"]')
        precio = selenium.find_element_by_xpath('//*[@id="id_precio"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Guardar

        descripcion.clear()
        horario.clear()
        precio.clear()

        submit.send_keys(Keys.RETURN)

        assert 'Castillo de Gibralfaro' in selenium.page_source and 'Valoraciones' not in selenium.page_source

    # Valorar ruta correctamente
    def test08_valorar_ruta_correctamente(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('Flandes')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa
        selenium.find_element_by_xpath('//*[@id="rutas"]/ul/li/a').click() # Primera ruta de la lista

        puntuacion = selenium.find_element_by_xpath('//*[@id="id_puntuacion"]')
        comentario = selenium.find_element_by_xpath('//*[@id="id_comentario"]')
        submit = selenium.find_element_by_xpath('//*[@id="form-valoracion-ruta"]/input[3]') # Valorar

        puntuacion.send_keys('9')
        comentario.send_keys('Comentario de la ruta')
        submit.send_keys(Keys.RETURN)

        assert 'Comentario de la ruta' in selenium.page_source

    # Valorar ruta campos vacíos
    def test09_valorar_ruta_campos_vacios(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('Flandes')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa
        selenium.find_element_by_xpath('//*[@id="rutas"]/ul/li/a').click()  # Primera ruta de la lista

        submit = selenium.find_element_by_xpath('//*[@id="form-valoracion-ruta"]/input[3]')  # Valorar

        submit.send_keys(Keys.RETURN)

        assert 'Valoraciones' in selenium.page_source

    # Cancelar borrado de comentario
    def test10_cancelar_borrar_comentario_ruta(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('Flandes')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa
        selenium.find_element_by_xpath('//*[@id="rutas"]/ul/li/a').click()  # Primera ruta de la lista

        selenium.find_element_by_xpath('//*[@id="panel-valoraciones"]/div[2]/a').click() # Borrar comentario
        selenium.switch_to.alert.dismiss()

        assert 'Comentario de la ruta' in selenium.page_source

    # Borrar comentario
    def test11_borrar_comentario_ruta(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('Flandes')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa
        selenium.find_element_by_xpath('//*[@id="rutas"]/ul/li/a').click()  # Primera ruta de la lista
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('//*[@id="panel-valoraciones"]/div[2]/a').click()  # Borrar comentario
        selenium.switch_to.alert.accept()

        assert 'Comentario de la ruta' not in selenium.page_source

    # Valorar lugar de interés correctamente
    def test12_valorar_lugar_interes_correctamente(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('Manneken Pis')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa
        selenium.find_element_by_xpath('/html/body/div/ul/li[3]/a').click() # Lugares de interés
        selenium.find_element_by_xpath('//*[@id="lugares_de_interes"]/ul/li/a').click() # Primer lugar de interés de la lista

        puntuacion = selenium.find_element_by_xpath('//*[@id="id_puntuacion"]')
        comentario = selenium.find_element_by_xpath('//*[@id="id_comentario"]')
        submit = selenium.find_element_by_xpath('//*[@id="form-valoracion-li"]/input[3]') # Valorar

        puntuacion.send_keys('9')
        comentario.send_keys('Comentario de lugar de interés')
        submit.send_keys(Keys.RETURN)

        assert 'Comentario de lugar de interés' in selenium.page_source

    # Valorar lugar de interés sin completar los campos obligatorios
    def test13_valorar_lugar_interes_campos_vacios(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('Manneken Pis')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa
        selenium.find_element_by_xpath('/html/body/div/ul/li[3]/a').click()  # Lugares de interés
        selenium.find_element_by_xpath(
            '//*[@id="lugares_de_interes"]/ul/li/a').click()  # Primer lugar de interés de la lista

        submit = selenium.find_element_by_xpath('//*[@id="form-valoracion-li"]/input[3]')  # Valorar

        submit.send_keys(Keys.RETURN)

        assert 'Valoraciones' in selenium.page_source

    # Cancelar el borrado de una valoración en un lugar de interés
    def test14_cancelar_borrar_valoracion_lugar_interes(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('Manneken Pis')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa
        selenium.find_element_by_xpath('/html/body/div/ul/li[3]/a').click()  # Lugares de interés
        selenium.find_element_by_xpath(
            '//*[@id="lugares_de_interes"]/ul/li/a').click()  # Primer lugar de interés de la lista

        selenium.find_element_by_xpath('/html/body/div[4]/div[2]/a').click() #Borrar comentario
        selenium.switch_to.alert.dismiss()

        assert 'Comentario de lugar de interés' in selenium.page_source

    # Borrar la valoración de un lugar de interés
    def test15_borrar_valoracion_lugar_interes(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('Manneken Pis')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa
        selenium.find_element_by_xpath('/html/body/div/ul/li[3]/a').click()  # Lugares de interés
        selenium.find_element_by_xpath(
            '//*[@id="lugares_de_interes"]/ul/li/a').click()  # Primer lugar de interés de la lista
        selenium.implicitly_wait(10)
        selenium.find_element_by_xpath('/html/body/div[4]/div[2]/a').click()  # Borrar comentario
        selenium.switch_to.alert.accept()

        assert 'Comentario de lugar de interés' not in selenium.page_source

    # Búsqueda lugares de interés exitosa
    def test16_busqueda_lugar_interes_exitosa(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('Manneken Pis')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa
        selenium.find_element_by_xpath('/html/body/div/ul/li[3]/a').click()  # Lugares de interés
        selenium.find_element_by_xpath('//*[@id="lugares_de_interes"]/ul/li/a').click() # Primer lugar de interés de la lista

        assert 'Manneken Pis' in selenium.page_source

    # Búsqueda lugares de interés parámetro vacío
    def test17_busqueda_lugares_interes_parametro_vacio(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa

        assert 'Timeline' in selenium.page_source

    # Búsqueda lugares de interés sin coincidencias
    def test18_busqueda_lugares_interes_sin_coincidencias(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        busqueda = selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/div/input')
        busqueda.send_keys('asdfa')
        selenium.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/form/button').click()  # Lupa
        selenium.find_element_by_xpath('/html/body/div/ul/li[3]/a').click()  # Lugares de interés

        assert 'No se han encontrado coincidencias' in selenium.page_source

    # Añadir lugares de interés a días correctamente
    def test19_add_lugares_interes_dia_correctamente(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath('//*[@id="rutas_creadas"]/div/table/tbody/tr[1]/td/a').click() #Primera ruta de la lista de rutas creadas
        selenium.find_element_by_xpath('/html/body/div[2]/div/table/tbody/tr[1]/td[1]/a').click() # Primer día de la lista de días de la ruta

        ciudad = selenium.find_element_by_xpath('//*[@id="buscar-li"]/input[3]')
        submit = selenium.find_element_by_xpath('//*[@id="buscar-li"]/button/span') # buscar ciudad

        ciudad.send_keys('Amberes')
        submit.send_keys(Keys.RETURN)

        select = Select(selenium.find_element_by_xpath('/html/body/form[2]/select'))
        submit = selenium.find_element_by_xpath('/html/body/form[2]/input[3]')  # Añadir

        select.select_by_index(0)
        submit.send_keys(Keys.RETURN)

        assert 'Añadir' not in selenium.page_source

    # Añadir lugares de interés a días con la búsqueda vacía
    def test20_add_lugares_interes_dias_busqueda_vacia(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        selenium.find_element_by_xpath(
            '//*[@id="rutas_creadas"]/div/table/tbody/tr[1]/td/a').click()  # Primera ruta de la lista de rutas creadas
        selenium.find_element_by_xpath(
            '/html/body/div[2]/div/table/tbody/tr[1]/td[1]/a').click()  # Primer día de la lista de días de la ruta
        selenium.find_element_by_xpath('/html/body/form[2]/input[3]').click()

        assert 'Añadir' not in selenium.page_source
