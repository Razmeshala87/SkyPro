import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from external_api import currency_convertor

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_transaction(transaction: Dict[str, Any]) -> bool:
    """Проверяет обязательные поля транзакции."""
    required_fields = {"id", "date", "amount", "currency"}
    return all(field in transaction for field in required_fields)


def load_transactions(
        file_path: str,
        target_currency: Optional[str] = None,
        convert_currency: bool = False,
        validate: bool = True
) -> List[Dict[str, Any]]:
    """
    Загружает и обрабатывает транзакции из JSON-файла.

    Параметры:
        file_path: Путь к JSON-файлу
        target_currency: Валюта для конвертации (если None - не конвертировать)
        convert_currency: Нужно ли выполнять конвертацию валют
        validate: Проверять ли обязательные поля транзакций

    Возвращает:
        Список словарей с транзакциями. Пустой список в случае ошибок.
    """
    try:
        path = Path(file_path)

        # Проверка существования файла
        if not path.exists():
            logger.warning(f"Файл не найден: {file_path}")
            return []

        # Чтение и парсинг JSON
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
            return []

        # Проверка типа данных
        if not isinstance(data, list):
            logger.warning(f"Файл {file_path} не содержит список транзакций")
            return []

        processed_transactions = []

        for transaction in data:
            try:
                # Валидация транзакции
                if validate and not validate_transaction(transaction):
                    logger.warning(f"Пропущена невалидная транзакция: {transaction}")
                    continue

                # Конвертация валюты
                if (convert_currency and target_currency
                        and 'amount' in transaction
                        and 'currency' in transaction):
                    try:
                        transaction['converted_amount'] = currency_convertor(
                            transaction['amount'],
                            transaction['currency'],
                            target_currency
                        )
                        transaction['converted_to'] = target_currency
                    except Exception as e:
                        logger.error(f"Ошибка конвертации валюты: {e}")
                        transaction['converted_amount'] = None

                processed_transactions.append(transaction)

            except Exception as e:
                logger.error(f"Ошибка обработки транзакции: {e}")
                continue

        return processed_transactions

    except Exception as e:
        logger.error(f"Неожиданная ошибка при обработке файла {file_path}: {e}")
        return []