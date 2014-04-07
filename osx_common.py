#!/usr/bin/env python
from __future__ import print_function
from subprocess import Popen

class Program(Popen):
	DEBUG = False

	def __init__(self, arg):
		self.init_program(arg)
	def init_program(self, arg):
		if arg: self.args = [arg]
		else: self.args = []
	def append_arg(self, arg):
		if arg: self.args.append(arg)
	def append_args(self, args):
		if args: self.args += args
	def start(self):
		if self.DEBUG: printe(' '.join(["'"+arg+"'" if ' ' in arg else arg for arg in self.args]))
		from subprocess import PIPE
		Popen.__init__(self, self.args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
	def run(self):
		self.start()
		self.wait()
	def communicate(self):
		self.start()
		return Popen.communicate(self)

input = raw_input if hasattr(__builtins__, 'raw_input') else input

def printe(*objects, **kwargs):
	from sys import stderr
	print(*objects, file=stderr, **kwargs)

class UserCancelled(Exception): pass
class Done(Exception): pass
