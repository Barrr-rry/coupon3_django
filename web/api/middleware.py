from log import logger
import traceback
from django.http import HttpResponse
import requests
import os

token = 'PAy6SmSfpfEI6nNN8K4cQKsUcjve4kxCWg03B49Tqt4'
DEBUG = os.environ.get('ENV') != 'prod'


def line_notify(msg):
    if DEBUG:
        return
    url = "https://notify-api.line.me/api/notify"

    headers = {
        "Authorization": "Bearer " + token
    }

    payload = {'message': msg}
    r = requests.post(url, headers=headers, params=payload)
    return r.status_code


def defaultmiddleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # print(f'req: {request.method} {request.path}')
        response = get_response(request)
        # print(f'res: {request.method} {request.path}')

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware


class CatchErrorMiddleware:
    def __init__(self, get_response, *args, **kwargs):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(f'{request.build_absolute_uri()},{traceback.format_exc()}')
        line_notify(f'coupon3: {traceback.format_exc()}')
        return HttpResponse("Error processing the request.", status=500)
