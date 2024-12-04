class _BaseError(Exception):
    def __str__(self):
        return "Check: https://yoomoney.ru/docs/wallet/using-api/format/protocol-response"


class InvalidRequestError(_BaseError):
    ...


class InvalidTokenError(_BaseError):
    ...


class ForbiddenError(_BaseError):
    ...
