# Imports for class InvalidConstructId
import sys                                # core 

import meta.errors                        # target 
# End imports for class InvalidConstructId


class InvalidConstructId(Error):
  __metaclass__ = InvalidConstructIdMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(InvalidConstructId, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
InvalidConstructIdClass = InvalidConstructId
