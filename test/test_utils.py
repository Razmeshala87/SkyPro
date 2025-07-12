import unittest
from unittest.mock import patch, mock_open, MagicMock
from src.utils import load_transactions
import json


class TestLoadTransactionsWithMock(unittest.TestCase):
    @patch('src.utils.Path')
    def test_load_valid_transactions(self, mock_path: MagicMock) -> None:
        """Тест загрузки корректного JSON-файла с транзакциями"""
        test_data = [
            {"id": 1, "amount": 100, "description": "Test 1"},
            {"id": 2, "amount": 200, "description": "Test 2"}
        ]

        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True
        mock_path_instance.stat.return_value.st_size = 100

        with patch('builtins.open', mock_open(read_data=json.dumps(test_data))) as mock_file:
            result = load_transactions('fake_path.json')
            mock_path.assert_called_once_with('fake_path.json')
            mock_path_instance.exists.assert_called_once()
            mock_file.assert_called_once_with(mock_path_instance, 'r', encoding='utf-8')
        self.assertEqual(result, test_data)

    @patch('src.utils.Path')
    def test_load_empty_file(self, mock_path: MagicMock) -> None:
        """Тест обработки пустого файла"""
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True
        mock_path_instance.stat.return_value.st_size = 0

        result = load_transactions('empty.json')
        self.assertEqual(result, [])

    @patch('src.utils.Path')
    def test_file_not_exists(self, mock_path: MagicMock) -> None:
        """Тест обработки случая, когда файл не существует"""
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = False

        result = load_transactions('nonexistent.json')
        self.assertEqual(result, [])

    @patch('src.utils.Path')
    @patch('json.load')
    def test_invalid_json(self, mock_json_load: MagicMock, mock_path: MagicMock) -> None:
        """Тест обработки некорректного JSON"""
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True
        mock_path_instance.stat.return_value.st_size = 100

        mock_json_load.side_effect = json.JSONDecodeError("Invalid JSON", doc="", pos=0)
        with patch('builtins.open', mock_open(read_data='{ invalid json }')):
            result = load_transactions('invalid.json')
        self.assertEqual(result, [])

    @patch('src.utils.Path')
    @patch('json.load')
    def test_non_list_json(self, mock_json_load: MagicMock, mock_path: MagicMock) -> None:
        """Тест обработки JSON, который не является списком"""
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True
        mock_path_instance.stat.return_value.st_size = 100

        mock_json_load.return_value = {"id": 1, "amount": 100}
        with patch('builtins.open', mock_open()):
            result = load_transactions('not_list.json')
        self.assertEqual(result, [])

    @patch('src.utils.Path')
    def test_unicode_content(self, mock_path: MagicMock) -> None:
        """Тест обработки файла с Unicode-символами"""
        test_data = [{"id": 1, "description": "Тест", "amount": 100}]
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True
        mock_path_instance.stat.return_value.st_size = 100

        with patch('builtins.open', mock_open(read_data=json.dumps(test_data, ensure_ascii=False))):
            result = load_transactions('unicode.json')
        self.assertEqual(result, test_data)


if __name__ == '__main__':
    unittest.main()
