# Imports for class ExitingMetaClass
import sys                                # core 

import meta.errors                        # target 
# End imports for class ExitingMetaClass


class ExitingMetaClass(ErrorMetaClass):
  """Meta class of meta.errors.Exiting."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(ExitingMetaClass, cls).__init__(meta__dct, meta__bases, meta__name)
    # User-provided code follows.
