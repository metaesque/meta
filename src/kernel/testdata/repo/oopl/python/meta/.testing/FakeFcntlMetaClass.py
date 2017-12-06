# Imports for class FakeFcntlMetaClass
import sys                                # core 
# End imports for class FakeFcntlMetaClass

TestCase.Initialize()


class FakeFcntlMetaClass(meta.root.ObjectMetaClass):
  """Meta class of meta.testing.FakeFcntl."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(FakeFcntlMetaClass, cls).__init__(meta__dct, meta__bases, meta__name)
    # User-provided code follows.
