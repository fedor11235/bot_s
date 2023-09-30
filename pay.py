import uuid
from yookassa import Configuration, Payment
import os

SECRET_KEY = os.getenv('M_KEY')
ACCOUNT_ID = os.getenv('ACCOUNT_ID')

Configuration.account_id = SECRET_KEY
Configuration.secret_key = ACCOUNT_ID

# Создание плтажеа
payment = Payment.create({
    "amount": {
        "value": "100.00",
        "currency": "RUB"
    },
    "confirmation": {
        "type": "redirect",
        "return_url": "https://www.example.com/return_url"
    },
    "capture": True,
    "description": "Заказ №1"
}, uuid.uuid4())