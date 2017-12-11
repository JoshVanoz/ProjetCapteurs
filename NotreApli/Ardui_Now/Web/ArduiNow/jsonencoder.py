import datetime

import decimal

from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        """JSON encoder function for SQLAlchemy special classes."""
        if isinstance(obj, datetime.datetime):
            return int(obj.timestamp()*1000)
        elif isinstance(obj, decimal.Decimal):
            return float(obj)

        return JSONEncoder.default(self, obj)