from typing import Iterator, Dict, Any


def filter_by_currency(transactions: list[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте и возвращает итератор.

    Args:
        transactions: Список словарей с транзакциями
        currency: Код валюты для фильтрации (например, "USD")

    Returns:
        Итератор, возвращающий транзакции с указанной валютой
    """
    return (tx for tx in transactions if tx.get("operationAmount", {}).get("currency", {}).get("code") == currency)


def transaction_descriptions(transactions: list[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который последовательно возвращает описания транзакций.

    Args:
        transactions: Список словарей с транзакциями, где каждый словарь содержит
                     ключ 'description' с описанием операции.

    Yields:
        str: Описание транзакции

    Пример использования:
        descriptions = transaction_descriptions(transactions)
        for _ in range(5):
            print(next(descriptions))
    """
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    Args:
        start: Начальное значение диапазона (от 1)
        end: Конечное значение диапазона (до 9999999999999999)

    Yields:
        str: Номер карты в заданном формате

    Пример использования:
        for card_number in card_number_generator(1, 5):
            print(card_number)
    """
    for number in range(start, end + 1):
        # Форматируем число в 16-значную строку с ведущими нулями
        card_str = f"{number:016d}"
        # Разбиваем на группы по 4 цифры
        yield f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
