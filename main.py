from config import room_keys
from data import get_cheapest_flats_by_rooms
from gdrive import insert_flats_data
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_data():
    data = []
    logging.info(f"Начало парсинга данных для комнат: {room_keys}")
    for i in room_keys:
        flats_data = get_cheapest_flats_by_rooms(i)
        for flat in flats_data:
            data.append(flat)
    
    logging.info(f"Всего собрано {len(data)} квартир.")
    insert_flats_data(data)

if __name__ == "__main__":
    try:
        logging.info("Начало выполнения парсинга данных.")
        parse_data()
        logging.info("Данные успешно добавлены в таблицу.")
    except Exception as e:
        logging.error(f"Ошибка при парсинге данных: {e}")