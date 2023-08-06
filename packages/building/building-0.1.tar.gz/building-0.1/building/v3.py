import copy
import functools
from datetime import datetime
from typing import Optional, Dict, Any

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
            response = fn(self, page=page, limit=limit, *args, **kwargs)
            results = response['data']
            pagination = response.get('meta', {}).get('pagination') or {}
            for x in results:
                n_total += 1
                if n_total > n_max > 0:
                    break
                yield x
            page += 1
            total_pages = pagination.get('total_pages') or 0
            done = n_total >= n_max > 0 or page > total_pages

    return decorated_fn


def paginate(fn):
    @functools.wraps(fn)
    def decorated_fn(self: BigApi, n_max=0, *args, **kwargs):
        yield_fn = paginate_and_yield(fn)
        return list(yield_fn(self, n_max=n_max, *args, **kwargs))

    return decorated_fn


class BigV3Exception(ApiException):
    """
    marker class to catch exceptions thrown by the v3 api
    """
    pass


class BigV3Api(BigApi):
    exception_class = BigV3Exception
    version = 'v3'

    def logs(
            self,
            page: Optional[int] = None,
            limit: Optional[int] = None,
            **kwargs,
    ):
        """This API can be used to retrieve and filter for specific store logs.
        """
        params = copy.copy(kwargs)
        params.update(
            limit=min(limit or 250, 250),
            page=page or 1)
        return self.get('store/systemlogs', params=params)

    def product_page(self,
            page: Optional[int] = None,
            limit: Optional[int] = None,
            min_date_modified: Optional[datetime] = None,
            raw: bool = False,
            **kwargs) -> Dict[Any, Any]:
        """Returns a list of Products. Optional filter parameters can be
        passed in.

        :Keyword Arguments:
            * *include* (``str``) --
               Sub-resources to include on a product, in a comma-separated list. If options or modifiers is used, results are limited to 10 per page.
                   Allowed values:
                   ``variants``
                   ``images``
                   ``custom_fields``
                   ``bulk_pricing_rules``
                   ``primary_image``
                   ``modifiers``
                   ``options``
                   ``videos``
        :raises: BigV3Exception
        """
        params = copy.copy(kwargs)
        params.update(
            limit=min(limit or 250, 250),
            page=page or 1)
        if min_date_modified:
            params['date_modified:min'] = min_date_modified
        return self.get('catalog/products', params=params, raw=raw)

    def variant_page(self,
            page: Optional[int] = None,
            limit: Optional[int] = None,
            raw: bool = False,
            **kwargs) -> Dict[Any, Any]:
        """Returns a list of all variants in your catalog. Optional parameters
        can be passed in.

        :Keyword Arguments:
        :raises: BigV3Exception
        """
        params = copy.copy(kwargs)
        params.update(
            limit=min(limit or 250, 250),
            page=page or 1)
        return self.get('catalog/variants', params=params, raw=raw)

    products = paginate(product_page)
    yield_products = paginate_and_yield(product_page)
    variants = paginate(variant_page)
    yield_variants = paginate_and_yield(variant_page)
