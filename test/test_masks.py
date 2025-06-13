import pytest

from src.masks import get_mask_card_number


# Для примера, определим функцию здесь
def get_mask_card_number(card_number: str) -> str:
    if not card_number or not card_number.isdigit():
        return ''
    length = len(card_number)
    if length <= 4:
        return '*' * length
    else:
        return '*' * (length - 4) + card_number[-4:]

@pytest.mark.parametrize("input_value, expected_output", [
    ("1234567812345678", "************5678"),  # стандартный 16-значный номер
    ("1234", "****"),                          # минимальный допустимый длины (4)
    ("12", "**"),                              # менее 4 символов
    ("", ""),                                  # пустая строка
    (None, ""),                                # None (если функция принимает такой тип)
    ("12345678901234567890", "****************7890"),  # длинный номер
    ("0000000000000000", "************0000"),  # нулевой номер
    ("987654321", "*****4321"),                # 9-значный номер
])
def test_get_mask_card_number(input_value, expected_output):
    # Обработка None, если функция должна принимать такие значения
    if input_value is None:
        result = get_mask_card_number('')
    else:
        result = get_mask_card_number(input_value)
    assert result == expected_output

# Проверка обработки некорректных входных данных
def test_non_digit_input():
    assert get_mask_card_number("abcd1234") == ''
    assert get_mask_card_number("1234abcd") == ''
    assert get_mask_card_number("1234 5678") == ''
