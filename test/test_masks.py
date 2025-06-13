import pytest

from src.masks import get_mask_card_number,get_mask_account


# Определение функции
def get_mask_card_number(card_number: str) -> str:
    if not card_number or not card_number.isdigit():
        return ''
    length = len(card_number)
    if length <= 4:
        return '*' * length
    else:
        return '*' * (length - 4) + card_number[-4:]

# Тест с параметризацией для корректных и некорректных данных
@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567812345678", "************5678"),
        ("1234", "****"),
        ("12", "**"),
        ("", ""),
        (None, ""),  # Обработка None
        ("12345678901234567890", "****************7890"),
        ("0000000000000000", "************0000"),
        ("987654321", "*****4321"),
        # Некорректные входные данные
        ("abcd1234", ""),
        ("1234abcd", ""),
        ("1234 5678", ""),
    ]
)
def test_get_mask_card_number_parametrized(card_number, expected):
    # Обработка None
    input_value = card_number if card_number is not None else ''
    result = get_mask_card_number(input_value)
    assert result == expected

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

# Фикстуры для тестовых данных
@pytest.fixture
def valid_account_numbers():
    return [
        ("73654108430135874305", "**4305"),
        ("1234", "**1234"),
        (" 12-34 56 ", "**56"),
        ("000000000000", "**0000"),
        ("987654321", "**4321"),
        ("  9876-5432  ", "**5432"),
    ]

@pytest.fixture
def invalid_account_numbers():
    return [
        ("123", "Номер счета слишком короткий"),
        ("abc-def", "Номер счета слишком короткий"),
        ("", "Номер счета слишком короткий"),
        ("   ", "Номер счета слишком короткий"),
        ("--", "Номер счета слишком короткий"),
    ]

@pytest.mark.parametrize("input_value, expected_output", [
    ("73654108430135874305", "**4305"),
    ("1234", "**1234"),
    (" 12-34 56 ", "**3456"),
    ("000000000000", "**0000"),
    ("987654321", "**4321"),
    ("  9876-5432  ", "**5432"),
])
def test_get_mask_account_valid(input_value, expected_output):
    result = get_mask_account(input_value)
    assert result == expected_output

# Тест для обработки ошибок (короткие номера)
@pytest.mark.parametrize("input_value, expected_error", [
    ("123", "Номер счета слишком короткий"),
    ("abc-def", "Номер счета слишком короткий"),
    ("", "Номер счета слишком короткий"),
    ("   ", "Номер счета слишком короткий"),
    ("--", "Номер счета слишком короткий"),
])
def test_get_mask_account_invalid(input_value, expected_error):
    with pytest.raises(ValueError) as excinfo:
        get_mask_account(input_value)
    assert str(excinfo.value) == expected_error