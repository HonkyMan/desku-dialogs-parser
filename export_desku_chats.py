# export_desku_chats.py
"""
Пример запуска скрипта: 
    export_desku_chats.py --start-date 2025-06-01 --end-date 2025-06-02
"""

from api import create_api_session, get_all_conversations, get_ticket_details
from config import load_configuration
from utils import setup_logging
from settings import FIELDS_TO_KEEP, MSG_FIELDS_TO_KEEP, SENDER_FIELDS_TO_KEEP
import logging
import json
import time
import argparse

def filter_sender_data(sender):
    if not isinstance(sender, dict):
        return sender
    return {k: sender[k] for k in SENDER_FIELDS_TO_KEEP if k in sender}

def filter_msg_data(msg_list):
    if not isinstance(msg_list, list):
        return msg_list
    filtered = []
    for msg in msg_list:
        if not isinstance(msg, dict):
            filtered.append(msg)
            continue
        filtered_msg = {k: msg[k] for k in MSG_FIELDS_TO_KEEP if k in msg}
        # Обработка sender
        if "sender" in filtered_msg:
            filtered_msg["sender"] = filter_sender_data(filtered_msg["sender"])
        filtered.append(filtered_msg)
    return filtered

def filter_ticket_data(ticket_data, fields_to_keep):
    """Фильтрует данные тикета, оставляя только указанные поля."""
    if not fields_to_keep:
        return ticket_data
    filtered = {key: ticket_data[key] for key in fields_to_keep if key in ticket_data}
    # Фильтрация вложенного msg
    if "msg" in filtered and isinstance(filtered["msg"], list):
        filtered["msg"] = filter_msg_data(filtered["msg"])
    return filtered

def save_data_to_json(data, filename="desku_export.json"):
    """Сохраняет данные в JSON-файл."""
    logging.info(f"Сохраняю {len(data)} записей в файл {filename}...")
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"Успешно! Все данные сохранены в {filename}.")
    except IOError as e:
        logging.error(f"Ошибка при записи в файл {filename}: {e}")

def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Экспорт диалогов Desku")
    parser.add_argument('--start-date', type=str, help='Дата начала (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, help='Дата окончания (YYYY-MM-DD)')
    args = parser.parse_args()
    try:
        config = load_configuration()
        session = create_api_session(config["email"], config["api_key"])
    except ValueError as e:
        logging.critical(e)
        return

    # Передаем даты, если они заданы
    conversations = get_all_conversations(
        session,
        config["base_url"],
        start_date=args.start_date,
        end_date=args.end_date
    )
    if not conversations:
        logging.warning("Диалоги для экспорта не найдены. Проверьте настройки и наличие данных в Desku.")
        return

    logging.info(f"\nНачинаю загрузку деталей для {len(conversations)} диалогов...")
    
    all_chats_details = []
    for i, conv in enumerate(conversations):
        ticket_id = conv.get('id')
        if not ticket_id:
            logging.warning(f"Найден диалог без ID, пропускаю: {conv}")
            continue
            
        logging.info(f"Обработка диалога {i + 1}/{len(conversations)} (ID: {ticket_id})")
        details = get_ticket_details(session, config["base_url"], ticket_id)
        
        if details:
            filtered_details = filter_ticket_data(details, FIELDS_TO_KEEP)
            all_chats_details.append(filtered_details)
        
        time.sleep(0.5)

    if all_chats_details:
        save_data_to_json(all_chats_details)
    else:
        logging.info("Нет данных для сохранения.")

if __name__ == "__main__":
    main()