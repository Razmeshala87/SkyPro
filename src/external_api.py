import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """Конвертирует сумму транзакции в рубли."""
    amount = transaction.get('amount', 0.0)
    currency = transaction.get('currency', 'RUB').upper()

    if currency == 'RUB':
        return float(amount)

    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY не найден в .env")

    url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}&symbols=RUB"
    headers = {"apikey": api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        rate = float(response.json()['rates']['RUB'])  # Явное преобразование в float
        return float(amount) * rate
    except (requests.RequestException, KeyError, ValueError) as e:
        raise ValueError(f"Ошибка конвертации валюты: {e}") from e
