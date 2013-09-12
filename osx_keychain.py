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
		Popen.__init__(self, self.args, stdout=PIPE, stderr=PIPE, universal_newlines=True)
	def run(self):
		self.start()
		self.wait()
	def communicate(self):
		self.start()
		return Popen.communicate(self)

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


if hasattr(__builtins__, 'raw_input'):
	input = __builtins__.raw_input

def printe(*objects, **kwargs):
	from sys import stderr
	print(*objects, file=stderr, **kwargs)


class UserCancelled: pass
class Done: pass

class KeychainError: 
	def __init__(self, raw): self.raw = raw.rstrip('\n')
	def __str__(self): return self.raw
class PasswordNotFoundError(KeychainError): pass



if __name__ == '__main__': pass
