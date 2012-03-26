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



def jsonify(*args, **kwargs):
    #return Response(json.dumps(data, cls=DateEncoder),
    #mimetype='application/json')
    return current_app.response_class(json.dumps(dict(*args, **kwargs),
        indent=None if request.is_xhr else 2, cls=DateEncoder), mimetype='application/json')

