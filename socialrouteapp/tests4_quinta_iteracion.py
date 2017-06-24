from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create your tests here.
class TestsQuintaIteracion(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(TestsQuintaIteracion, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(TestsQuintaIteracion, self).tearDown()

    # Cancelar el borrado de lugares de interés de días
    def test01_cancelar_quitar_lugar_interes_dia(self):
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
        selenium.find_element_by_xpath('/html/body/div[3]/div/table/tbody/tr[1]/td[2]/a/span').click() # Quitar LI de día
        selenium.switch_to.alert.dismiss()

        assert 'Guiness Storehouse' in selenium.page_source

    # Borrar correctamente un lugar de interés de un día
    def test02_quitar_lugar_interes_dia(self):
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
        selenium.find_element_by_xpath(
            '/html/body/div[3]/div/table/tbody/tr[1]/td[2]/a/span').click()  # Quitar LI de día
        selenium.switch_to.alert.accept()

        assert 'Guiness Storehouse' not in selenium.page_source

    # Recuperar contraseña correctamente
    def test03_recuperar_password_correctamente(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        selenium.find_element_by_xpath('/html/body/div/form/a').click() # He olvidado mi contraseña

        email = selenium.find_element_by_xpath('//*[@id="id_email"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]') #Enviar

        email.send_keys('rocarrpas@uma.es')
        submit.send_keys(Keys.RETURN)

        alias = selenium.find_element_by_id('id_alias')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Iniciar sesión

        alias.send_keys('rarrebola')
        password.send_keys('incendiosdenieve')
        submit.send_keys(Keys.RETURN)

        assert 'Usuario o contraseña no válido(s)' in selenium.page_source

    # Recuperar contraseña e-mail vacío
    def test04_recuperar_password_email_vacio(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        selenium.find_element_by_xpath('/html/body/div/form/a').click()  # He olvidado mi contraseña

        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Enviar

        submit.send_keys(Keys.RETURN)

        assert 'Recuperación de la contraseña' in selenium.page_source

    # Recuperar contraseña e-mail sin cuenta en el sistema
    def test05_email_no_en_sistema(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        selenium.find_element_by_xpath('/html/body/div/form/a').click()  # He olvidado mi contraseña

        email = selenium.find_element_by_xpath('//*[@id="id_email"]')
        submit = selenium.find_element_by_xpath('/html/body/div/form/input[2]')  # Enviar

        email.send_keys('rocioarrebola95@uma.es')
        submit.send_keys(Keys.RETURN)

        assert 'No existen usuarios con el email indicado' in selenium.page_source



