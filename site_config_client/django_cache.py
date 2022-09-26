"""
Django cache backend.
"""


class DjangoCache:
    """
    Allows Site Configuration client to configure caching with Django
    """

    DEFAULT_TIMEOUT = 300  # 5 minutes

    def __init__(self, cache_name, cache_timeout):
        self.cache_name = cache_name
        self.cache_timeout = int(cache_timeout or self.DEFAULT_TIMEOUT)
        self._django_cache = None

    def get_django_cache(self):
        """
        Lazily instantiate Django cache to avoid `ImproperlyConfigured` error.
        """
        if not self._django_cache:
            from django.core.cache import caches
            self._django_cache = caches[self.cache_name]
        return self._django_cache

    def set(self, key, value):
        return self.get_django_cache().set(key, value, timeout=self.cache_timeout)

    def get(self, key):
        return self.get_django_cache().get(key)

    def delete(self, key):
        return self.get_django_cache().delete(key)
