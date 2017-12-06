# Imports for class InternalErrorMetaClass
import sys                                # core 

import meta.errors                        # target 
# End imports for class InternalErrorMetaClass


class InternalErrorMetaClass(ErrorMetaClass):
  """Meta class of meta.errors.InternalError."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(InternalErrorMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.
