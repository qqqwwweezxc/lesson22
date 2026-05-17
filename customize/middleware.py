from threading import local
import logging

class CustomHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        response["X-Custom-Header"] = "This is my custom header"

        return response


logger = logging.getLogger("custom")


def my_view(request):
    logger.info("View was called")
    return HttpResponse("OK")


_thread_locals = local()


class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not hasattr(_thread_locals, "request_count"):
            _thread_locals.request_count = 0

        _thread_locals.request_count += 1

        response = self.get_response(request)

        return response


def get_request_count():
    return getattr(_thread_locals, "request_count", 0)
