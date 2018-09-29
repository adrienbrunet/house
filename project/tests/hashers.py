from collections import OrderedDict

from django.contrib.auth.hashers import BasePasswordHasher


class DummyHasher(BasePasswordHasher):
    """
    This hasher is for local use only.
    It does nothing on purpose to speed things
    when using user passwords hasing
    (when creating users for example)

    /!\ This is not suitable for production.
    """

    algorithm = "dummy_hasher"

    def _load_library(self):
        pass

    def encode(self, password, salt):
        return f"{self.algorithm}${password}"

    def verify(self, password, encoded):
        return self.encode(password, self.salt) == encoded

    def safe_summary(self, encoded):
        algorithm, _hash = encoded.split("$", 2)
        return OrderedDict([("algorithm", algorithm), ("hash", _hash)])
