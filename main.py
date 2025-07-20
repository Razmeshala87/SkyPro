from typing import Dict, List, Union

from src.bank_operations import filter_by_status, filter_rub_only, process_bank_search, sort_by_date
from src.file_handlers import load_csv, load_json, load_xlsx


def print_operation(operation: Dict[str, Union[str, int, float, bool, None]]) -> None:
    """Печатает одну операцию в заданном формате"""
    date = str(operation.get('date', ''))
    description = str(operation.get('description', ''))
    amount = str(operation.get('amount', ''))
    currency = str(operation.get('currency_code', 'руб.'))

    if 'from' in operation and 'to' in operation:
        from_account = str(operation['from'])
        to_account = str(operation['to'])
        # Маскировка номеров карт/счетов
        if 'счет' in from_account.lower():
            from_account = 'Счет **' + from_account[-4:]
        else:
            parts = from_account.split()
            number = parts[-1]
            masked = number[:4] + ' ' + number[4:6] + '** **** ' + number[-4:]
            from_account = ' '.join(parts[:-1] + [masked])

        if 'счет' in to_account.lower():
            to_account = 'Счет **' + to_account[-4:]
        else:
            parts = to_account.split()
            number = parts[-1]
            masked = number[:4] + ' ' + number[4:6] + '** **** ' + number[-4:]
            to_account = ' '.join(parts[:-1] + [masked])

        print(f"{date} {description}\n{from_account} -> {to_account}\nСумма: {amount} {currency}\n")
    else:
        account = str(operation.get('to', ''))
        if 'счет' in account.lower():
            account = 'Счет **' + account[-4:]
        print(f"{date} {description}\n{account}\nСумма: {amount} {currency}\n")


def get_user_choice(prompt: str, options: List[str]) -> str:
    """Получает выбор пользователя с валидацией"""
    while True:
        choice = input(prompt).strip()
        if choice.lower() in [opt.lower() for opt in options]:
            return choice
        print(f"Неверный ввод. Пожалуйста, выберите один из: {', '.join(options)}")


def main() -> None:
    """Основная функция программы для работы с банковскими транзакциями"""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_choice = get_user_choice("Ваш выбор (1-3): ", ["1", "2", "3"])
    filename = input("Введите имя файла: ")

    data: List[Dict[str, Union[str, int, float, bool, None]]] = []

    try:
        if file_choice == "1":
            data = load_json(filename)
            print("Для обработки выбран JSON-файл.")
        elif file_choice == "2":
            csv_data = load_csv(filename)
            data = [{k: str(v) for k, v in item.items()} for item in csv_data]
            print("Для обработки выбран CSV-файл.")
        else:
            data = load_xlsx(filename)
            print("Для обработки выбран XLSX-файл.")
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return

    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input("Введите статус, по которому необходимо выполнить фильтрацию.\n"
                       f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}\n").strip().upper()
        if status in valid_statuses:
            break
        print(f'Статус операции "{status}" недоступен.')

    filtered_data = filter_by_status(data, status)
    print(f'Операции отфильтрованы по статусу "{status}"')

    if not filtered_data:
        print("Не найдено ни одной транзакции с указанным статусом.")
        return

    sort_choice = get_user_choice("Отсортировать операции по дате? Да/Нет: ", ["да", "нет"])
    if sort_choice.lower() == "да":
        order_choice = get_user_choice("Отсортировать по возрастанию или по убыванию? ",
                                       ["по возрастанию", "по убыванию"])
        reverse = order_choice.lower() == "по убыванию"
        filtered_data = sort_by_date(filtered_data, reverse)

    currency_choice = get_user_choice("Выводить только рублевые транзакции? Да/Нет: ", ["да", "нет"])
    if currency_choice.lower() == "да":
        filtered_data = filter_rub_only(filtered_data)

    word_choice = get_user_choice("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ",
                                  ["да", "нет"])
    if word_choice.lower() == "да":
        search_word = input("Введите слово для поиска в описании: ")
        filtered_data = process_bank_search(filtered_data, search_word)

    print("\nРаспечатываю итоговый список транзакций...\n")
    print(f"Всего банковских операций в выборке: {len(filtered_data)}\n")

    if not filtered_data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        for op in filtered_data:
            print_operation(op)


if __name__ == "__main__":
    main()
