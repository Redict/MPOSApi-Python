import requests, json, re
import urllib.parse as urllib

methods = {"getblockcount": [], "getblocksfound": [], "getblockstats": [], "getcurrentworkers": [], "getdashboarddata": ["id"],
           "getdifficulty": [], "getestimatedtime": [], "gethourlyhashrates": [], "getnavbardata": [], "getpoolhashrate": [],
           "getpoolinfo": [], "getpoolsharerate": [], "getpoolstatus": [], "gettimesincelastblock": [], "gettopcontributors": [],
           "getuserbalance": ["id"], "getuserhashrate": ["id"], "getusersharerate": ["id"], "getuserstatus": ["id"], "getusertransactions": ["id"],
           "getuserworkers": ["id"], "public": []}

validateUrl = lambda x: True if len(re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE).findall(x)) else False


class NoSuchMethod(Exception):

    def __init__(self, message):
        self.message = message

class ValidationError(Exception):

    def __init__(self, message):
        self.message = message

class NoParameter(Exception):

    def __init__(self, message):
        self.message = message

class RequestError(Exception):

    def __init__(self, message):
        self.message = message

class MPOSApi:
    """
    
    MPOS API Reference available at https://goo.gl/jM9zNB

    """

    def __init__(self, url, api_key):
        if not validateUrl(url):
            raise ValidationError(f"Bad URL: {url}")
        self.url = urllib.urlparse(url)
        self.key = api_key

    def makeRequest(self, url):
        f = requests.get(url)
        if f.status_code != 200:
            raise RequestError(f"Request to {url} returned {f.status_code}")
        return f.json()

    def command(self, key, args=None):
        key_args = methods[key]
        sanitized = dict()
        for arg in key_args:
            if not isinstance(args, dict):
                return NoParameter(f"Not enough arguments. {key} parameters: {', '.join(key_args)}")
            if arg not in args:
                raise NoParameter(f"{arg}")
            sanitized[arg] = args[arg]

        url = self.url.scheme + "://" + self.url.netloc + f"/index.php?page=api&action={key}&api_key={self.key}&{urllib.urlencode(sanitized)}"

        return self.makeRequest(url)

    def __getattr__(self, key):

        def out(args=None):
            if key not in methods:
                raise NoSuchMethod(f"{key}")

            return self.command(key, args)

        return out
