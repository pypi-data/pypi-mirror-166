from functools import wraps
from django.http import HttpResponse, JsonResponse
from django.db.models.query import QuerySet
from django.db.models import Model
from django.http.response import HttpResponseBase
from .utils import QToDict, rest_response

def url_pattern(url_path, isregex=False, **kwargs):  # url_path, isregex, name(template_name)
    def middle(func):
        @wraps(func)
        def inner(request, *args, **innerkwargs):
            result = func(request, *args, **innerkwargs)
            return result
        if not hasattr(url_pattern, "_all_func"):
            url_pattern._all_func = []
        context = {}
        context['url_path'] = url_path
        context['isregex'] = isregex
        context['func'] = func
        context['name'] = kwargs.get('name') or func.__name__
        url_pattern._all_func.append(context)
        return inner
    return middle

def rest_controller(func):
    @wraps(func)
    def deal(request):
        result = func(request)
        if result is None:
            return result
        elif isinstance(result, dict):
            return rest_response(result)
        elif isinstance(result, Model) or isinstance(result, QuerySet):
            data = QToDict(result, request).get_result()
            return rest_response(data)
        elif isinstance(result, HttpResponseBase):
            return result
        elif isinstance(result, set or list):
            return rest_response(list(result), safe=False)
        else:
            return HttpResponse(result)
    return deal