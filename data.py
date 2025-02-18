import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

logger.addHandler(console_handler)

def get_cheapest_flats_by_rooms(room_number):
    url = f"https://www.mr-group.ru/flats/zhk-paveletskaya-siti/rooms-{room_number}/?sort=price_asc"
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Подмена User-Agent
    chrome_options.add_argument("--disable-dev-shm-usage")  

    service = Service(executable_path='')  
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url) 

    logger.info(f"Получение данных для комнат: {room_number}")

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a._wrapper_18ebo_8"))
        )
    except TimeoutException:
        logger.error(f"Время ожидания истекло для комнат {room_number}")
        driver.quit()
        return []
    
    soup = BeautifulSoup(driver.page_source, "html.parser")  
    driver.quit()  

    flats = []

    for flat in soup.select("a._wrapper_18ebo_8"):  
        try:
            link = "https://www.mr-group.ru" + flat["href"]
            rooms = flat.select_one("span._offerTitle_hbl86_1244").text.strip().replace('\xa0', ' ')
            price = flat.select_one("div._currentPrice_hbl86_1288").text.strip()

            flats.append({
                "link": link,
                "rooms": rooms,
                "price": re.sub(r'\D', '', price)
            })
        except AttributeError as e:
            logger.error(f"Ошибка извлечения данных: {e}")
            continue

    flats = sorted(flats, key=lambda x: int(x["price"]))
    logger.info(f"Найдено {len(flats)} квартир для комнатности {room_number}.")

    return flats[:3]
