# Виджет банковских операций клиента.

## Данный виджет предназначен для банковских операций клиента: 
1. Маскировка номера карты клиента;
2. Маскировка номера счета клиента; 
3. Умеет принимать на вход строку с датой в одном и 
возвращает строку с датой в формате "ДД.ММ.ГГГГ"



Установка


		1. Клонируйте репозиторий:

git clone https://github.com/Razmeshala87/SkyPro.git


		2. Перейдите в директорию проекта:

C:\Users\Razme\PycharmProjects


		3. Установите необходимые зависимости:

pip install -r requirements.txt



Использование

Примеры использования функций:

from src.masks import get_mask_account, get_mask_card_number

# Пример использования get_mask_account

print(get_mask_card_number("1234567812345678"))

# Пример использования get_mask_account

print(get_mask_account("123456"))


from src.processing import filter_by_state, sort_by_date

# Пример использования filter_by_state
print(
        filter_by_state(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ]
        )
    )

# Пример использования sort_by_date
print(
    sort_by_date(
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        ]
    )
)

Вклад

Если вы хотите внести свой вклад, пожалуйста, создайте форк репозитория и отправьте пул-реквест.