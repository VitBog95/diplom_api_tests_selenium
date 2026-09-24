from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Базовый класс для всех Page Object'ов"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def find(self, by, value):
        """Найти элемент с ожиданием появления"""
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def find_visible(self, by, value):
        """Найти видимый элемент"""
        return self.wait.until(EC.visibility_of_element_located((by, value)))

    def find_all(self, by, value):
        """Найти все элементы"""
        return self.driver.find_elements(by, value)

    def get_current_url(self):
        """Получить текущий URL"""
        return self.driver.current_url
