import gspread
import logging
from config import spreadsheet_url, credentials_path

logger = logging.getLogger()

gc = gspread.service_account(filename=credentials_path)

try:
    spreadsheet = gc.open_by_url(spreadsheet_url)
    logging.info("Подключение к Google Sheets успешно.")
except Exception as e:
    logging.error(f"Ошибка при подключении к Google Sheets: {e}")
    raise

sheet = spreadsheet.sheet1

def insert_flats_data(flats):
    try:
        logging.info("Очищение листа и добавление новых данных.")
        sheet.clear()
        sheet.append_row(["Комнатность", "Цена", "Ссылка"])

        for flat in flats:
            room = flat.get('rooms', 'Не указано')
            price = flat.get('price', 'Не указана')
            link = flat.get('link', 'Нет ссылки')
            
            logging.info(f"Добавление данных: {room}, {price}, {link}")
            sheet.append_row([room, price, link])

        logging.info(f"Данные успешно добавлены в таблицу. Всего добавлено {len(flats)} записей.")
    except Exception as e:
        logging.error(f"Ошибка при вставке данных в таблицу: {e}")