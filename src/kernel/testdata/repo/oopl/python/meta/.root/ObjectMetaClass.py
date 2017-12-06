# Imports for class ObjectMetaClass
import sys                                # core 
# End imports for class ObjectMetaClass


class ObjectMetaClass(type):
  """Meta class of meta.root.Object."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(ObjectMetaClass, cls).__init__(meta__dct, meta__bases, meta__name)
    # User-provided code follows.
