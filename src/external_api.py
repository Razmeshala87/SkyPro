import os
import requests
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')


def convert_to_rub(amount: float, currency: str) -> Optional[float]:
    """
    Конвертирует сумму в RUB используя Exchange Rates Data API

    :param amount: Сумма для конвертации
    :param currency: Исходная валюта (USD, EUR)
    :return: Сумма в рублях или None при ошибке
    """
    if currency == 'RUB':
        return amount

    try:
        response = requests.get(
            f"{BASE_URL}/convert",
            params={
                'to': 'RUB',
                'from': currency,
                'amount': amount
            },
            headers={'apikey': API_KEY}
        )
        response.raise_for_status()
        return float(response.json()['result'])
    except Exception as e:
        print(f"Ошибка конвертации валюты: {e}")
        return None