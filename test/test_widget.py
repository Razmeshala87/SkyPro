from typing import Any, List, Tuple, Union

import pytest

from src.widget import get_date, mask_account_card


@pytest.fixture
def valid_card_numbers() -> List[Tuple[str, str]]:
    return [
        ("Visa 1234567812345678", "Visa 1234 56** **** 5678"),
        ("МИР 1234123412341234", "МИР 1234 12** **** 1234"),
        ("MasterCard 5678567856785678", "MasterCard 5678 56** **** 5678"),
    ]


@pytest.fixture
def valid_account_numbers() -> List[Tuple[str, str]]:
    return [
        ("Счет 12345678901234567890", "Счет **7890"),
        ("счет 98765432109876543210", "счет **3210"),
        ("СЧЕТ 11112222333344445555", "СЧЕТ **5555"),
    ]


@pytest.fixture
def invalid_data() -> List[Tuple[Union[str, Any], Union[str, Any]]]:
    return [
        ("Карта 1234", "Карта 1234"),
        ("Счет", "Счет"),
        ("1234567812345678", "1234567812345678"),
        ("", ""),
        ("InvalidType 1234567890123456", "InvalidType 1234 56** **** 3456"),
    ]


@pytest.fixture
def date_samples() -> List[Tuple[str, str]]:
    return [
        ("2023-10-05T14:30:00.000000", "05.10.2023"),
        ("1999-12-31T23:59:59.999999", "31.12.1999"),
        ("2000-01-01T00:00:00.000000", "01.01.2000"),
    ]


@pytest.fixture
def invalid_dates() -> List[Tuple[Union[str, Any], Union[str, Any]]]:
    return [("2023/10/05", "2023/10/05"), ("NotADate", "NotADate"), ("", ""), ("2023-13-01", "01.13.2023")]


def test_mask_card_numbers(valid_card_numbers: List[Tuple[str, str]]) -> None:
    for input_data, expected in valid_card_numbers:
        assert mask_account_card(input_data) == expected


def test_mask_account_numbers(valid_account_numbers: List[Tuple[str, str]]) -> None:
    for input_data, expected in valid_account_numbers:
        assert mask_account_card(input_data) == expected


def test_mask_invalid_input(invalid_data: List[Tuple[Union[str, Any], Union[str, Any]]]) -> None:
    for input_data, expected in invalid_data:
        try:
            assert mask_account_card(str(input_data)) == expected
        except (ValueError, AttributeError, TypeError):
            assert str(input_data) == str(expected)


def test_get_date_valid(date_samples: List[Tuple[str, str]]) -> None:
    for input_date, expected in date_samples:
        assert get_date(input_date) == expected


def test_get_date_invalid(invalid_dates: List[Tuple[Union[str, Any], Union[str, Any]]]) -> None:
    for input_date, expected in invalid_dates:
        try:
            assert get_date(str(input_date)) == expected
        except (ValueError, AttributeError, TypeError):
            assert str(input_date) == str(expected)


def test_mask_none_input() -> None:
    with pytest.raises((AttributeError, TypeError)):
        mask_account_card(None)  # type: ignore


def test_get_date_none_input() -> None:
    with pytest.raises((AttributeError, TypeError)):
        get_date(None)  # type: ignore


def test_mask_non_string_input() -> None:
    with pytest.raises((AttributeError, TypeError)):
        mask_account_card(12345)  # type: ignore


def test_get_date_non_string_input() -> None:
    with pytest.raises((AttributeError, TypeError)):
        get_date(12345)  # type: ignore
