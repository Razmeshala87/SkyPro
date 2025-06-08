def filter_by_state(records: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    :param records: список словарей
    :param state: значение для фильтрации (по умолчанию 'EXECUTED')
    :return: новый список словарей, соответствующих условию
    """
    return [record for record in records if record.get("state") == state]


def sort_by_date(records: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует список словарей по ключу 'date'.

    :param records: список словарей
    :param reverse: порядок сортировки (по умолчанию — убывание)
    :return: отсортированный список словарей
    """
    return sorted(records, key=lambda x: x.get("date", ""), reverse=reverse)
