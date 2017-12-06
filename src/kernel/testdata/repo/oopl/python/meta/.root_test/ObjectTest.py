# Imports for class ObjectTest
import sys                                # core 

import meta.root                          # target meta: 19
import meta.testing                       # target meta: 19
import meta.testing                       # target 
# End imports for class ObjectTest


class ObjectTest(meta.testing.TestCase):
  """Unit tests for class Object."""
  __metaclass__ = ObjectTestMetaClass

  def __init__(self, meta__name):
    """Initializer.

    Args:
      meta__name: str
    """
    super(ObjectTest, self).__init__(meta__name)
    # User-provided code follows.
