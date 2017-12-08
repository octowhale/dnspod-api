#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#

import requests
import json
import re


class Api(object):
    # def __init__(self, email, password, **kw):
    def __init__(self):
        self.api_domain = "api.dnspod.com"
        self.base_url = "https://api.dnspod.com"

        self.email = None
        self.password = None
        self.user_token = None
        self.s = requests.session()
        self.s.headers.update({"Content-type": "application/x-www-form-urlencoded",
                               "Accept": "text/json",
                               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    def login(self):
        params = dict(
            login_email=self.email,
            login_password=self.password,
            format="json"
        )

        uri = r'/Auth'
        r = self.s.post(self.base_url + uri,
                        data=params)

        # print(r.text)
        data = json.loads(r.text)

        if data['status']['code'] != "1":
            print(data['status']['message'])
            exit(1)

        self.user_token = data['user_token']

        return self.s

    def request(self, uri, **kw):
        """do api request"""
        if self.user_token is None:
            self.login()
            print("user_token -> ", self.user_token)

        name = re.sub(r'([A-Z])', r'.\1', uri)
        url = self.base_url + '/' + name[1:]

        print("url -> ", url)
        params = dict(
            user_token=self.user_token,
            format='json'
        )

        params.update(kw)

        r = self.s.post(url, data=params)

        resp_json = json.loads(r.text)

        if resp_json.get('status').get('code') != "1":
            print(resp_json.get('status').get('message'))
            return False

        return json.loads(r.text)


if __name__ == "__main__":

    from user import *
    client = Api()
    client.email = email
    client.password = password

    # data = client.login()
    # print(data)
    # client.version()
    # client.user_detail()

    client.InfoVersion()

    data = client.request('InfoVersion')
    print(data)
