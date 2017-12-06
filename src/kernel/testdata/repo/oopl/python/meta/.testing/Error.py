# Imports for class Error
import sys                                # core 
# End imports for class Error


class Error(Exception):
  __metaclass__ = ErrorMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(Error, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
ErrorClass = Error
