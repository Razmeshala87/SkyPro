import re
from collections import Counter
from typing import Dict, List


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Фильтрует операции по строке поиска в описании.
    """
    try:
        pattern = re.compile(search, re.IGNORECASE)
    except re.error:
        # Если строка поиска не валидный regex, ищем как обычную строку
        pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [op for op in data if 'description' in op and pattern.search(op['description'])]


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Считает количество операций по категориям (с использованием Counter)
    """
    category_counter = Counter({category: 0 for category in categories})
    for op in data:
        if 'description' in op:
            for category in categories:
                if category.lower() in op['description'].lower():
                    category_counter[category] += 1
    return dict(category_counter)


def filter_by_status(data: List[Dict], status: str) -> List[Dict]:
    """
    Фильтрует операции по статусу (без учета регистра)
    """
    return [op for op in data if 'status' in op and op['status'].upper() == status.upper()]


def sort_by_date(data: List[Dict], reverse: bool = False) -> List[Dict]:
    """
    Сортирует операции по дате
    """
    return sorted(data, key=lambda x: x.get('date', ''), reverse=reverse)


def filter_rub_only(data: List[Dict]) -> List[Dict]:
    """
    Фильтрует только рублевые транзакции
    """
    return [op for op in data if 'currency_code' in op and op['currency_code'] == 'RUB']
