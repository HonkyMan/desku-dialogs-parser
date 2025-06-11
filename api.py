import requests
import time
import logging


def create_api_session(email, api_key):
    """Создает и настраивает сессию requests для работы с API."""
    session = requests.Session()
    session.auth = (email, api_key)
    return session


def get_all_conversations(session, base_url, start_date=None, end_date=None):
    """Получает полный список всех диалогов (тикетов) с пагинацией. Можно указать start_date и end_date."""
    logging.info("Начинаю загрузку списка всех диалогов...")
    all_conversations = []
    page = 1
    record = 50
    while True:
        try:
            logging.info(f"Загружаю страницу {page}...")
            params = {"page": page, "record": record}
            # Добавляем параметры дат, если оба указаны
            if start_date and end_date:
                params["start_date"] = start_date
                params["end_date"] = end_date
            response = session.get(
                f"{base_url}/all-conversations",
                params=params
            )
            response.raise_for_status()
            data = response.json().get('data', []).get('data', [])
            if not data:
                logging.info("Больше диалогов не найдено. Загрузка списка завершена.")
                break
            all_conversations.extend(data)
            logging.info(f"Найдено {len(data)} диалогов. Всего: {len(all_conversations)}")
            # Если получили меньше, чем запрошено — это последняя страница
            if len(data) < record:
                break
            page += 1
            time.sleep(0.6)  # Пауза для избежания превышения лимитов API
        except requests.exceptions.HTTPError as e:
            if response.status_code == 403:
                logging.info("Достигнут конец страниц (403 Forbidden).")
                break
            logging.error(f"Критическая ошибка при загрузке списка диалогов: {e}")
            break
        except requests.exceptions.RequestException as e:
            logging.error(f"Критическая ошибка при загрузке списка диалогов: {e}")
            break
    return all_conversations


def get_ticket_details(session, base_url, ticket_id):
    """Получает полную информацию по одному тикету."""
    try:
        response = session.get(f"{base_url}/single-ticket/{ticket_id}")
        response.raise_for_status()
        return response.json().get('data', {})
    except requests.exceptions.RequestException as e:
        logging.warning(f"Не удалось получить детали для тикета {ticket_id}: {e}")
        return None
