import re
from typing import Dict, List


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Фильтрует операции по строке поиска в описании
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [op for op in data if 'description' in op and pattern.search(op['description'])]


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Считает количество операций по категориям
    """
    result = {category: 0 for category in categories}

    for op in data:
        if 'description' in op:
            for category in categories:
                if category.lower() in op['description'].lower():
                    result[category] += 1
    return result


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
