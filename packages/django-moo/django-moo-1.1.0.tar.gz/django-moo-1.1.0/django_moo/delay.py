import time
from urllib import parse
from .settings import get_setting
from .decorators import url_pattern
from .utils import get_objs_all_attr
from django.urls import get_resolver, path, re_path

def set_path():
    apps_route_prefix = get_setting().get('DJANGO_MOO_URL', {})
    if not hasattr(url_pattern, '_all_func'):
        url_pattern._all_func = []
    url_patterns = get_resolver().url_patterns
    for c in url_pattern._all_func:
        url_path = c.get('url_path')
        func = c.get('func')
        name = c.get('name')
        app_name = func.__module__.split('.')[0]   
        prefix = apps_route_prefix.get(app_name)
        if prefix is None:
            prefix = ''
        url_path = parse.urljoin(prefix, url_path)
        if c.get('isregex'):
            p = re_path(url_path, func, name=name)
        else:
            p = path(url_path, func, name=name)
        if p.name not in get_objs_all_attr(url_patterns, "name"):
            url_patterns.append(p)

def delay_thread():
    time.sleep(0.5)
    set_path()