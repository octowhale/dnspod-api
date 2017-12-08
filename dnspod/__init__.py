import json
import requests


class DnspodApi(object):
    def __init__(self, user_token=None):
        self.domain = 'api.dnspod.com'
        self.base_url = 'https://' + self.domain
        self.user_token = user_token

        self.s = requests.session()
        self.s.headers.update({"Content-type": "application/x-www-form-urlencoded",
                               "Accept": "text/json",
                               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    def login(self, email, password):

        uri = '/Auth'
        params = dict(login_email=email,
                      login_password=password,
                      format='json')

        r = self.s.post(self.base_url + uri, data=params)

        resp_json = json.loads(r.text)
        if resp_json.get('status').get('code') != "1":
            raise resp_json.get('status').get('message')
        self.user_token = resp_json.get('user_token')

    def do_request(self, method, **kw):

        if self.user_token is None:
            raise "No user_token, login first"

        params = dict(user_token=self.user_token,
                      format='json')
        params.update(kw)

        url = '{baseurl}/{method}'.format(baseurl=self.base_url, method=method)
        r = self.s.post(url,
                        data=params)
        resp_json = json.loads(r.text)

        if resp_json.get('status').get('code') != "1":
            raise resp_json.get('status').get('message')

        print("*" * 10)
        print(json.dumps(resp_json, indent=4, sort_keys=True))
