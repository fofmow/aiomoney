import asyncio
from os import environ

from dotenv import load_dotenv

from aiomoney.wallet import YooMoneyWallet, PaymentSource

load_dotenv()


async def main():
    wallet = YooMoneyWallet(access_token=environ.get("ACCESS_TOKEN"))
    
    payment_form = await wallet.create_payment_form(
        amount_rub=10,
        unique_label="myproject_second_unicorn",
        payment_source=PaymentSource.YOOMONEY_WALLET,
        success_redirect_url="https://t.me/fofmow (nonono =/)"
    )
    payment_is_completed = await wallet.check_payment_on_successful(payment_form.payment_label)
    print(f"Ссылка на оплату:\n{payment_form.link_for_customer}\n\n"
          f"Форма оплачена: {'Да' if payment_is_completed else 'Нет'}")


if __name__ == "__main__":
    asyncio.run(main())
