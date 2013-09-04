osx_keychain.py
===============

Want to save passwords securely via Python? Now you can, via OS X's "security" command — and this!

Example
-------

    >>> import osx_keychain
    >>> d = osx_keychain.Domain('mail.google.com')
    >>> d.add_password('interestinglythere', 'correct horse battery staple')
    >>> d.find_password('another_user')
    osx_keychain.PasswordNotFoundError: ...
    >>> d.find_password('interestinglythere')
    'correct horse battery staple'
    >>> d.delete_password('interestinglythere')
