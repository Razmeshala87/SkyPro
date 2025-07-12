import unittest
from unittest.mock import patch, Mock
import requests
from typing import Dict, Any
from src.external_api import convert_to_rub


class TestConvertToRub(unittest.TestCase):
    def test_convert_rub_to_rub(self) -> None:
        """Тест конвертации RUB в RUB (без конвертации)."""
        transaction: Dict[str, Any] = {"amount": 100.0, "currency": "RUB"}
        result: float = convert_to_rub(transaction)
        self.assertEqual(result, 100.0)

    @patch.dict("os.environ", {"API_KEY": "test_api_key"})
    @patch("requests.get")
    def test_convert_usd_to_rub(self, mock_get: Mock) -> None:
        """Тест конвертации USD в RUB."""
        mock_response: Mock = Mock()
        mock_response.json.return_value = {"rates": {"RUB": 75.50}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        transaction: Dict[str, Any] = {"amount": 10.0, "currency": "USD"}
        result: float = convert_to_rub(transaction)
        self.assertEqual(result, 755.0)
        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/latest?base=USD&symbols=RUB",
            headers={"apikey": "test_api_key"},
        )

    @patch.dict("os.environ", {"API_KEY": "test_api_key"})
    @patch("requests.get")
    def test_convert_with_api_error(self, mock_get: Mock) -> None:
        """Тест обработки ошибки API."""
        mock_get.side_effect = requests.RequestException("API недоступно")

        transaction: Dict[str, Any] = {"amount": 10.0, "currency": "EUR"}
        with self.assertRaises(ValueError) as context:
            convert_to_rub(transaction)
        self.assertIn("Ошибка конвертации валюты", str(context.exception))

    def test_missing_api_key(self) -> None:
        """Тест отсутствия API_KEY в переменных окружения."""
        transaction: Dict[str, Any] = {"amount": 10.0, "currency": "GBP"}
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ValueError) as context:
                convert_to_rub(transaction)
            self.assertIn("API_KEY не найден в .env", str(context.exception))

    @patch.dict("os.environ", {"API_KEY": "test_api_key"})
    @patch("requests.get")
    def test_invalid_json_response(self, mock_get: Mock) -> None:
        """Тест обработки некорректного JSON-ответа."""
        mock_response: Mock = Mock()
        mock_response.json.return_value = {}  # Нет поля 'rates'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        transaction: Dict[str, Any] = {"amount": 10.0, "currency": "JPY"}
        with self.assertRaises(ValueError) as context:
            convert_to_rub(transaction)
        self.assertIn("Ошибка конвертации валюты", str(context.exception))


if __name__ == "__main__":
    unittest.main()
