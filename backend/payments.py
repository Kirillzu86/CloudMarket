import base64
import json
import os
import uuid
from decimal import Decimal
from urllib.error import HTTPError
from urllib.request import Request, urlopen


YOOKASSA_API_URL = "https://api.yookassa.ru/v3"


class YooKassaConfigError(RuntimeError):
    pass


class YooKassaRequestError(RuntimeError):
    pass


def get_yookassa_credentials() -> tuple[str, str]:
    shop_id = os.getenv("YOOKASSA_SHOP_ID")
    secret_key = os.getenv("YOOKASSA_SECRET_KEY")
    if not shop_id or not secret_key:
        raise YooKassaConfigError("YooKassa credentials are not configured")
    return shop_id, secret_key


def get_frontend_base_url() -> str:
    return os.getenv("FRONTEND_BASE_URL", "http://localhost:5173").rstrip("/")


def request_yookassa(method: str, path: str, payload: dict | None = None, idempotence_key: str | None = None) -> dict:
    shop_id, secret_key = get_yookassa_credentials()
    auth_token = base64.b64encode(f"{shop_id}:{secret_key}".encode("utf-8")).decode("ascii")
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }
    if idempotence_key:
        headers["Idempotence-Key"] = idempotence_key

    request = Request(f"{YOOKASSA_API_URL}{path}", data=body, headers=headers, method=method)
    try:
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise YooKassaRequestError(f"YooKassa request failed: {exc.code} {details}") from exc


def create_yookassa_payment(order_id: int, amount: Decimal, description: str) -> dict:
    return_url = f"{get_frontend_base_url()}/payment/success?order_id={order_id}"
    payload = {
        "amount": {
            "value": f"{amount:.2f}",
            "currency": "RUB",
        },
        "capture": True,
        "confirmation": {
            "type": "redirect",
            "return_url": return_url,
        },
        "description": description[:128],
        "metadata": {
            "order_id": str(order_id),
        },
    }
    return request_yookassa("POST", "/payments", payload, idempotence_key=str(uuid.uuid4()))


def get_yookassa_payment(payment_id: str) -> dict:
    return request_yookassa("GET", f"/payments/{payment_id}")
