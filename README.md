# TentorgAPI

Эта библиотека предназначена для работы с API [**Tentorg**](https://trade.tentorg.ru/), позволяя аутентифицироваться, выполнять запросы и обрабатывать данные заказов.

## Установка
```
pip install git+https://github.com/SergeyDyatlov/TentorgAPI.git
```
## Использование
```
from tentorgapi import TentorgAPI

client = TentorgAPI("user@example.com", "password123")
client.authenticate()

orders = client.get_orders(page=1)
[print(order) for order in orders]
```
