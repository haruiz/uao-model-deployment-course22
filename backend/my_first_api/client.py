import urllib.error
import urllib.parse
import urllib.request
import json
import os


def call_api(endpoint):
    """
    Call API
    :param endpoint:
    :return:
    """
    # Create request
    request = urllib.request.Request(endpoint, method="GET")
    try:
        response = urllib.request.urlopen(request)
        print(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # The request failed
        print("Request failed")
        print(e.reason)
        print(e.headers)
        print(e.read())
        return None



if __name__ == '__main__':
    call_api("http://0.0.0.0:8000/")