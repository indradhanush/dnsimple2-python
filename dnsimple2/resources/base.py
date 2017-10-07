from collections import MutableSequence
from copy import deepcopy
from dateutil import parser


class BaseResource(object):
    def __init__(self, **kwargs):
        self._raw = kwargs

    @classmethod
    def parse_datetime(cls, value):
        return parser.parse(value) if value else None

    @classmethod
    def parse_date(cls, value):
        datetime = cls.parse_datetime(value)
        return datetime.date() if datetime else None


class ResourceList(MutableSequence):
    """A list of resources"""
    def __init__(self, service, total_entries, per_page, list_args):
        """
        :param service: The service from which the ResourceList was created.
        :type: dnsimple2.services.BaseService
        :param total_entries: Total no. of elements
        :type: int
        :param per_page: No. of items on each page
        :type: int
        :param args_list: List of arguments that need to be passed to the `service.list` method
        :type: list
        """
        self._list_args = list_args
        self._service = service

        self.total_entries = total_entries
        self.per_page = per_page

        self._list = []

    def __len__(self):
        return self.total_entries

    def __getitem__(self, index):
        if index > self.total_entries:
            raise IndexError

        try:
            if self._list[index] is None:
                self._fetch(index)
        except IndexError:
            self._fetch(index)

        return self._list[index]

    def __delitem__(self, index):
        """We do not allow delete operation"""
        raise NotImplementedError

    def __setitem__(self, index, value):
        """We do not allow this to be changed externally"""
        raise NotImplementedError

    def _fetch(self, i):
        page_required = divmod(i, self.per_page)[0] + 1

        args = deepcopy(self._list_args)
        args.append(page_required)
        resources, _ = self._service._list(*args)

        self.update(resources, page_required)

    def update(self, resources, page):
        high = page * self.per_page
        low = high - self.per_page

        length = len(self._list)
        if low > length:
            self._list.extend([None] * (low - length))

        for resource, index in zip(resources, range(low, high)):
            try:
                self._list[index] = resource
            except IndexError:
                self._list.insert(index, resource)

    def insert(self, index, value):
        self._list.insert(index, value)
