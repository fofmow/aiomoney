# aiomoney — простая асинхронная библиотека для работы с API ЮMoney

### Авторизация приложения

1. Зарегистрируйте новое приложение YooMoney по ссылке https://yoomoney.ru/myservices/new
   (без указания чекбокса OAuth2!).
2. Получите и скопируйте `client_id` после создания приложения
3. Создайте запрос на получение api-токена.
   [О правах приложения](https://yoomoney.ru/docs/wallet/using-api/authorization/protocol-rights)

   ```python
   import asyncio
   from os import environ
   from aiomoney import authorize_app
   
   
   async def main():
       await authorize_app(
           client_id=environ.get("CLIENT_ID"),
           redirect_uri=environ.get("REDIRECT_URI"),
           app_permissions=[
               "account-info",
               "operation-history",
               "operation-details",
               "incoming-transfers",
               "payment-p2p",
               "payment-shop",
           ]
       )
   
   
   if __name__ == "__main__":
       asyncio.run(main())
   ```

4. Во время перенаправления по `redirect_uri` в адресной строке появится параметр `code=`.
   Скопируйте значение и вставьте его в консоль
5. Если авторизация прошла успешно, в консоли отобразится Ваш api-token.
   Сохраните его в переменную окружения (рекомендация)

### Получение основной информации об аккаунте

```python
import asyncio
from aiomoney.types import AccountInfo, Operation, OperationDetails
from aiomoney.wallet import YooMoneyWallet


async def main():
    wallet = YooMoneyWallet(access_token="ACCESS_TOKEN")
    
    account_info: AccountInfo = await wallet.account_info
    operation_history: list[Operation] = await wallet.get_operation_history()
    operation_details: OperationDetails = await wallet.get_operation_details(operation_id="999")


if __name__ == "__main__":
    asyncio.run(main())
```

### Создание платёжной формы и проверка оплаты

```python
import asyncio
from aiomoney.wallet import YooMoneyWallet, PaymentSource


async def main():
    wallet = YooMoneyWallet(access_token="ACCESS_TOKEN")
    
    payment_form = await wallet.create_payment_form(
        amount_rub=990,
        unique_label="myproject_second_unicorn",
        payment_source=PaymentSource.YOOMONEY_WALLET,
        success_redirect_url="https://t.me/fofmow (nonono =/)"
    )
    # проверка платежа по label
    payment_is_completed: bool = await wallet.check_payment_on_successful(payment_form.payment_label)
    
    print(f"Ссылка на оплату:\n{payment_form.link_for_customer}\n\n"
          f"Форма оплачена: {'Да' if payment_is_completed else 'Нет'}")


if __name__ == "__main__":
    asyncio.run(main())

```

### Если библиотека полезна для вас - [Donates ❤️](https://yoomoney.ru/to/4100116938791262)
