from dateutil import parser


class BaseResource(object):
    def parse_datetime(self, value):
        return parser.parse(value) if value else None
