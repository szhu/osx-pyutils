#!/usr/bin/env python
'''
    Python interface to OS X's `defaults` command.

'''

from __future__ import print_function
from osx_common import Program

READ_NOT_FOUND = 'does not exist'
DELETE_NOT_FOUND = 'not found'
DELETED = 'password has been deleted.'
TYPE_IS = 'Type is '

STRING = 'string'
DATA = 'data'
INT = 'int'
FLOAT = 'float'
BOOL = 'bool'
DATE = 'date'
ARRAY = 'array'

GLOBAL_DOMAIN='NSGlobalDomain' # or: '-g'
AUTODETECT_TYPE = -1 # TODO not implemented yet

class DefaultsError: 
    def __init__(self, raw): self.raw = raw.rstrip('\n')
    def __str__(self): return self.raw
class NotFoundError(DefaultsError): pass
class InternalError(DefaultsError): pass


from datetime import datetime
from numbers import Real
TYPE_PY_DEFAULTS = [
    (int, 'integer'),
    (Real, 'float'),
    (list, 'array'),
    (tuple, 'array'),
    (object, 'string'),
]
TYPE_DEFAULTS_PY = {
    'array': list,
    'boolean': bool,
    'data': str,
    'date': datetime,
    'dictionary': dict,
    'float': float,
    'integer': int,
    'string': str,
}

def get_py_type(self, t):
    return TYPE_DEFAULTS_PY[t]

def get_defaults_type(self, val):
    for pytype, dtype in TYPE_PY_DEFAULTS:
        if isinstance(val, pytype): return dtype
    raise TypeError()


class Defaults(Program):

    def __init__(self, *args):
        self.init_program('defaults')
        self.append_args(args)

    def append_type(self, type, value):
        if type is None: return
        if type == AUTODETECT_TYPE:
            type = get_defaults_type(value)
        self.append_arg('-' + type)


class Domain:
    def __init__(self, domain=GLOBAL_DOMAIN):
        self.domain = domain

    @staticmethod
    def process_output(out):
        if not out.endswith('\n'): raise InternalError(out)
        return out[:-1]

    def read(self, key):
        defaults = Defaults('read', self.domain, key)
        out, err = defaults.communicate()
        if READ_NOT_FOUND in err: raise NotFoundError(err)
        elif err: raise DefaultsError(err)
        else: return self.process_output(out)

    def read_type(self, key):
        defaults = Defaults('read-type', self.domain, key)
        out, err = defaults.communicate()
        if READ_NOT_FOUND in err: raise NotFoundError(err)
        elif err: raise DefaultsError(err)
        if not out.startswith(TYPE_IS): raise InternalError(out)
        else: return self.process_output(out[len(TYPE_IS):])

    def delete(self, key):
        defaults = Defaults('delete', self.domain, key)
        out, err = defaults.communicate()
        if DELETE_NOT_FOUND in err: raise NotFoundError(err)
        elif err: raise DefaultsError(err)
        else: return out

    def write(self, key, value, type=None):
        defaults = Defaults('write', self.domain, key)
        defaults.append_type(type, value)
        defaults.append_arg(str(value))
        out, err = defaults.communicate()
        if err: raise DefaultsError(err)
        else: return out


    def __str__(self):
        return '%s(%r, %r)' % (self.__name__, self.domain)

DefaultsDomain = Domain # for `import DefaultsDomain from ...`
