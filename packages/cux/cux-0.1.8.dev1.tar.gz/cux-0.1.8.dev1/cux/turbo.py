#!/usr/bin/env python
from enum import Enum, auto
import os
import random
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from typing import ClassVar, Dict

import codefast as cf
import joblib
import requests


@dataclass
class UserInfo:
    name: ClassVar[str] = "liugaoang"
    password: ClassVar[str] = "5a5ef4356682cd686b23dce660e9a83d"


class Env(Enum):
    PRODUCT = auto()
    DEV = auto()
    TEST = auto()


class TurboUrl(Enum):
    PRODUCT = "https://turbo.mgvai.cn"
    DEV = "https://turbo.dev.mgvai.cn"
    TEST = "https://turbo.test.mgvai.cn"


class Turbo:
    def __init__(self, env: Env) -> None:
        self.session = requests.Session()
        self.env = env
        self.token_file = '/tmp/turbo_token_{}.joblib'.format(self.env.name)
        self.session_file = '/tmp/ses_{}.joblib'.format(self.env.name)
        self.url = TurboUrl[self.env.name].value
        self.token = None

    def login(self):
        if self.is_session_valid():
            cf.info(f'Token {self.token} still valid')
            return

        cf.warning(f'Token {self.token} expired')
        url = self.url + '/api/user_authority/user/login'
        params = {'username': UserInfo.name, 'password': UserInfo.password}
        resp = self.session.post(url, data=params)
        cf.info(resp, resp.text, resp.json())

        self.token = resp.json()['results']['session']
        cf.info(resp, resp.text)
        joblib.dump(self.token, self.token_file)
        joblib.dump(self.session, self.session_file)
        return self

    def is_session_valid(self) -> bool:
        '''check if previous session still valid or not'''
        if not cf.io.exists(self.session_file):
            return False
        url = self.url + '/api/user_authority/user/info'
        self.session = joblib.load(self.session_file)
        self.token = joblib.load(self.token_file)
        resp = self.session.get(
            url, headers={'Cookie': f'turbo_session={self.token}'})
        return resp.json()['code'] == 200

    def status(self) -> Dict:
        url = self.url + '/api/user_authority/user/info'
        self.session = joblib.load(self.session_file)
        self.token = joblib.load(self.token_file)
        resp = self.session.get(
            url,
            headers={'Cookie': f'turbo_session={self.token}'})
        cf.info(resp, resp.json())
        return resp.json()


if __name__ == '__main__':
    tb = Turbo(Env.TEST)
    tb.login()
    tb.status()
    tb.redo()
