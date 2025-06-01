def mask_account_card(info: str) -> str:
    """
    Маскирует информацию о карте или счете.
    """
    # Разделяем строку на тип и номер
    parts = info.split(' ', 1)
    if len(parts) != 2:
        return info  # некорректный формат, возвращаем как есть

    type_info, number = parts
    type_info_lower = type_info.lower()

    # Обработка в зависимости от типа
    if 'счет' in type_info_lower:
        masked_number = mask_account_number(number)
        return f"{type_info} {masked_number}"
    else:
        # Предполагаем, что это карта
        masked_number = mask_card_number(number)
        return f"{type_info} {masked_number}"


def get_date(date_str: str) -> str:
    """
    Преобразует строку с датой из формата "YYYY-MM-DDTHH:MM:SS.ssssss"
    в формат "ДД.ММ.ГГГГ" без использования импортов.
    """
    # Разделяем строку по символу 'T'
    date_part = date_str.split('T')[0]
    # Разделяем дату по '-'
    year, month, day = date_part.split('-')
    # Форматируем в "ДД.ММ.ГГГГ"
    return f"{day}.{month}.{year}"
