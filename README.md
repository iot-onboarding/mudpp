# MUD Pretty Printer

This library presents two interfaces: browser and RESTful.  The response is an HTML formatted string of sentences that explain the ACLs found in a MUD file.

The entry points are defined in mudpp/__init__.py.  This is suitable for flask or wsgi interfaces.  The main parsing code can be found in mudpp/mudpp.py.  If you make use of the browser interface, you will need to modify the template if you do not use this mechanism in combination with mudmaker.

You can try a running version of it at https://www.mudmaker.org/mudrest/mudpp

