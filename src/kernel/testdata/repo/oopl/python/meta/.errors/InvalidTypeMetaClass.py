# Imports for class InvalidTypeMetaClass
import sys                                # core 

import meta.errors                        # target 
# End imports for class InvalidTypeMetaClass


class InvalidTypeMetaClass(ErrorMetaClass):
  """Meta class of meta.errors.InvalidType."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(InvalidTypeMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.
