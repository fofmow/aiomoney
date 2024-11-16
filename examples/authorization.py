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
