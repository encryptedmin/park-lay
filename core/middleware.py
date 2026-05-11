import os
import traceback

from django.http import HttpResponse


class RenderTracebackMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception:
            if os.environ.get("RENDER"):
                return HttpResponse(
                    traceback.format_exc(),
                    status=500,
                    content_type="text/plain; charset=utf-8",
                )
            raise
