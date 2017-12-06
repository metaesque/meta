# Imports for class Exception
import exceptions                         # core meta: 412
import sys                                # core 
# End imports for class Exception


class Exception(Exception):
  """# The class that all exception classes within the Meta universe should
  # inherit from.
  """
  __metaclass__ = ExceptionMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(Exception, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
ExceptionClass = Exception
