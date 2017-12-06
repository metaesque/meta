# Imports for class ProtectedMethod
import sys                                # core 

import meta.errors                        # target 
# End imports for class ProtectedMethod


class ProtectedMethod(Error):
  __metaclass__ = ProtectedMethodMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(ProtectedMethod, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
ProtectedMethodClass = ProtectedMethod
