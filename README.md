osx_keychain.py
===============

Want to save passwords securely via Python? Now you can, via OS X's "security" command — and this!

Example
-------

    >>> import osx_keychain
    >>> d = osx_keychain.Domain('example.com')
    >>> d.add_password('interestinglythere', 'correct horse battery staple')
    >>> d.find_password('interestinglythere')
    osx_keychain.PasswordNotFoundError: ...
    >>> d.find_password('interestinglythere')
    'correct horse battery staple'
    >>> d.delete_password('interestinglythere')
    >>> d.find_password('interestinglythere')
    osx_keychain.PasswordNotFoundError: ...

Here's what the result looks like from *Keychain Access* (before deleting, of course):

![screenshot](https://f.cloud.github.com/assets/1570168/1078791/2ca6c7a0-1534-11e3-87f0-9358917fc58e.png)
