import datetime, copy, warnings
from typing import *
from django.conf import settings
from django.db.models import Model
from django.db.models.fields import files
from django.db.models.query import QuerySet
from django.db.models import Manager
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

def rest_response(value):
    if isinstance(value, list):
        return JsonResponse(value, safe=False, json_dumps_params={"indent":4})
    else:
        return JsonResponse(value, json_dumps_params={"indent":4})

class OrderSet:
    def __init__(self, iterable:Iterable) -> None:
        if not isinstance(iterable, Iterable):
            t = type(iterable)
            raise TypeError(f"'{t}' object is not iterable.")
        self.iterable = list(iterable)
        self._remove_duplicate()

    def add(self,value):
        self.iterable.append(value)
        self._remove_duplicate()

    def add_(self, value):
        ls = copy.deepcopy(self.iterable)
        ls.append(value)
        return OrderSet(ls)

    def remove(self, value):
        self.iterable = [i for i in self.iterable if i != value]

    def remove_(self, value):
        return OrderSet([i for i in self.iterable if i != value])
    
    def _remove_duplicate(self):
        ls = []
        for i in self.iterable:
            while i not in ls:
                ls.append(i)
        self.iterable = ls

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.iterable})'

    def __repr__(self) -> str:
        return str(self)

    def __add__(self, orderset):
        return OrderSet(self.iterable + orderset.iterable)

    def __sub__(self, orderset):
        ls = copy.deepcopy(self.iterable)
        for i in orderset:
            if i in ls:
                ls.remove(i)
        return OrderSet(ls)

    def __iter__(self):
        return iter(self.iterable)

    def __contains__(self, key):
        return (key in self.iterable)

    def __eq__(self, orderset):
        return self.iterable == orderset.iterable

def get_objs_all_attr(objs, attr, ls=[]):
    for obj in objs:
        try:
            ls.append(getattr(obj, attr))
        except AttributeError:
            pass
    return ls

class QToDict:
    def __init__(self, q, request, context={}) -> None:
        self.request = request
        self.context = context
        if isinstance(q, Model):
            self.context.update(self.query_to_dict(q))
        if isinstance(q, QuerySet):
            self.context=self.queryset_to_dict(q)
        assert isinstance(q, Model) or isinstance(q, QuerySet), {
            TypeError("please input value type of Model instance or QuerySet.")
        }

    def query_to_dict(self, query, context={}):
        for attr in self.get_query_attrs(query):
            result = getattr(query, attr)
            if callable(result) and not isinstance(result, Model) and not isinstance(result, Manager):
                result = result()
            if isinstance(result, datetime.datetime):
                context[attr] = str(result).split('.')[0]
            elif isinstance(result, datetime.timedelta):
                context[attr] = str(result).split('.')[0]
            elif isinstance(result, datetime.date):
                context[attr] = str(result)
            elif isinstance(result, files.FieldFile):
                if settings.MEDIA_URL.startswith('/') and settings.MEDIA_URL.endswith('/'):
                    context[attr] = f'{self.request.scheme}://{self.request.get_host()}{settings.MEDIA_URL}{str(result)}'
                else:
                    raise ValueError("MEDIA_URL in settings.py must start with '/' and end with '/'.")
            elif isinstance(result, Model):
                # context[attr] = self.query_to_dict(result)
                context[attr] = result.pk
            elif isinstance(result, Manager):
                # context[attr] = self.queryset_to_dict(result.all())
                context[attr] = [item.pk for item in result.all()]
            else:
                context[attr] = result
        return context

    def queryset_to_dict(self, queryset, context=[]):
        return [copy.deepcopy(self.query_to_dict(query)) for query in queryset]

    @classmethod
    def get_query_attrs(cls, query):
        class SampleModel(Model):
            pass
        attrs = OrderSet(dir(query.__class__)) - OrderSet(dir(SampleModel)).remove_('id')
        attrs = cls.filter_attrs(query, attrs)
        return attrs

    @classmethod
    def filter_attrs(cls, query, attrs):
        attrs_set = copy.deepcopy(attrs)
        for attr in attrs:
            try:
                result = getattr(query, attr)
            except ObjectDoesNotExist:
                attrs_set.remove(attr)
                warnings.warn("you cannot get OneToOne field by realted name, because your model exist ForeignKey or ManyToMany field which point to a same model with OneToOne field.")
                continue
            if isinstance(result, datetime.date) or isinstance(result, datetime.datetime):
                attrs_set.remove("get_next_by_"+attr)
                attrs_set.remove("get_previous_by_"+attr)
            if isinstance(result, Model):
                try:
                    attrs_set.remove(attr+"_id")
                except KeyError:
                    pass
        return attrs_set

    def get_result(self):
        return self.context