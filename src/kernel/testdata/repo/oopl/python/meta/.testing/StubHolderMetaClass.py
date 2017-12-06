# Imports for class StubHolderMetaClass
import sys                                # core 
# End imports for class StubHolderMetaClass


class StubHolderMetaClass(meta.root.ObjectMetaClass):
  """Meta class of meta.testing.StubHolder."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(StubHolderMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.
