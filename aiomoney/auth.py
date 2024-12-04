from http_executor import YoomoneyHttpExecutor
from getpass import getpass

AUTH_APP_URL = "https://yoomoney.ru/oauth/authorize?client_id={client_id}&response_type=code" \
               "&redirect_uri={redirect_uri}&scope={permissions}"

GET_TOKEN_URL = "https://yoomoney.ru/oauth/token?code={code}&client_id={client_id}&" \
                "grant_type=authorization_code&redirect_uri={redirect_uri}"


async def authorize_app(
    client_id: str,
    redirect_uri: str,
    app_permissions: list[str]
):
    auth_url = AUTH_APP_URL.format(
        client_id=client_id,
        redirect_uri=redirect_uri,
        permissions="%20".join(app_permissions)
    )
    http_executor = YoomoneyHttpExecutor(headers={"content-type": "application/x-www-form-urlencoded"})
    resp, resp_data = await http_executor.make_request(auth_url, load_response_body=False)

    print(f"Перейдите по URL и подтвердите доступ для приложения\n{resp.url}")
    code = getpass("Введите код в консоль >  ").strip()

    get_token_url = GET_TOKEN_URL.format(
        code=code,
        client_id=client_id,
        redirect_uri=redirect_uri
    )
    _, resp_data = await http_executor.make_request(get_token_url)

    access_token = resp_data.get("access_token")
    if not access_token:
        return print(f"Не удалось получить токен. {resp_data.get('error', '')}")

    return print(f"Ваш токен — {access_token}. Сохраните его в безопасном месте!")
