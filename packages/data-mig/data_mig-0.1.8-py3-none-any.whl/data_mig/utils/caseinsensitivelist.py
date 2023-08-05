from collections.abc import Mapping

class CaseInsensitiveList(Mapping):
    def __init__(self, d):
        self._d = d
        self._s = dict((k.lower(), k) for k in d)

    def __contains__(self, k):  # implements `in`
        return k.lower() in self._s

    def __iter__(self):
        return iter(self._s)

    def __len__(self):
        return len(self._s)

    def add(self, name):
        self._lowered_keys.append(name)

    def __getitem__(self, k):
        return self._d[self._s[k.lower()]]

    def to_lowercase(self):
        return [x.lower() for x in self.names]

    def to_uppercase(self):
        return [x.upper() for x in self.names]

    def __bool__(self):
        return len(self.names) > 0

    def actual_key_case(self, k):
        return self._s.get(k.lower())
