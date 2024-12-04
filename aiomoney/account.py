from collections import deque

from http_executor import YoomoneyHttpExecutor
from schemas import AccountInfo, OperationDetails, Operation, InvoiceSource, InvoiceForm


class YooMoney:
    api_host = "https://yoomoney.ru"

    def __init__(self, access_token: str):
        self._http = YoomoneyHttpExecutor(
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {access_token}"
            }
        )

    @property
    async def account_info(self) -> AccountInfo:
        url = self.api_host + "/api/account-info"
        _, resp_data = await self._http.make_request(url)

        return AccountInfo.parse_obj(resp_data)

    async def get_operation_details(self, operation_id: str) -> OperationDetails:
        url = self.api_host + "/api/operation-details"
        _, resp_data = await self._http.make_request(url, data={"operation_id": operation_id})

        return OperationDetails.parse_obj(resp_data)

    async def get_operation_history(self, label: str | None = None) -> deque[Operation]:
        url = self.api_host + "/api/operation-history"
        _, resp_data = await self._http.make_request(url)

        if operations := resp_data.get("operations"):
            if label:
                return deque(
                    (Operation.parse_obj(op) for op in operations if op.get("label") == label)
                )
            return deque((Operation.parse_obj(op) for op in operations))

    async def get_operation_by_label(self, label: str) -> Operation | None:
        history = await self.get_operation_history(label)
        if history:
            return history.pop()

    async def create_invoice(
        self,
        amount_rub: int,
        label: str | None = None,
        success_redirect_url: str | None = None,
        payment_source: InvoiceSource = InvoiceSource.BANK_CARD
    ) -> InvoiceForm:
        account_info = await self.account_info

        params = {
            "receiver": account_info.account,
            "quickpay-form": "button",
            "paymentType": payment_source,
            "sum": amount_rub,
            "successURL": success_redirect_url,
            "label": label
        }
        params = {k: v for k, v in params.items() if v}

        url = "https://yoomoney.ru/quickpay/confirm.xml?"
        resp, resp_data = await self._http.make_request(url, params=params, load_response_body=False)

        return InvoiceForm(
            url=str(resp.url),
            label=label
        )

    async def is_payment_successful(self, label: str) -> bool:
        operation = await self.get_operation_by_label(label=label)
        return operation and operation.status == "success"

    async def revoke_token(self) -> None:
        url = self.api_host + "/api/revoke"
        resp, resp_body = await self._http.make_request(url, load_response_body=False)

        print(f"Запрос на отзыв токена завершен с кодом {resp.status} "
              f"https://yoomoney.ru/docs/wallet/using-api/authorization/revoke-access-token#response")
