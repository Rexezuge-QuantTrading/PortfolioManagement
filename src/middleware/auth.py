import hashlib
import hmac
import time
import json
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send


def get_minified_body(body: bytes) -> bytes:
    try:
        if not body:
            return b""

        # Attempt to parse the body as JSON
        json_body = json.loads(body)

        # If parsing succeeds, re-serialize it with no extra whitespace
        return json.dumps(json_body, separators=(",", ":")).encode("utf-8")
    except json.JSONDecodeError:
        # If parsing fails, it's not a JSON body, so return the original body
        return body


class AuthMiddleware:
    def __init__(self, app: ASGIApp, secret_key: str):
        self.app = app
        self.secret_key = secret_key

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)

        signature = request.headers.get("X-Signature")
        timestamp_str = request.headers.get("X-Timestamp")

        if not signature or not timestamp_str:
            response = JSONResponse(
                {"error": "Missing signature or timestamp"}, status_code=401
            )
            await response(scope, receive, send)
            return

        try:
            timestamp = int(timestamp_str)
        except ValueError:
            response = JSONResponse(
                {"error": "Invalid timestamp format"}, status_code=401
            )
            await response(scope, receive, send)
            return

        if abs(time.time() * 1000 - timestamp) > 3 * 60 * 1000:
            response = JSONResponse({"error": "Timestamp expired"}, status_code=401)
            await response(scope, receive, send)
            return

        headers_to_sign = {
            k.lower(): v
            for k, v in request.headers.items()
            if k.lower().startswith("x-") and k.lower() != "x-signature"
        }

        sorted_headers = "".join(
            f"{k}:{headers_to_sign[k]}" for k in sorted(headers_to_sign)
        )

        body = await request.body()
        minified_body = get_minified_body(body)

        message = (
            request.method.encode("utf-8")
            + request.url.path.encode("utf-8")
            + b"?"
            + request.url.query.encode("utf-8")
            + minified_body
            + sorted_headers.encode("utf-8")
        )

        calculated_signature = hmac.new(
            self.secret_key.encode("utf-8"), message, hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(calculated_signature, signature):
            response = JSONResponse(
                {
                    "error": "Invalid signature",
                    "debug": {
                        "requestMessage": message.decode("utf-8"),
                    },
                },
                status_code=401,
            )
            await response(scope, receive, send)
            return

        # We need to create a new receive function because the body has been consumed
        async def new_receive():
            return {"type": "http.request", "body": body, "more_body": False}

        await self.app(scope, new_receive, send)
