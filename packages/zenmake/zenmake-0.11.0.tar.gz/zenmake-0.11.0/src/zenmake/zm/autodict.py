# coding=utf-8
#

"""
 Copyright (c) 2019, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

from copy import deepcopy
from collections.abc import Mapping as maptype

class AutoDict(dict):
    """
    This class provides dot notation and auto creation of items.
    Usually inheritance from the built-in dict type is a bad idea.
    Especially if you want to override __*item__ methods.
    But it is normal internal solution with a good performance if you just want
    to have a dot notation and auto creation of items.
    Just don't override __*item__ methods.
    """

    def __missing__(self, key):
        val = AutoDict()
        self[key] = val
        return val

    def __getattr__(self, name):
        return self[name] # this calls __missing__ if name doesn't exist

    def __setattr__(self, name, value):
        self[name] = value

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo):
        result = AutoDict()
        memo[id(self)] = result
        for k, v in self.items():
            result[deepcopy(k, memo)] = deepcopy(v, memo)
        # It's not really necessary to copy attrs
        #for k, v in self.__dict__.items():
        #    setattr(result, k, deepcopy(v, memo))
        return result

    def copy(self):
        """ shallow copy """
        return AutoDict(super().copy())

    def getByDots(self, keystring, default = None):
        """
        Get value using a dot notation string
        """
        keys = keystring.split('.')
        _dict = self
        for k in keys[:-1]:
            value = _dict.get(k, None)
            if value is None or not isinstance(value, maptype):
                return default
            _dict = value
        return _dict.get(keys[-1], default)
