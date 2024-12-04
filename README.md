# aiomoney — простая асинхронная библиотека для работы с API ЮMoney

### Авторизация приложения

1. Зарегистрируйте новое приложение YooMoney по ссылке https://yoomoney.ru/myservices/new
   (без указания чекбокса OAuth2!).
2. Получите и скопируйте `client_id` после создания приложения
3. Создайте запрос на получение api-токена.
   [О правах приложения](https://yoomoney.ru/docs/wallet/using-api/authorization/protocol-rights)

   ```python
   import asyncio
   from aiomoney import authorize_app
   
   
   async def main():
       await authorize_app(
           client_id="YOUR_CLIENT_ID",
           redirect_uri="YOUR_REDIRECT_URI",
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
   Сохраните его в переменную окружения

### Получение основной информации об аккаунте

```python
import asyncio
from collections import deque

from aiomoney import YooMoney
from aiomoney.schemas import AccountInfo, Operation, OperationDetails


async def main():
    account = YooMoney(access_token="ACCESS_TOKEN")

    account_info: AccountInfo = await account.account_info
    operation_history: deque[Operation] = await account.get_operation_history()
    operation_details: OperationDetails = await account.get_operation_details(operation_id="999")

    print(account_info, operation_history, operation_details, sep="\n\n")


if __name__ == "__main__":
    asyncio.run(main())
```

### Создание платёжной формы и проверка оплаты

```python
import asyncio

from aiomoney import YooMoney
from aiomoney.schemas import InvoiceSource


async def main():
    wallet = YooMoney(access_token="ACCESS_TOKEN")

    payment_form = await wallet.create_invoice(
        amount_rub=990,
        label="abcdefg",
        payment_source=InvoiceSource.YOOMONEY_WALLET,
        success_redirect_url="https://t.me/fofmow (nonono =/)"
    )
    # проверка платежа по label
    is_paid: bool = await wallet.is_payment_successful(payment_form.label)

    print(f"Ссылка на оплату:\n{payment_form.url}\n\n"
          f"Форма оплачена: {'Да' if is_paid else 'Нет'}")


if __name__ == "__main__":
    asyncio.run(main())

```

## Если библиотека полезна для вас - [Donates ❤️](https://yoomoney.ru/fundraise/16P5TIMSNLK.241127)


