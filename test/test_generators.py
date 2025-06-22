from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {"operationAmount": {"currency": {"code": "USD"}, "amount": "100.00"}, "description": "Payment for services"},
        {"operationAmount": {"currency": {"code": "EUR"}, "amount": "50.00"}, "description": "Grocery shopping"},
        {"operationAmount": {"currency": {"code": "USD"}, "amount": "200.00"}, "description": "Transfer to friend"},
        {"description": "No currency transaction"},
    ]


@pytest.mark.parametrize(
    "currency, expected_count",
    [("USD", 2), ("EUR", 1), ("RUB", 0)],
)
def test_filter_by_currency(
    sample_transactions: List[Dict[str, Any]],
    currency: str,
    expected_count: int
) -> None:
    filtered = filter_by_currency(sample_transactions, currency)
    assert len(list(filtered)) == expected_count


def test_filter_by_currency_empty_input() -> None:
    assert len(list(filter_by_currency([], "USD"))) == 0


def test_filter_by_currency_missing_keys() -> None:
    transactions = [{"invalid": "data"}]
    assert len(list(filter_by_currency(transactions, "USD"))) == 0


def test_transaction_descriptions_empty_input() -> None:
    assert list(transaction_descriptions([])) == []


@pytest.mark.parametrize(
    "start, end, expected_first, expected_last",
    [
        (1, 3, "0000 0000 0000 0001", "0000 0000 0000 0003"),
        (999, 1001, "0000 0000 0000 0999", "0000 0000 0000 1001"),
    ],
)
def test_card_number_generator(
    start: int,
    end: int,
    expected_first: str,
    expected_last: str
) -> None:
    generator = card_number_generator(start, end)
    cards = list(generator)
    assert cards[0] == expected_first
    assert cards[-1] == expected_last
    assert len(cards) == end - start + 1


def test_card_number_generator_single_value() -> None:
    assert next(card_number_generator(42, 42)) == "0000 0000 0000 0042"


def test_card_number_generator_invalid_range() -> None:
    with pytest.raises(ValueError):
        next(card_number_generator(5, 1))
