#!/usr/bin/env python
'''
    Python interface to OS X's `pbcopy` and `pbpaste` commands.
    >>> import osx_pboard
    >>> old_clipboard = osx_pboard.get_clipboard()
    >>> osx_pboard.set_clipboard('dsfhjshdfjkdsf')
    >>> osx_pboard.get_clipboard()
    'dsfhjshdfjkdsf'
    >>> osx_pboard.set_clipboard(old_clipboard)
'''

from __future__ import print_function
from osx_common import Program

class PboardError: 
    def __init__(self, raw): self.raw = raw.rstrip('\n')
    def __str__(self): return self.raw

class Pboard(Program):
    def add_pboard(self, pboard):
        if pboard:
            self.append_args(['-pboard', pboard])

class Copy(Pboard):
    def __init__(self, pboard=None):
        self.init_program('pbcopy')
        self.add_pboard(pboard)

    def copy(self, contents):
        self.start()
        self.stdin.write(contents)
        self.stdin.close()
        self.wait()

class Paste(Pboard):
    def __init__(self, pboard=None):
        self.init_program('pbpaste')
        self.add_pboard(pboard)

    def paste(self):
        out, err = self.communicate()
        if err: raise PboardError(err)
        return out

def set_clipboard(contents):
    Copy().copy(contents)

def get_clipboard():
    return Paste().paste()
