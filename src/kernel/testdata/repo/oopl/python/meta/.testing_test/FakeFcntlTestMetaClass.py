# Imports for class FakeFcntlTestMetaClass
import sys                                # core 

import meta.testing_test                  # target 
# End imports for class FakeFcntlTestMetaClass


class FakeFcntlTestMetaClass(TestCaseMetaClass):
  """Meta class of meta.testing_test.FakeFcntlTest."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(FakeFcntlTestMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.
