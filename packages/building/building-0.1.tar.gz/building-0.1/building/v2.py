import copy
import functools
from datetime import datetime
from typing import Optional, Union
import requests.models
from deceit.exceptions import ApiException
from building.base import BigApi


def paginate_and_yield(fn):
    @functools.wraps(fn)
    def decorated_fn(self: BigApi, n_max=0, *args, **kwargs):
        n_total = 0
        page = kwargs.pop('page', None) or 1
        limit = kwargs.pop('limit', None) or 250
        done = False
        while not done:
            self.log.debug('%s getting page %s', fn.__name__, page)
            results = fn(self, page=page, limit=limit, *args, **kwargs)
            n_len = len(results)
            for x in results:
                n_total += 1
                if n_total > n_max > 0:
                    break
                yield x
            page += 1
            done = n_total >= n_max > 0 or n_len < limit

    return decorated_fn


def paginate(fn):
    @functools.wraps(fn)
    def decorated_fn(self: BigApi, n_max=0, *args, **kwargs):
        page = kwargs.pop('page', None) or 1
        limit = kwargs.pop('limit', None) or 250
        done = False
        all_results = []
        while not done:
            self.log.debug('%s getting page %s', fn.__name__, page)
            results_page = fn(self, page=page, limit=limit, *args, **kwargs)
            n_len = len(results_page)
            n_end = n_len
            if n_max > 0:
                n_end = min(n_max - len(all_results), n_len)
            all_results += results_page[:n_end]
            page += 1
            done = len(all_results) >= n_max > 0 or n_len < limit
        return all_results

    return decorated_fn


class BigV2Exception(ApiException):
    """
    marker class to catch exceptions thrown by the v2 api
    """
    pass


class BigV2Api(BigApi):
    exception_class = BigV2Exception
    version = 'v2'

    def time(self, raw: bool = False) -> Union[requests.models.Response, dict]:
        """Returns the system timestamp at the time of the request. The time
        resource is useful for validating API authentication details and
        testing client connections.

        :raises: BigV2ApiException
        """
        return self.get('time')

    def order_page(
            self,
            page: Optional[int] = None,
            limit: Optional[int] = None,
            min_date_modified: Optional[datetime] = None,
            raw: bool = False,
            **kwargs):
        """Gets a list of orders using the filter query. The default sort is by
        order id, from lowest to highest.

        :raises: BigV2Exception
        """
        params = copy.copy(kwargs)
        params.update(
            limit=min(limit or 250, 250),
            page=page or 1)
        if min_date_modified:
            params['min_date_modified'] = min_date_modified
        return self.get('orders', params=params, raw=raw)

    orders = paginate(order_page)
    yield_orders = paginate_and_yield(order_page)
