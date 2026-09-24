from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage


class SchedulePage(BasePage):
    """Page Object для страницы расписания"""

    SCHEDULE_LINK = (By.XPATH, "//a[contains(@href, '/schedule')]")
    WEEK_LABEL = (By.XPATH, "//*[contains(text(), '–')]")
    DAY_LABEL = (By.XPATH, "//*[contains(text(), 'Пон') or contains(text(), 'Вт') or contains(text(), 'Ср')]")
    BUTTON = (By.TAG_NAME, "button")
    ERROR_TEXT = (By.XPATH, "//*[contains(text(), 'Ошибка')]")

    def open(self):
        """Открыть страницу расписания"""
        self.driver.get("https://teachers.skyeng.ru")
        return self

    def is_schedule_tab_visible(self) -> bool:
        """Проверить, что вкладка «Расписание» видна"""
        return self.find_visible(*self.SCHEDULE_LINK).is_displayed()

    def is_week_label_visible(self) -> bool:
        """Проверить, что отображается текущая неделя"""
        return self.find_visible(*self.WEEK_LABEL).is_displayed()

    def is_day_label_visible(self) -> bool:
        """Проверить, что отображаются дни недели"""
        return self.find_visible(*self.DAY_LABEL).is_displayed()

    def are_buttons_visible(self) -> bool:
        """Проверить, что на странице есть кнопки"""
        return len(self.find_all(*self.BUTTON)) > 0

    def has_no_errors(self) -> bool:
        """Проверить, что нет ошибок на странице"""
        return len(self.find_all(*self.ERROR_TEXT)) == 0

    def has_day_of_week(self) -> bool:
        """Проверить, что хотя бы один день недели присутствует"""
        days = ["Пон", "Вт", "Ср", "Чт", "Пт", "Суб", "Вс"]
        for day in days:
            if len(self.find_all(By.XPATH, f"//*[contains(text(), '{day}')]")) > 0:
                return True
        return False
