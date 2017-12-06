# Imports for class ExceptionTestMetaClass
import sys                                # core 

import meta.testing                       # target 
# End imports for class ExceptionTestMetaClass


class ExceptionTestMetaClass(meta.testing.TestCaseMetaClass):
  """Meta class of meta.root_test.ExceptionTest."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(ExceptionTestMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.
