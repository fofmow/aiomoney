import asyncio
from os import environ

from dotenv import load_dotenv

from aiomoney.types import AccountInfo, Operation, OperationDetails
from aiomoney.wallet import YooMoneyWallet

load_dotenv()


async def main():
    wallet = YooMoneyWallet(access_token=environ.get("ACCESS_TOKEN"))
    
    account_info: AccountInfo = await wallet.account_info
    """
    account='4100116938791262' balance=small =) currency='643' account_status='identified'
    account_type='personal' balance_details=BalanceDetail(total=X, available=X,
    deposition_pending=None, blocked=None, debt=None, hold=None) cards_linked=None
    """
    
    operation_history: list[Operation] = await wallet.get_operation_history()
    """
    [Operation(operation_id='000000', status='success',
    execution_datetime=datetime.datetime(2023, 3, 9, 13, 15, 10, tzinfo=datetime.timezone.utc),
    title='Пополнение с карты ****0000', pattern_id=None, direction='in',
    amount=00, label='000000', operation_type='deposition'), ...]
    """
    
    operation_details: OperationDetails = await wallet.get_operation_details(operation_id="000")
    # details by operation ...


if __name__ == "__main__":
    asyncio.run(main())
