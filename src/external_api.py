import os
from typing import Optional, Dict, Union, Any
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY: str = os.getenv('API_KEY', '')
BASE_URL: str = os.getenv('BASE_URL', 'https://api.apilayer.com/exchangerates_data')


def convert_to_rub(amount: float, currency: str) -> Optional[float]:
    """
    Конвертирует сумму в RUB используя Exchange Rates Data API

    Args:
        amount: Сумма для конвертации
        currency: Исходная валюта (USD, EUR, etc.)

    Returns:
        Сумма в рублях или None при ошибке
    """
    if currency == 'RUB':
        return amount

    try:
        # Явно аннотируем тип параметров
        params: Dict[str, Union[str, float]] = {
            'to': 'RUB',
            'from': currency,
            'amount': amount
        }

        headers: Dict[str, str] = {'apikey': API_KEY}

        response = requests.get(
            f"{BASE_URL}/convert",
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        json_data: Dict[str, Any] = response.json()
        result: float = float(json_data['result'])
        return result

    except (requests.exceptions.RequestException, ValueError, KeyError) as e:
        print(f"Ошибка конвертации валюты: {e}")
        return None
