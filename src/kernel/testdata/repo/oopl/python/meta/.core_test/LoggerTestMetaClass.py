# Imports for class LoggerTestMetaClass
import sys                                # core 

import meta.testing                       # target 
# End imports for class LoggerTestMetaClass


class LoggerTestMetaClass(meta.testing.TestCaseMetaClass):
  """Meta class of meta.core_test.LoggerTest."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(LoggerTestMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.
