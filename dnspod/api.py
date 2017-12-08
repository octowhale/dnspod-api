#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#

import requests
import json


class Api(object):
    # def __init__(self, email, password, **kw):
    def __init__(self):
        self.api_domain = "api.dnspod.com"
        self.base_url = "https://api.dnspod.com"

        self.email = None
        self.password = None
        self.user_token = None
        self.s = requests.session()

        if self.email is not None or self.password is not None:
            self.login()

    def login(self):
        params = dict(
            login_email=self.email,
            login_password=self.password,
            format="json"
        )

        uri = r'/Auth'
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/json",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

        r = self.s.post(self.base_url + uri,
                        data=params, headers=headers)

        # print(r.text)
        data = json.loads(r.text)

        if data['status']['code'] != "1":
            print(data['status']['message'])
            exit(1)

        self.user_token = data['user_token']

        return self.s

    def version(self):
        """check api version"""

        uri = '/Info.Version'
        data = self.request(uri)
        version = data['status']['message']

        print(version)
        return version

    def request(self, uri, **kw):
        """do api request"""
        if self.user_token is None:
            print('User login failed')
            return False

        url = self.base_url + uri
        params = dict(
            user_token=self.user_token,
            format='json'
        )

        params.update(kw)

        r = self.s.post(url, data=params)

        # print(r.text)
        return json.loads(r.text)

    def user_detail(self):
        uri = '/User.Detail'
        data = self.request(uri)
        print(data)

    def user_modify(self, **kw):
        """
        real_name  :  Your real name for personal accounts,and company name for company accounts.
        nick Your  :  nickname that make it easier to contact to the users.
        telephone  :  The users’ phone number.
        im         :  Your Instant Messaging account.
        """
        uri = '/User.Modify'

        if not kw:
            raise ""
        data = self.request(uri, kw)


if __name__ == "__main__":

    from user import *
    client = Api()
    client.email = email
    client.password = password

    data = client.login()
    # print(data)
    client.version()
    client.user_detail()
