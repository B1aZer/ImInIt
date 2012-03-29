from datetime import datetime
from flaskext.babel import gettext, ngettext
from flask import current_app,request

try:
    import json
except ImportError:
    import simplejson as json

try:
    from bson.objectid import ObjectId
except:
    pass


class APIEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.ctime()
        elif isinstance(obj, datetime.time):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def timesince(dt, default=None):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    NB: when/if Babel 1.0 releaseduse format_timedelta/timedeltaformat instead
    """

    if default is None:
        default = gettext("just now")

    now = datetime.utcnow()
    diff = now - dt

    years = diff.days / 365
    months = diff.days / 30
    weeks = diff.days / 7
    days = diff.days
    hours = diff.seconds / 3600
    minutes = diff.seconds / 60
    seconds = diff.seconds

    periods = (
        (years, ngettext("%(num)s year", "%(num)s years", num=years)),
        (months, ngettext("%(num)s month", "%(num)s months", num=months)),
        (weeks, ngettext("%(num)s week", "%(num)s weeks", num=weeks)),
        (days, ngettext("%(num)s day", "%(num)s days", num=days)),
        (hours, ngettext("%(num)s hour", "%(num)s hours", num=hours)),
        (minutes, ngettext("%(num)s minute", "%(num)s minutes", num=minutes)),
        (seconds, ngettext("%(num)s second", "%(num)s seconds", num=seconds)),
    )

    for period, trans in periods:
        if period:
            return gettext("%(period)s ago", period=trans)

    return default

def timebefore(dt, default=None):

    if default is None:
        default = gettext("passed")

    now = datetime.utcnow()
    diff = dt - now

    years = diff.days / 365
    months = diff.days / 30
    weeks = diff.days / 7
    days = diff.days
    hours = diff.seconds / 3600
    minutes = diff.seconds / 60
    seconds = diff.seconds

    periods = (
        (years, ngettext("%(num)s year", "%(num)s years", num=years)),
        (months, ngettext("%(num)s month", "%(num)s months", num=months)),
        (weeks, ngettext("%(num)s week", "%(num)s weeks", num=weeks)),
        (days, ngettext("%(num)s day", "%(num)s days", num=days)),
        (hours, ngettext("%(num)s hour", "%(num)s hours", num=hours)),
        (minutes, ngettext("%(num)s minute", "%(num)s minutes", num=minutes)),
        (seconds, ngettext("%(num)s second", "%(num)s seconds", num=seconds)),
    )

    for period, trans in periods:
        if period:
            return gettext("%(period)s left", period=trans)

    return default

def jsonify(*args, **kwargs):
    #return Response(json.dumps(data, cls=DateEncoder),
    #mimetype='application/json')
    return current_app.response_class(json.dumps(dict(*args, **kwargs),
        indent=None if request.is_xhr else 2, cls=DateEncoder), mimetype='application/json')

