import pytest

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


# Фикстуры для тестовых данных
@pytest.fixture
def sample_transactions():
    return [
        {"operationAmount": {"currency": {"code": "USD"}, "amount": "100.00"}, "description": "Payment for services"},
        {"operationAmount": {"currency": {"code": "EUR"}, "amount": "50.00"}, "description": "Grocery shopping"},
        {"operationAmount": {"currency": {"code": "USD"}, "amount": "200.00"}, "description": "Transfer to friend"},
        {"description": "No currency transaction"},
    ]


def test_filter_by_currency(sample_transactions, currency, expected_count):
    filtered = filter_by_currency(sample_transactions, currency)
    assert len(list(filtered)) == expected_count


def test_filter_by_currency_empty_input():
    assert len(list(filter_by_currency([], "USD"))) == 0


def test_filter_by_currency_missing_keys():
    transactions = [{"invalid": "data"}]
    assert len(list(filter_by_currency(transactions, "USD"))) == 0


def test_transaction_descriptions_empty_input():
    assert list(transaction_descriptions([])) == []


def test_card_number_generator(start, end, expected_first, expected_last):
    generator = card_number_generator(start, end)
    cards = list(generator)
    assert cards[0] == expected_first
    assert cards[-1] == expected_last
    assert len(cards) == end - start + 1


def test_card_number_generator_single_value():
    assert next(card_number_generator(42, 42)) == "0000 0000 0000 0042"


def test_card_number_generator_invalid_range():
    with pytest.raises(ValueError):
        next(card_number_generator(5, 1))
