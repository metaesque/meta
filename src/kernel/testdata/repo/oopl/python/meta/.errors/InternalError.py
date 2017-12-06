# Imports for class InternalError
import sys                                # core 

import meta.errors                        # target 
# End imports for class InternalError


class InternalError(Error):
  __metaclass__ = InternalErrorMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(InternalError, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
InternalErrorClass = InternalError
