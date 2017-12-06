# Imports for class Error
import sys                                # core 
# End imports for class Error


class Error(Exception):
  """This is the top-level (within Meta) exception class. It may inherit from
  some non-meta class defined within the base language, but this class
  provides the interface common across all languages for raising exceptions.

  Meta:suppress: reportUnknownTypes
  """
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
