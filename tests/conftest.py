import os
import json
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from tests.pages.schedule_page import SchedulePage

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
                except Exception:
                    pass

    driver.get(BASE_URL)
    WebDriverWait(driver, 15).until(lambda d: "login" not in d.current_url)

    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def schedule_page(driver):
    """Возвращает объект страницы расписания"""
    return SchedulePage(driver)