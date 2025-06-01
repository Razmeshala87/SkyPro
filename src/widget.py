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


