import contextvars
import sys

http_request_context = contextvars.ContextVar("http_request_context", default=None)


async def http_request_middleware_func(request, call_next):
    """Middleware function that can"""
    http_request = {
        "requestMethod": request.method,
        "requestUrl": request.url.path,
        "requestSize": sys.getsizeof(request),
        "remoteIp": request.client.host,
        "protocol": request.url.scheme,
    }
    if "referrer" in request.headers:
        http_request["referrer"] = request.headers.get("referrer")

    if "user-agent" in request.headers:
        http_request["userAgent"] = request.headers.get("user-agent")
    token = http_request_context.set(http_request)
    response = await call_next(request)
    http_request_context.reset(token)
    return response
