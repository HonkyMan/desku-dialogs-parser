# Desku Parser

Скрипт для экспорта диалогов (тикетов) из Desku по API с фильтрацией нужных полей и сохранением в JSON.

## Возможности
- Экспорт всех диалогов или за указанный период (по дате создания)
- Гибкая фильтрация полей тикета, сообщений и отправителя (настраивается в `settings.py`)
- Сохранение результата в JSON-файл
- Логирование процесса

## Быстрый старт

1. **Установите зависимости:**
   ```sh
   pip install -r requirements.txt
   ```

2. **Создайте файл `.env`** (пример):
   ```env
   PUBLIC_KEY=ваш_api_key
   DESKU_EMAIL=ваш_email
   DOMAIN=https://yourdomain.desku.io/
   DOMAIN_POSTFIX=api/public
   ```

3. **Настройте нужные поля в `settings.py`, которые одидаются в итоговом файле JSON**

4. **Запустите экспорт:**
   ```sh
   python3 export_desku_chats.py --start-date 2025-06-01 --end-date 2025-06-02
   # или без дат для экспорта всех диалогов
   python3 export_desku_chats.py
   ```

5. **Результат будет сохранён в файл `desku_export.json`** (или другой, если изменить в коде).

## Структура проекта
- `export_desku_chats.py` — основной скрипт экспорта
- `api.py` — работа с API Desku
- `config.py` — загрузка конфигурации из .env
- `utils.py` — логирование
- `settings.py` — настройка экспортируемых полей
- `requirements.txt` — зависимости
- `dst/` — папка для сохранённых экспортов (можно создать вручную)

## Пример настройки полей (settings.py)
```python
FIELDS_TO_KEEP = ["ticket_no", "title", "status", "created_at", "msg"]
MSG_FIELDS_TO_KEEP = ["id", "msg", "sender", "time"]
SENDER_FIELDS_TO_KEEP = ["email"]
```