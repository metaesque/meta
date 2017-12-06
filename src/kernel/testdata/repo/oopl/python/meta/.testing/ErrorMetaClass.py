# Imports for class ErrorMetaClass
import sys                                # core 
# End imports for class ErrorMetaClass

import cStringIO
cStringIOClass = cStringIO.StringIO().__class__
import copy
ENV = copy.copy(os.environ)


class ErrorMetaClass(meta.root.ObjectMetaClass):
  """Meta class of meta.testing.Error."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(ErrorMetaClass, cls).__init__(meta__dct, meta__bases, meta__name)
    # User-provided code follows.
