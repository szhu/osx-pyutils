osx-pyutils
===========

This module contains Python interfaces to some command-line programs that come with Mac OS:

* `osx_keychain` uses [`security`][] to manipulate keychains
* `osx_pboard` uses [`pbcopy`][] and [`pbpaste`][] to manipulate the clipboard
* `osx_defaults` uses [`defaults`][] to manipulate preferences

Most of these features are also accessible via [PyObjC][], which takes some time to import. `osx-pyutils` is designed to be used by shell scripts that live for much shorter than that by working with the already-compiled tools. `osx-pyutils` can also be used as convenience functions for those who don't want to directly deal with spawning new processes.

This project is currently alpha-quality work and welcomes PRs. Please contribute if you can!

[PyObjC]: https://pythonhosted.org/pyobjc/
[`security`]: https://developer.apple.com/library/mac/Documentation/Darwin/Reference/ManPages/man1/security.1.html
[`pbcopy`]: https://developer.apple.com/library/mac/Documentation/Darwin/Reference/ManPages/man1/pbcopy.1.html
[`pbpaste`]: https://developer.apple.com/library/mac/Documentation/Darwin/Reference/ManPages/man1/pbpaste.1.html
[`defaults`]: https://developer.apple.com/library/mac/Documentation/Darwin/Reference/ManPages/man1/defaults.1.html

osx_keychain.py
-------

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

Here's what the result looks like from *Keychain Access* (before deleting):

![screenshot](https://f.cloud.github.com/assets/1570168/1078791/2ca6c7a0-1534-11e3-87f0-9358917fc58e.png)
