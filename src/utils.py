import json
from pathlib import Path
from typing import List, Dict, Any


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла."""
    try:
        path = Path(file_path)
        if not path.exists() or path.stat().st_size == 0:
            return []

        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, OSError):
        return []
