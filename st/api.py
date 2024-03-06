import os

from src.utils import RateLimiter, ensure_directory


class ST:

    base_url = 'https://api.spacetraders.io/v2'

    def __init__(self, token_fp):
        self.token_fp = token_fp
        self.rate_limiter = RateLimiter()

        ensure_directory(token_fp)

    def get_token(self, callsign):
        with open(os.path.join(self.token_fp, callsign), 'r') as f:
            return f.read()

    def request(self, endpoint='', method='GET', params=None, data=None, json=None, headers={}, token=None):

        url = os.path.join(self.base_url, endpoint)
        kwargs = {k: v for k, v in {'params': params, 'data': data, 'json': json}.items() if v}

        if token:
            headers['Authorization'] = f'Bearer {token}'

        if json or data:
            headers['Content-Type'] = 'application/json'

        if headers:
            kwargs['headers'] = headers

        result = self.rate_limiter.queue_request((method, url), kwargs)

        if result.ok:
            return result.json()
        else:
            return result

    def register_agent(self, callsign, faction):
        result = self.request(
            'register',
            'POST',
            json={'symbol': callsign, 'faction': faction}
        )

        return result

        token = result['data']['token']
        with open(os.path.join(self.token_fp, callsign), 'w+') as f:
            f.write(token)

        return result

    def get_agent(self, token=None, callsign=None):
        if not token:
            token = self.get_token(callsign)

        try:
            return Agent(self, token)
        except Exception as e:
            print(e)


class BaseEntity:

    endpoint = ''

    def __init__(self, api, token=None, data=None):
        self.api = api
        self.token = token
        if data:
            self.data = data
        else:
            self.update_data()

    def __getattr__(self, name):
        return self.data.get(name, None)

    def __str__(self):
        return f"{type(self).__name__}: {self.symbol}"

    def __repr__(self):
        return f"{type(self).__name__}: {self.data}"

    def request(self, **kwargs):
        if 'endpoint' in kwargs and self.endpoint not in kwargs['endpoint']:
            kwargs['endpoint'] = os.path.join(self.endpoint, kwargs['endpoint'])
        return self.api.request(**kwargs)

    def update_data(self):
        self.data = self.request(token=self.token)['data']


class Agent(BaseEntity):

    endpoint = 'my/agent'

    def __init__(self, api, token, data=None):
        super().__init__(api, token, data)
