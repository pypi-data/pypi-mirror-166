import base64

import requests


class utils:
    @staticmethod
    def raise_not_own():
        raise Exception("This url can't be bypass by this class")

    @staticmethod
    def getUserAgent():
        return 'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'

    @staticmethod
    def print_debug(debug, message):
        if debug:
            print(message)

    @staticmethod
    def request(debug, status_code_should, request_params):
        utils.print_debug(debug, f"request : {request_params}")
        response = requests.request(**request_params)
        if response.status_code != status_code_should:
            raise ValueError(f"status code should be 200 but is {response.status_code}")
        return response

    @staticmethod
    def encode_base64(string):
        return base64.b64encode(string.encode('ascii')).decode('utf-8')

    @staticmethod
    def decode_base64(string):
        return base64.b64decode(string.encode('ascii')).decode('utf-8')
