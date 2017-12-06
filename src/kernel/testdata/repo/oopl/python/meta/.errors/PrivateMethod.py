# Imports for class PrivateMethod
import sys                                # core 

import meta.errors                        # target 
# End imports for class PrivateMethod


class PrivateMethod(Error):
  __metaclass__ = PrivateMethodMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(PrivateMethod, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
PrivateMethodClass = PrivateMethod
