# Imports for class PrivateMethodMetaClass
import sys                                # core 

import meta.errors                        # target 
# End imports for class PrivateMethodMetaClass


class PrivateMethodMetaClass(ErrorMetaClass):
  """Meta class of meta.errors.PrivateMethod."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(PrivateMethodMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.
