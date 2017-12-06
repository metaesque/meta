# Imports for class ErrorMetaClass
import sys                                # core 
# End imports for class ErrorMetaClass


class ErrorMetaClass(type):
  """Meta class of meta.errors.Error."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(ErrorMetaClass, cls).__init__(meta__dct, meta__bases, meta__name)
    # User-provided code follows.
