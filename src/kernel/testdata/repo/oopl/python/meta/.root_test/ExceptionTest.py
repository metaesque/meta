# Imports for class ExceptionTest
import sys                                # core 

import meta.root                          # target meta: 411
import meta.testing                       # target meta: 411
import meta.testing                       # target 
# End imports for class ExceptionTest


class ExceptionTest(meta.testing.TestCase):
  """Unit tests for class Exception."""
  __metaclass__ = ExceptionTestMetaClass

  def __init__(self, meta__name):
    """Initializer.

    Args:
      meta__name: str
    """
    super(ExceptionTest, self).__init__(meta__name)
    # User-provided code follows.
