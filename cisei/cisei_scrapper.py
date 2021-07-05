from urllib.parse import urljoin
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests.sessions import Session
import csv
from time import sleep
import requests
from bs4 import BeautifulSoup
from tenacity import retry, wait_fixed
from os import path


class CiseiRequestHandler:
    _DEFAULT_CONNECTION_TIMEOUT = 3
    _DEFAULT_RESPONSE_TIMEOUT = 3
    _URL = "http://www.ciseionline.it/portomondo/ricerca.asp"

    def __init__(self):
        self.timeout = (
            self._DEFAULT_CONNECTION_TIMEOUT,
            self._DEFAULT_RESPONSE_TIMEOUT,
        )
        self.retries = Retry(connect=5, read=2, redirect=5)

        self.session = self._init_session()

    def _init_session(self):
        session = Session()
        session.mount("http://", HTTPAdapter(max_retries=self.retries))
        session.mount("https://", HTTPAdapter(max_retries=self.retries))
        session.headers.update(
            {
                "User-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"
            }
        )
        return session

    def get_surname_soup(self, surname: str):
        custom_header = {
            "input_cognome": surname,
            "input_nome": "",
            "input_dest": "al",
        }
        r = self.session.post(self._URL, custom_header)
        r.raise_for_status()
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        return soup


def scrap_cisei():
    crh = CiseiRequestHandler()
    print(crh.get_surname_soup("Corsini"))