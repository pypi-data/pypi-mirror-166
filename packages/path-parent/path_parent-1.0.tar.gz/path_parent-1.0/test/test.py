import sys

print(sys.path)

from ..path_parent import p		    # add '..' to path setting;
print(sys.path)

from ..path_parent import pp		# add '../..' to path setting;
print(sys.path)

from ..path_parent import ppp		# add '../../..' to path setting;
print(sys.path)

from .. import path_parent			# nothing happen;

path_parent.clear("../..")			# remove only '../..';
print(sys.path)

path_parent.clear("..\..\..")		# nothing removed, not backslash;
print(sys.path)

path_parent.clear()			        # remove all '..', '../..' and '../../..';
print(sys.path)
