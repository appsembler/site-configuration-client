"""
Django cache backend.
"""


class DjangoCache:
    def __init__(self, cache_name, cache_timeout=None):
        self.cache_name = cache_name
        self.cache_timeout = cache_timeout
        self._django_cache = None  # Delay the import since this is initialized during settings

    def get_django_cache(self):
        if not self._django_cache:
            from django.core.cache import caches
            self._django_cache = caches[self.cache_name]
        return self._django_cache

    def set(self, key, value):
        kwargs = {}
        if self.cache_timeout is not None:
            kwargs['timeout'] = self.cache_timeout
        return self.get_django_cache().set(key, value, **kwargs)

    def get(self, key):
        return self.get_django_cache().get(key)
