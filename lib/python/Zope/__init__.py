"""Initialize the Zope Package and provide a published module
"""

#######################################################################
# We need to get the right BTree extensions loaded
import sys, os, App.FindHomes
sys.path.insert(0, os.path.join(SOFTWARE_HOME, 'ZopeZODB3'))
#######################################################################

import ZODB, ZODB.ZApplication, imp
import Globals, OFS.Application, sys

Globals.BobobaseName = '%s/Data.fs' % Globals.data_dir
Globals.DatabaseVersion='3'

# Import products
OFS.Application.import_products()

# Open the database
try:
    # Try to use custom storage
    m=imp.find_module('custom_zodb',[INSTANCE_HOME])
except:
    import ZODB.FileStorage
    DB=ZODB.FileStorage.FileStorage(Globals.BobobaseName)
else:
    m=imp.load_module('Zope.custom_zodb', m[0], m[1], m[2])
    DB=m.Storage
    Globals.BobobaseName = DB.getName()
    sys.modules['Zope.custom_zodb']=m

DB=ZODB.DB(DB)
Globals.DB=DB # Ick, this is temporary until we come up with some registry
Globals.opened.append(DB)
import ClassFactory
DB.setClassFactory(ClassFactory.ClassFactory)

# Set up the "application" object that automagically opens
# connections
app=bobo_application=ZODB.ZApplication.ZApplicationWrapper(
    DB, 'Application', OFS.Application.Application, (),
    Globals.VersionNameName)

# Initialize products:
c=app()
OFS.Application.initialize(c)
c._p_jar.close()
del c

# This is sneaky, but we don't want to play with Main:
sys.modules['Main']=sys.modules['Zope']
