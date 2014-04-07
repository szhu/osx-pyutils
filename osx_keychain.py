#!/usr/bin/env python
'''
    Python interface to OS X's `security` command.

    >>> import osx_keychain
    >>> d = osx_keychain.Domain('example.com')
    >>> d.find_password('interestinglythere')
    Traceback (most recent call last):
    PasswordNotFoundError: security: SecKeychainSearchCopyNext: The specified item could not be found in the keychain.
    >>> d.add_password('interestinglythere', 'correct horse battery staple')
    >>> d.find_password('interestinglythere')
    'correct horse battery staple'
    >>> d.delete_password('interestinglythere')
    >>> d.find_password('interestinglythere')
    Traceback (most recent call last):
    PasswordNotFoundError: security: SecKeychainSearchCopyNext: The specified item could not be found in the keychain.
'''

from __future__ import print_function
from osx_common import Program

class KeychainError(Exception): 
    def __init__(self, raw): self.raw = raw.rstrip('\n')
    def __str__(self): return self.raw
class PasswordNotFoundError(KeychainError): pass


class Security(Program):
    NOT_FOUND = 'SecKeychainSearchCopyNext: The specified item could not be found in the keychain.'
    DELETED = 'password has been deleted.'

    def __init__(self, arg):
        self.init_program('security')
        self.append_arg(arg)


class Domain:
    def __init__(self, server, label=None, keychain='login.keychain'):
        self.server = server
        self.label = label or server
        self.keychain = keychain

    def find_password(self, username=None):
        security = Security('find-internet-password')
        security.append_args([
            '-l', self.label,
            '-s', self.server,
            '-w',
        ])
        if username: security.append_args([
            '-a', username,
        ])
        security.append_args([
            self.keychain,
        ])
        out, err = security.communicate()
        if Security.NOT_FOUND in err: raise PasswordNotFoundError(err)
        elif err: raise KeychainError(err)
        else: return '\n'.join(out.splitlines()) or None

    def delete_password(self, username):
        security = Security('delete-internet-password')
        security.append_args([
            '-l', self.label,
            '-s', self.server,
            '-a', username,
            self.keychain,
        ])
        out, err = security.communicate()
        if Security.DELETED in err: return
        elif Security.NOT_FOUND in err: raise PasswordNotFoundError(err)
        elif err: raise KeychainError(err)
        else: return


    def add_password(self, username, password):
        security = Security('add-internet-password')
        security.append_args([
            '-l', self.label,
            '-s', self.server,
            '-a', username,
            '-w', password,
            self.keychain,
        ])
        out, err = security.communicate()
        if err: raise KeychainError(err)
        else: return

    def __str__(self):
        return '%s(%r, %r)' % (self.__name__, self.server, self.label)

KeychainDomain = Domain # for `import KeychainDomain from ...`
