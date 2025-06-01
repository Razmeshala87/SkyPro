def get_mask_card_number(card_number):
    """
    Маскирует номер карты в формате XXXX XX** **** XXXX,
    показывая первые 6 и последние 4 цифры, остальные заменяет звездочками.

    Args:
        card_number (str): Номер карты в виде строки, может содержать пробелы или дефисы.

    Returns:
        str: Маскированный номер карты в указанном формате.
    """
    # Удаляем все пробелы и дефисы
    clean_number = "".join(filter(str.isdigit, card_number))

    # Проверка длины номера
    if len(clean_number) != 16:
        raise ValueError("Длина номера карты должна быть 16 цифр")

    # Распределение по блокам
    first_four = clean_number[:4]
    next_two = clean_number[4:6]
    last_four = clean_number[12:]

    # Маскируем средние блоки
    masked_middle = "**"

    # Формируем итоговую строку
    masked_number = f"{first_four} {next_two}{masked_middle} **** {last_four}"

    return masked_number


# Пример использования
print(get_mask_card_number("7000792289606361"))  # Вывод: 7000 79** **** 6361


def get_mask_account(account_number):
    """
    Маскирует номер счета в формате **XXXX,
    показывая только последние 4 цифры, остальные заменяет на две звездочки.

    Args:
        account_number (str): Номер счета в виде строки, может содержать пробелы или дефисы.

    Returns:
        str: Маскированный номер счета в формате **XXXX.
    """
    # Удаляем все пробелы и нецифровые символы
    clean_number = "".join(filter(str.isdigit, account_number))

    # Проверка длины номера
    if len(clean_number) < 4:
        raise ValueError("Номер счета слишком короткий")

    # Берем последние 4 цифры
    last_four = clean_number[-4:]

    # Формируем маскировку
    masked_account = f"**{last_four}"

    return masked_account


# Пример использования
print(get_mask_account("73654108430135874305"))  # Вывод: **4305
