# Imports for class LoggerMetaClass
import sys                                # core 

import meta.root                          # target 
# End imports for class LoggerMetaClass


class LoggerMetaClass(meta.root.ObjectMetaClass):
  """Meta class of meta.core.Logger."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(LoggerMetaClass, cls).__init__(meta__dct, meta__bases, meta__name)
    # User-provided code follows.
