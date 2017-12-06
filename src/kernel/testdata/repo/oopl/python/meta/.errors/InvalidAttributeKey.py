# Imports for class InvalidAttributeKey
import sys                                # core 

import meta.errors                        # target 
# End imports for class InvalidAttributeKey


class InvalidAttributeKey(Error):
  __metaclass__ = InvalidAttributeKeyMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(InvalidAttributeKey, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
InvalidAttributeKeyClass = InvalidAttributeKey
