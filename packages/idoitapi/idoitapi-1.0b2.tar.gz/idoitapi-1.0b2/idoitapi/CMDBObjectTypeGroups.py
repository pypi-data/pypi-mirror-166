"""
Requests for API namespace 'cmdb.object_type_groups'
"""

from idoitapi.Request import Request
from idoitapi.APIException import InvalidParams


class CMDBObjectTypeGroups(Request):

    ORDER_BY_TITLE = 'title'
    ORDER_BY_STATUS = 'status'
    ORDER_BY_CONSTANT = 'constant'
    ORDER_BY_ID = 'id'

    SORT_ASCENDING = 'asc'
    SORT_DESCENDING = 'desc'

    def read(self, order_by=None, sort_direction=None, limit=None):
        """
        Fetch object type groups

        :param str order_by: (optional) Order by 'title', 'status',
            'constant', or 'id'
        :param str sort_direction: (optional) Sort ascending ('asc') or
            descending ('desc')
        :param int limit: (optional) Limit result set
        :return: List of object type groups
        :rtype: list
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params = dict()

        if order_by is not None:
            if order_by not in ('title', 'status', 'constant', 'id'):
                raise InvalidParams(message='"{}" is not a valid order parameter'.format(order_by))
            params['order_by'] = order_by

        if sort_direction is not None:
            if sort_direction.lower() not in ('asc', 'desc'):
                raise InvalidParams(message='"{}" is not a valid sort_direction parameter'.format(sort_direction))
            params['sort'] = sort_direction

        if limit is not None:
            if not isinstance(limit, int) or limit < 0:
                raise InvalidParams(message='"{}" is not a valid limit parameter'.format(limit))
            params['limit'] = limit

        return self._api.request(
            'cmdb.object_type_groups.read',
            params
        )
