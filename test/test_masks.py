from typing import Dict, List, Tuple, Union

import pytest

from src.masks import get_mask_account, get_mask_card_number


# Тест для маскировки номера карты с параметризацией различных случаев
@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567812345678", "1234 56** **** 5678"),
        ("1234", "raise ValueError"),
        ("", "raise ValueError"),
        (None, "raise ValueError"),
        ("12345678901234567890", "raise ValueError"),
        ("0000000000000000", "0000 00** **** 0000"),
        ("987654321", "raise ValueError"),
        ("abcd1234", "raise ValueError"),
        ("1234abcd", "raise ValueError"),
        ("1234 5678", "raise ValueError"),
    ],
)
def test_get_mask_card_number_parametrized(
    card_number: Union[str, None],
    expected: str,
) -> None:
    if expected == "raise ValueError":
        with pytest.raises(ValueError):
            input_value = card_number if card_number is not None else ""
            get_mask_card_number(input_value)
    else:
        input_value = card_number if card_number is not None else ""
        result = get_mask_card_number(input_value)
        assert result == expected


# Фикстура с корректными тестовыми данными для номера карты
@pytest.fixture
def valid_card_data() -> List[Dict[str, str]]:
    return [
        {"card_number": "7000792289606361", "expected": "7000 79** **** 6361"},
        {"card_number": "1234567812345678", "expected": "1234 56** **** 5678"},
        {"card_number": "0000000000000000", "expected": "0000 00** **** 0000"},
    ]


# Фикстура с некорректными тестовыми данными для номера карты
@pytest.fixture
def invalid_card_data() -> List[Dict[str, str]]:
    return [
        {"card_number": "1234", "expected": "raise ValueError"},
        {"card_number": "", "expected": "raise ValueError"},
        {"card_number": "12345678901234567890", "expected": "raise ValueError"},
        {"card_number": "987654321", "expected": "raise ValueError"},
        {"card_number": "abcd1234", "expected": "raise ValueError"},
        {"card_number": "1234abcd", "expected": "raise ValueError"},
        {"card_number": "1234 5678", "expected": "raise ValueError"},
    ]


# Тест маскировки карты с использованием фикстур
def test_get_mask_card_number_with_fixtures(
    valid_card_data: List[Dict[str, str]],
    invalid_card_data: List[Dict[str, str]],
) -> None:
    # Проверка валидных данных
    for item in valid_card_data:
        result = get_mask_card_number(item["card_number"])
        assert result == item["expected"], f"Failed for input: {item['card_number']}"

    # Проверка невалидных данных
    for item in invalid_card_data:
        with pytest.raises(ValueError):
            get_mask_card_number(item["card_number"])


# Фикстура с корректными тестовыми данными для номера счета
@pytest.fixture
def valid_account_numbers() -> List[Tuple[str, str]]:
    return [
        ("73654108430135874305", "**4305"),
        ("1234", "**1234"),
        (" 12-34 56 ", "**3456"),
        ("000000000000", "**0000"),
        ("987654321", "**4321"),
        ("  9876-5432  ", "**5432"),
    ]


# Фикстура с некорректными тестовыми данными для номера счета
@pytest.fixture
def invalid_account_numbers() -> List[Tuple[str, str]]:
    return [
        ("123", "Номер счета слишком короткий"),
        ("abc-def", "Номер счета слишком короткий"),
        ("", "Номер счета слишком короткий"),
        ("   ", "Номер счета слишком короткий"),
        ("--", "Номер счета слишком короткий"),
    ]


# Тест маскировки счета с корректными данными
@pytest.mark.parametrize(
    "input_value, expected_output",
    [
        ("73654108430135874305", "**4305"),
        ("1234", "**1234"),
        (" 12-34 56 ", "**3456"),
        ("000000000000", "**0000"),
        ("987654321", "**4321"),
        ("  9876-5432  ", "**5432"),
    ],
)
def test_get_mask_account_valid(input_value: str, expected_output: str) -> None:
    result = get_mask_account(input_value)
    assert result == expected_output


# Тест маскировки счета с некорректными данными
@pytest.mark.parametrize(
    "input_value, expected_error",
    [
        ("123", "Номер счета слишком короткий"),
        ("abc-def", "Номер счета слишком короткий"),
        ("", "Номер счета слишком короткий"),
        ("   ", "Номер счета слишком короткий"),
        ("--", "Номер счета слишком короткий"),
    ],
)
def test_get_mask_account_invalid(input_value: str, expected_error: str) -> None:
    with pytest.raises(ValueError) as excinfo:
        get_mask_account(input_value)
    assert str(excinfo.value) == expected_error
