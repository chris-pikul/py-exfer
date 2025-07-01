import urllib.request


def ping(url: str) -> bool:
    """Checks that an endpoint is responding with a valid status code.

    Args:
        url (str): The URL to test.

    Returns:
        bool: True if the request succeeded with a 2XX or 3XX status code.
    """
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.status >= 200 and response.status < 400
    except Exception as e:
        return False
