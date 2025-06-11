# settings.py

# Список полей, которые нужно оставить в итоговом JSON для каждого тикета.
# Оставьте список пустым [], чтобы экспортировать ВСЕ поля без фильтрации.
#
# Примеры:
# FIELDS_TO_KEEP = ["id", "subject", "status", "messages"] # Экспорт только этих полей
# FIELDS_TO_KEEP = [] # Экспорт всех полей
#
FIELDS_TO_KEEP = [
    "ticket_no",
    "title",
    "status",
    "created_at",
    "updated_at",
    "rating",
    "review",
    "msg"
]

# Для вложенного массива msg: какие поля оставить в каждом сообщении
MSG_FIELDS_TO_KEEP = [
    "id",
    "ticket_id",
    "send_by",
    "sender_role",
    "msg",
    "sender",
    "time",
    "attachments"
]

# Для вложенного sender: какие поля оставить
SENDER_FIELDS_TO_KEEP = [
    "email"
]