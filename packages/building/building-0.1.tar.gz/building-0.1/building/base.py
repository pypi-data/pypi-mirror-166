import posixpath
from deceit.api_client import ApiClient
from waddle import ParamBunch


class BigApi(ApiClient):
    exception_class = None
    version = None

    def __init__(self, conf: ParamBunch, *args, default_timeout=None, **kwargs):
        base_url = kwargs.pop('base_url', None)
        store = kwargs.get('store') or conf.store
        if not base_url:
            base_url = conf.get('base_url') or 'https://api.bigcommerce.com'
            base_url = posixpath.join(base_url, 'stores', store, self.version)

        kwargs.setdefault('exception_class', self.__class__.exception_class)
        super().__init__(
            *args,
            default_timeout=default_timeout,
            base_url=base_url,
            **kwargs)
        self.access_token = kwargs.get('access_token') or conf.access_token

    def headers(self, *args, **kwargs):
        h = super().headers(*args, **kwargs)
        h['x-auth-token'] = self.access_token
        h.setdefault('content-type', 'application/json')
        h.setdefault('accept', 'application/json')
        return h


