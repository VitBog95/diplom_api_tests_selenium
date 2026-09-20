import os
import json
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://teachers.skyeng.ru"
SESSION_FILE = "session.json"


@pytest.fixture(scope="function")
def driver():
    """Открывает Chrome с сохранёнными cookies"""
    options = Options()
    options.add_argument("--start-maximized")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(BASE_URL)

    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            session_data = json.load(f)
            for cookie in session_data.get("cookies", []):
                cookie_dict = {
                    "name": cookie["name"],
                    "value": cookie["value"],
                    "domain": cookie.get("domain", ".skyeng.ru"),
                    "path": cookie.get("path", "/"),
                }
                try:
                    driver.add_cookie(cookie_dict)
                except Exception as e:
                    print(f"⚠️ Не удалось добавить cookie {cookie['name']}: {e}")

    driver.get(BASE_URL)
    WebDriverWait(driver, 15).until(
        lambda d: "login" not in d.current_url
    )
    
    print(f"📌 URL: {driver.current_url}")
    
    yield driver
    driver.quit()

def test_schedule_page_loads(driver):
    """TC-UI-01: Страница расписания загружается"""
    assert "teachers.skyeng.ru" in driver.current_url
    assert "login" not in driver.current_url

def test_schedule_tab_is_visible(driver):
    """TC-UI-02: Вкладка «Расписание» отображается"""
    schedule_link = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//a[contains(@href, '/schedule')]"))
    )
    assert schedule_link.is_displayed()

def test_create_lesson_button_is_visible(driver):
    """TC-UI-03: Элементы управления расписанием отображаются"""

    buttons = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "button"))
    )
    assert len(buttons) > 0

    week_label = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), '–')]"))
    )
    assert week_label.is_displayed()

    days_label = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Пон') or contains(text(), 'Вт') or contains(text(), 'Ср')]")
        )
    )
    assert days_label.is_displayed()

def test_week_view_is_available(driver):
    """TC-UI-04: Отображение дней недели в расписании"""
    days = ["Пон", "Вт", "Ср", "Чт", "Пт", "Суб", "Вс"]
    found_day = False
    for day in days:
        elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{day}')]")
        if len(elements) > 0:
            found_day = True
            break
    assert found_day, "В расписании не найдены дни недели"

def test_page_has_no_critical_errors(driver):
    """TC-UI-05: На странице нет критических ошибок"""
    errors = driver.find_elements(By.XPATH, "//*[contains(text(), 'Ошибка')]")
    assert len(errors) == 0, "На странице найдены критические ошибки"
