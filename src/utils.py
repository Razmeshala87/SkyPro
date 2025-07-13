import json
import logging
from pathlib import Path
from typing import Any, Dict, List


def setup_logger() -> logging.Logger:
    """Настройка логгера с гарантированной записью в файл"""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    logger = logging.getLogger("utils")
    logger.setLevel(logging.INFO)  # Уровень для самого логгера

    # Очищаем предыдущие обработчики (если есть)
    if logger.hasHandlers():
        logger.handlers.clear()

    # Файловый обработчик
    file_handler = logging.FileHandler(
        "logs/utils.log",
        mode="w",
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)  # Уровень для файлового вывода

    # Консольный обработчик для отладки (опционально)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)  # Для отладки можно временно добавить

    return logger


logger = setup_logger()


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла."""
    logger.info(f"Начало загрузки транзакций из файла: {file_path}")

    try:
        path = Path(file_path)

        if not path.exists():
            error_msg = f"Файл не существует: {file_path}"
            logger.error(error_msg)
            return []

        if path.stat().st_size == 0:
            logger.warning(f"Файл пуст: {file_path}")
            return []

        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logger.debug(f"Прочитано {len(data)} записей")  # Для отладки

        if not isinstance(data, list):
            logger.warning(f"Файл {file_path} не содержит список транзакций")
            return []

        logger.info(f"Успешно загружено {len(data)} транзакций")
        return data

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка JSON в файле {file_path}: {str(e)}", exc_info=True)
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {str(e)}", exc_info=True)
        return []


# Тестовый вызов для проверки логирования
if __name__ == "__main__":
    # Тест с существующим файлом
    test_data = load_transactions("data/transactions.json")

    # Тест с несуществующим файлом
    load_transactions("nonexistent.json")

    # Тест с пустым файлом
    Path("empty.json").touch()
    load_transactions("empty.json")
