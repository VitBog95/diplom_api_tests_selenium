import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://teachers.skyeng.ru"
SESSION_FILE = "session.json"

options = Options()
options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

print("🌐 Открываем Skyeng...")
driver.get(BASE_URL)

print("=" * 60)
print("🔑 Войди в аккаунт ВРУЧНУЮ:")
print("   1. Введи логин и пароль")
print("   2. Дождись загрузки расписания")
print("=" * 60)
print("⏳ Нажми ENTER, когда увидишь расписание.")
input()

print(f"📌 Итоговый URL: {driver.current_url}")

cookies = driver.get_cookies()
session_data = {"cookies": cookies, "origins": []}

with open(SESSION_FILE, "w", encoding="utf-8") as f:
    json.dump(session_data, f, ensure_ascii=False, indent=2)

print(f"✅ Сессия сохранена в {SESSION_FILE}")
driver.quit()
