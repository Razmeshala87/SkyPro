import json
import logging
from pathlib import Path
from typing import List, Dict, Any


# Настройка логгера для модуля utils
def setup_logger() -> logging.Logger:
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    logger = logging.getLogger("utils")
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler("logs/utils.log", mode="w")
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


logger = setup_logger()


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла."""
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

        if not isinstance(data, list):
            logger.warning(f"Файл {file_path} не содержит список транзакций")
            return []

        logger.info(f"Успешно загружено {len(data)} транзакций из {file_path}")
        return data

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {str(e)}")
        return []
    except OSError as e:
        logger.error(f"Ошибка ввода-вывода при работе с файлом {file_path}: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при загрузке транзакций: {str(e)}")
        return []
