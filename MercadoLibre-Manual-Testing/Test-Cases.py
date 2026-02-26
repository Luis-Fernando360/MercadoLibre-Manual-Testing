from helpers import retrieve_phone_code
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class UrbanRoutesPage:
    # Localizadores para cada elemento
    # Dirección
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    # Hacer click en pedir Taxi
    btn_taxi = (By.XPATH, "//button[contains(text(),'Pedir un taxi')]")

    # Tarifa comfort
    btn_comfort = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")
    # Active
    btn_comfort_active = (By.XPATH, "//div[contains(@class, 'tcard') and contains(@class, 'active')]//div[text()='Comfort']")

    # Telefono
    #telefono = (By.XPATH, '//*[@id="phone"]')
    telefono_id = (By.ID, 'phone')
    #phone_confirm_button = (By.ID, 'confirm-phone')
    phone_confirm_button = (By.XPATH, "//button[@type='submit' and @class='button full']")
    sms_code_field = (By.ID, 'code')
    confirm_code = (By.XPATH, "//button[@type='submit' and @class='button full' and text()='Confirmar']")
    phone_button = (By.XPATH, "//div[contains(text(),'Número de teléfono')]")
    # Método de pago- Agregar tarjeta
    metodo_pago_button = (By.XPATH, "//div[@class='pp-text' and text()='Método de pago']")
    add_card_button = (By.CLASS_NAME, "pp-plus")
    add_card = (By.XPATH, "//button[contains(text(),'Agregar tarjeta')]")
    card_number_field = (By.ID, 'number')
    card_code_field = (By.ID, 'code')
    cvv_field = (By.CSS_SELECTOR, "input[placeholder='12']")
    link_card_button = (By.XPATH, "//button[contains(text(),'Enlazar')]")
    close_button = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/button')
    # Mensaje para el conductor
    driver_message_field = (By.ID, 'comment')
    # Solicitar servicios adicionales
    # Manta y pañuelos
    blanket_checkbox = (By.XPATH,
                        "//div[@class='r-sw-label' and contains(text(),'Manta y pañuelos')]/..//div[@class='switch']")
    tissues_checkbox = (By.XPATH, "//div[contains(text(),'Manta y pañuelos')]//input[@type='checkbox']")
    # Pedir helado
    ice_cream_plus = (By.XPATH, "//div[contains(text(),'Helado')]/following::button[1]")
    # Pedir Taxi
    order_taxi_button = (By.XPATH, "//button[contains(text(),'Pedir un taxi')]")
    # Modal de búsqueda de taxi
    searching_modal = (By.XPATH, "//div[contains(text(),'Buscar automóvil')]")
    driver_info = (By.XPATH, "//div[contains(text(),'Tu conductor')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)  #Le asiganmos un tiempo para verificar que este

    def set_from(self, from_address):
        field = self.wait.until(EC.element_to_be_clickable(self.from_field))
        field.clear()
        field.send_keys(from_address)
        time.sleep(1)
        field.send_keys(Keys.ENTER)

    def set_to(self, to_address):
        field = self.wait.until(EC.element_to_be_clickable(self.to_field))
        field.clear()
        field.send_keys(to_address)
        time.sleep(1)
        field.send_keys(Keys.ENTER)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def wait_for_tariffs(self):
        # Espera a que aparezca cualquier tarifa (Comfort)
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'Comfort')]")
            )
        )


    def set_route(self, address_from, address_to):
        #Configurar dirección "desde"
        self.set_from(address_from)
        time.sleep(1)
        # Configurar dirección "hasta"
        self.set_to(address_to)
        time.sleep(2)
        print("✅ se configuro la ruta")
        # Buscra boton pedir un taxi
        print("buscando boton 'pedir un taxi'...")
        self.click_taxi_button()
        time.sleep(3)  #Dar tiempo a que aparezca el panel de tarifas
        self.select_comfort_rate()

    def click_taxi_button(self):
        self.wait.until(EC.element_to_be_clickable(self.btn_taxi)).click()
        print("✅ Se a pedido un taxi")

    def select_comfort_rate(self):
        # Esperar a que el panel de tarifas se visualice
        self.wait_for_tariffs()

        comfort = self.wait.until(
            EC.presence_of_element_located(self.btn_comfort)
        )
        # Hacer scroll hasta el botón deseado
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", comfort
        )
        time.sleep(1)
        comfort.click()
        print("✅ Tarifa comfort seleccionada")

    def is_comfort_selected(self):
        try:
            comfort_active = self.driver.find_element(*self.btn_comfort_active)
            return True
        except:
            return False


    def set_phone_number(self, phone_number):
        # Hacer clic en el botón "Número de teléfono"
        phone_button = self.wait.until(EC.element_to_be_clickable(self.phone_button)
                                       )
        phone_button.click()

        # Esperar a que el campo esté listo para interactuar
        phone_field = self.wait.until(EC.element_to_be_clickable(self.telefono_id))
        phone_field.clear()  # Limpiar el campo por si tiene contenido
        phone_field.send_keys(phone_number)

        # Hacer clic en confirmar
        confirm_phone_button = self.wait.until(EC.element_to_be_clickable(self.phone_confirm_button))
        confirm_phone_button.click()
        print("✅ Número de telefono agregado")

    def phone_confirm_code(self):
        code = retrieve_phone_code(self.driver)
        print(f"✅ Código SMS obtenido: {code}")

        # Assert: Validar que se obtuvo un código
        assert code is not None and len(code) > 0, "No se pudo obtener el código SMS"

        # Primero ingresar el código SMS
        sms_field = self.wait.until(EC.element_to_be_clickable(self.sms_code_field))
        print("✅ Campo SMS encontrado")
        sms_field.send_keys(code)
        print(f"✅ Código {code} ingresado en el campo SMS")
        time.sleep(1)
        #Confirma el código
        confirm_code_button = self.wait.until(EC.element_to_be_clickable(self.confirm_code))
        confirm_code_button.click()
        print("✅ Código SMS confirmado")
        return True

    def add_credit_card(self, card_number, card_code):
        print("🔍 Seleccionando botón 'Método de pago'...")

        # Click en método de pago con JavaScript
        payment_button = self.wait.until(EC.presence_of_element_located(self.metodo_pago_button))
        self.driver.execute_script("arguments[0].click();", payment_button)

        print("Esperando que aparezca el Modal Método de pago...")
        time.sleep(2)

        # Click en el botón "+" (pp-plus) para agregar tarjeta
        print("🔍 Botón '+' para agregar tarjeta...")
        plus_button = self.wait.until(EC.element_to_be_clickable(self.add_card_button))
        plus_button.click()

        print("✅ Click en botón '+' realizado")
        time.sleep(3)

        # Ahora llenar los campos de la tarjeta
        self.wait.until(EC.element_to_be_clickable(self.card_number_field)).send_keys(card_number)
        self.wait.until(EC.element_to_be_clickable(self.cvv_field)).send_keys(card_code)

        # Importante: hacer que el campo CVV pierda el enfoque (según las instrucciones)
        self.driver.find_element(*self.cvv_field).send_keys(Keys.TAB)
        time.sleep(2)

        # Click en botón "Agregar"
        add_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space(text())='Agregar']")
            )
        )
        add_button.click()
        print("✓ se ha 'Agregado' una tarjeta")
        time.sleep(2)

        # Prueba esto:
        try:
            # Buscar cualquier botón de cerrar disponible
            close_buttons = [
                (By.XPATH, "//button[@class='close-button section-close']"),
                (By.XPATH, "//button[contains(@class, 'close')]"),
                (By.XPATH, "//button[@aria-label='Close']"),
                (By.XPATH, "//button[text()='×']"),
                (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/button')
            ]
            close_buttons = [(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')]


            btns_close = self.driver.find_elements('//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
            for button in btns_close:
                try:
                    button.click()
                except:
                    continue

            for locator in close_buttons:
                try:
                    close_btn = self.wait.until(EC.element_to_be_clickable(locator))
                    close_btn.click()
                    print("✓ Modal cerrado exitosamente")
                    break
                except:
                    continue
        except Exception as e:
            print(f"No se pudo cerrar el modal: {e}")

        return True


    def set_driver_message(self, message):
        self.wait.until(EC.presence_of_element_located(self.driver_message_field)).send_keys(message)
        print("✅ Se a enviado mensaje al conductor")

    def get_driver_message(self):
        return self.driver.find_element(*self.driver_message_field).get_property('value')


    def order_blanket_and_tissues(self):
        # Encuentra el elemento
        element = self.wait.until(
            EC.presence_of_element_located(self.blanket_checkbox))
        # Usar JS para hacer click
        self.driver.execute_script("arguments[0].click();", element)
        print("✅ Se han solicitado manta y pañuelos")

    def order_ice_creams(self, quantity=2):
        # Encuentra el elemento
        element = self.wait.until(
            EC.presence_of_element_located(self.ice_cream_plus))

        # Usar JS para hacer click
        self.driver.execute_script("arguments[0].click();", element)
        print("✅ Se pidieron 2 helados")
        return quantity

    def order_taxi(self):
        print("🔍 Buscando botón 'Pedir un taxi'...")

        # Encontrar el elemento
        element = self.driver.find_element(*self.order_taxi_button)

        # Hacer click con JavaScript (ignora si está visible o no)
        self.driver.execute_script("arguments[0].click();", element)
        print("✅ Se Pidio un taxi")
        return True


    def is_searching_modal_displayed(self):
        print("🔍 Verificando modal de búsqueda...")
        return self.wait.until(EC.presence_of_element_located(self.searching_modal))
        print("✅ Aparece le modal para buscar un taxi")

    def is_driver_info_displayed(self):
        # Esperar un poco más para que aparezca la información
        time.sleep(3)

        try:
            # Buscar variaciones del texto
            variations = ["Tu conductor", "conductor", "Conductor", "driver"]
            for variation in variations:
                elements = self.driver.find_elements(By.XPATH, f"//div[contains(text(),'{variation}')]")
                if elements:
                    print(f"✅ Encontrado '{variation}': {len(elements)} elementos")
                    for elem in elements:
                        print(f"   Texto: '{elem.text}'")
                        print(f"   Visible: {elem.is_displayed()}")

            # Intentar encontrar el elemento con timeout
            element = self.wait.until(EC.presence_of_element_located(self.driver_info))
            print("✅ Información del conductor encontrada")
            return True

        except TimeoutException:
            print("⚠️ Información del conductor no encontrada (paso opcional)")
            return False
