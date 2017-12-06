# Imports for class InvalidType
import sys                                # core 

import meta.errors                        # target 
# End imports for class InvalidType


class InvalidType(Error):
  __metaclass__ = InvalidTypeMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(InvalidType, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
InvalidTypeClass = InvalidType
