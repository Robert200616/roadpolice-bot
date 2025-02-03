import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot

# === ТВОЙ НОВЫЙ ТОКЕН ТУТ ===
TELEGRAM_BOT_TOKEN = "7853457616:AAGoWCmPDoeQ8c6C_WFg54y9-bx6TvWUhyE"
TELEGRAM_CHAT_ID = "958142174"  # Узнать можно через @userinfobot в Telegram

# === Логирование ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# === Настройки Selenium ===
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск без графического интерфейса
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# === Инициализация Selenium ===
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def check_available_dates():
    logging.info("Проверяю сайт...")
    driver.get("https://roadpolice.am/hy/hqb")

    try:
        # Выбираем "Գործնական" (Практический)
        practical_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Գործնական')]")
        practical_button.click()
        time.sleep(2)

        # Выбираем "Աշտարակի" (Аштaрак)
        dropdown = driver.find_element(By.TAG_NAME, "select")
        dropdown.click()
        option = driver.find_element(By.XPATH, "//option[contains(text(), 'Աշտարակի')]")
        option.click()
        time.sleep(2)

        # Проверяем календарь (февраль и март)
        available_dates = driver.find_elements(By.XPATH, "//td[contains(@class, 'available')]")
        if available_dates:
            message = "⚠️ Появились свободные даты в феврале или марте! Быстрее записывайся: https://roadpolice.am/hy/hqb"
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
            logging.info("Отправлено уведомление в Telegram!")
        else:
            logging.info("Свободных мест пока нет.")

    except Exception as e:
        logging.error(f"Ошибка: {e}")

# Запуск проверки каждые 5 минут
while True:
    check_available_dates()
    time.sleep(300)  # Ждем 5 минут перед новой проверкой
