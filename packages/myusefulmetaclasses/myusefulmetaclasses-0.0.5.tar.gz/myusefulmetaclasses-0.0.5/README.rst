MUM: My Useful Metaclasses
==========================

This package contains a bunch of metaclasses that can be of use in many occasions. In particular we have:

 - ``Singleton``: for Singleton objects;
 - ``AbstractSingleton``: for abstract classes whose children will be Singletons;
 - ``NoDuplicates``: this is a generalization of the Singleton concept. If a user calls this class more than once with the same arguments, it will always get the same instance of the first time (but different instances if it is called with other arguments).
 
Installation
------------

``$ pip install myusefulmetaclasses``


Usage
-----

``import mum #that's the real name of the module``

Documentation
-------------

That's it. I have nothing to say more.