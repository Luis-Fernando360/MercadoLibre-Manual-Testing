
from pages import UrbanRoutesPage
from helpers import retrieve_phone_code
import data
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(service=Service(), options=chrome_options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)  # Vamos a abrir el explorador
        routes_page = UrbanRoutesPage(self.driver) # Estamos generando una instancia
        # 1 Configurar ruta
        address_from = data.address_from  #addres_from: 'East 2nd Street. 601'
        address_to = data.address_to    #addres_to: '1300 1st St'
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

        # 2. Selección tarifa Comfort
        routes_page.select_comfort_rate()
        assert routes_page.is_comfort_selected() == data.comfort_selected

        # 3. Teléfono
        routes_page.set_phone_number(data.phone_number)
        phone_confirmation_result = routes_page.phone_confirm_code()
        assert phone_confirmation_result == data.phone_confirm_code

        # 4. Tarjeta
        card_result = routes_page.add_credit_card(data.card_number, data.card_code)
        assert card_result == True

        # 5. Mensaje al conductor
        routes_page.set_driver_message(data.message_for_driver)
        assert routes_page.get_driver_message() == data.message_for_driver

        # 6. Servicios
        routes_page.order_blanket_and_tissues()
        expected_ice_creams =2
        routes_page.order_ice_creams(expected_ice_creams)
        assert routes_page.order_ice_creams() == expected_ice_creams

        # 7. Pedir taxi
        routes_page.order_taxi()
        assert routes_page.order_taxi() == True

        # 8. Modal de búsqueda
        assert routes_page.is_searching_modal_displayed()

        # 9. Información del conductor (opcional)
        if routes_page.is_driver_info_displayed():
            print("✅ Información del conductor verificada")


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
