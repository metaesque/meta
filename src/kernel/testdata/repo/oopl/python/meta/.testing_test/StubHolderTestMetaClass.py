# Imports for class StubHolderTestMetaClass
import sys                                # core 

import meta.testing_test                  # target 
# End imports for class StubHolderTestMetaClass


class StubHolderTestMetaClass(TestCaseMetaClass):
  """Meta class of meta.testing_test.StubHolderTest."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(StubHolderTestMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.
