# Imports for class ExceptionMetaClass
import sys                                # core 
# End imports for class ExceptionMetaClass

protected = Object._meta__protected
private = Object._meta__private


class ExceptionMetaClass(type):
  """Meta class of meta.root.Exception."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(ExceptionMetaClass, cls).__init__(meta__dct, meta__bases, meta__name)
    # User-provided code follows.
