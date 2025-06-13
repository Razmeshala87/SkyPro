import pytest

from src.masks import get_mask_card_number


def get_mask_card_number(card_number: str) -> str:
    if not card_number or not card_number.isdigit():
        return ''
    length = len(card_number)
    if length <= 4:
        return '*' * length
    else:
        return '*' * (length - 4) + card_number[-4:]

# Фикстуры для тестовых данных
@pytest.fixture
def sample_data():
    return [
        {"card_number": "1234567812345678", "expected": "************5678"},
        {"card_number": "1234", "expected": "****"},
        {"card_number": "12", "expected": "**"},
        {"card_number": "", "expected": ""},
        {"card_number": None, "expected": ""},
        {"card_number": "12345678901234567890", "expected": "****************7890"},
        {"card_number": "0000000000000000", "expected": "************0000"},
        {"card_number": "987654321", "expected": "*****4321"},
    ]

@pytest.fixture
def non_digit_inputs():
    return [
        {"card_number": "abcd1234", "expected": ""},
        {"card_number": "1234abcd", "expected": ""},
        {"card_number": "1234 5678", "expected": ""},
    ]

# Тест с использованием фикстур
def test_get_mask_card_number_with_fixtures(sample_data, non_digit_inputs):
    # Проверка корректных данных
    for item in sample_data:
        result = get_mask_card_number(item["card_number"] if item["card_number"] is not None else "")
        assert result == item["expected"], f"Failed for input: {item['card_number']}"

    # Проверка некорректных данных
    for item in non_digit_inputs:
        result = get_mask_card_number(item["card_number"])
        assert result == item["expected"], f"Failed for input: {item['card_number']}"
