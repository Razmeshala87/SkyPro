import logging
from pathlib import Path


def setup_logger() -> logging.Logger:
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    logger = logging.getLogger("masks")
    logger.setLevel(logging.INFO)

    # Явно указываем кодировку utf-8
    handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


logger = setup_logger()


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты в формате XXXX XX** **** XXXX,
    показывая первые 6 и последние 4 цифры, остальные заменяет звездочками.

    Args:
        card_number (str): Номер карты в виде строки, может содержать пробелы
        или дефисы.

    Returns:
        str: Маскированный номер карты в указанном формате.
    """
    try:
        # Удаляем все пробелы и дефисы
        clean_number = "".join(filter(str.isdigit, card_number))

        # Проверка длины номера
        if len(clean_number) != 16:
            error_msg = "Длина номера карты должна быть 16 цифр"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Распределение по блокам
        first_four = clean_number[:4]
        next_two = clean_number[4:6]
        last_four = clean_number[12:]

        # Маскируем средние блоки
        masked_middle = "**"

        # Формируем итоговую строку
        masked_number = f"{first_four} {next_two}{masked_middle} **** {last_four}"

        logger.info(f"Успешно замаскирован номер карты: {masked_number}")
        return masked_number

    except Exception as e:
        logger.error(f"Ошибка при маскировании номера карты: {str(e)}")
        raise


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета в формате **XXXX,
    показывая только последние 4 цифры, остальные заменяет на две звездочки.

    Args:
        account_number (str): Номер счета в виде строки, может содержать
         пробелы или дефисы.

    Returns:
        str: Маскированный номер счета в формате **XXXX.
    """
    try:
        # Удаляем все пробелы и нецифровые символы
        clean_number = "".join(filter(str.isdigit, account_number))

        # Проверка длины номера
        if len(clean_number) < 4:
            error_msg = "Номер счета слишком короткий"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Берем последние 4 цифры
        last_four = clean_number[-4:]

        # Формируем маскировку
        masked_account = f"**{last_four}"

        logger.info(f"Успешно замаскирован номер счета: {masked_account}")
        return masked_account

    except Exception as e:
        logger.error(f"Ошибка при маскировании номера счета: {str(e)}")
        raise


# Пример использования
if __name__ == "__main__":
    print(get_mask_card_number("7000792289606361"))  # Вывод: 7000 79** **** 6361
    print(get_mask_account("73654108430135874305"))  # Вывод: **4305
