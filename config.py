import os
import logging
from dotenv import load_dotenv


def load_configuration():
    """Загружает конфигурацию из .env файла и проверяет наличие переменных."""
    load_dotenv()
    config = {
        "api_key": os.getenv("PUBLIC_KEY"),
        "email": os.getenv("DESKU_EMAIL"),
        "domain": os.getenv("DOMAIN"),
        "postfix": os.getenv("DOMAIN_POSTFIX")
    }
    if not all(config.values()):
        missing = [key for key, value in config.items() if not value]
        logging.error(f"Ошибка: не найдены переменные в .env файле: {missing}")
        raise ValueError(f"Отсутствуют переменные окружения: {missing}")
    config["base_url"] = f"{config['domain'].strip('/')}/{config['postfix'].strip('/')}"
    return config
