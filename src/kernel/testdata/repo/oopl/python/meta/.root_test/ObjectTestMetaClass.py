# Imports for class ObjectTestMetaClass
import sys                                # core 

import meta.testing                       # target 
# End imports for class ObjectTestMetaClass


class ObjectTestMetaClass(meta.testing.TestCaseMetaClass):
  """Meta class of meta.root_test.ObjectTest."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(ObjectTestMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.
