# Imports for class ProtectedMethodMetaClass
import sys                                # core 

import meta.errors                        # target 
# End imports for class ProtectedMethodMetaClass


class ProtectedMethodMetaClass(ErrorMetaClass):
  """Meta class of meta.errors.ProtectedMethod."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(ProtectedMethodMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.
