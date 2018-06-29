import urllib.parse
import urllib.request
from random import randint
from time import sleep

from urllib.parse import quote

from fake_useragent import UserAgent


class WeblioCaller:
    def __init__(self):
        self.weblio_url = "http://www.weblio.jp/content/"
        self.user_agent = UserAgent()

    def simple_weblio(self, word, pos):
        """Description: Call Weblio and return html text along with http status code
        """
        while True:
            print("Performing a http request to weblio")
            req = urllib.request.Request(
                self.weblio_url + quote(word),
                data=None,
                headers={
                    'User-Agent': self.user_agent.random
                }
            )
            with urllib.request.urlopen(req) as r:
                result = r.read()
                status = r.status
                if ( status < 300 ):
                    return (status, result)




