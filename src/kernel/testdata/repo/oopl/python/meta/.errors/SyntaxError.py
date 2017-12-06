# Imports for class SyntaxError
import sys                                # core 

import meta.errors                        # target 
# End imports for class SyntaxError


class SyntaxError(Error):
  __metaclass__ = SyntaxErrorMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(SyntaxError, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
SyntaxErrorClass = SyntaxError
