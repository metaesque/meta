# Imports for class StubHolderTest
import sys                                # core 

import meta.testing                       # target meta: -2
import meta.testing                       # target meta: -2
import meta.testing_test                  # target 
# End imports for class StubHolderTest


class StubHolderTest(TestCase):
  """Unit tests for class StubHolder."""
  __metaclass__ = StubHolderTestMetaClass

  def __init__(self, meta__name):
    """Initializer.

    Args:
      meta__name: str
    """
    super(StubHolderTest, self).__init__(meta__name)
    # User-provided code follows.

  def test_Meta__9_id(self):
    pass

  def test___del__(self):
    pass

  def test___enter__(self):
    pass

  def test___exit__(self):
    pass

  def test_CleanUp(self):
    pass

  def test_SmartSet(self):
    pass

  def test_SmartUnsetAll(self):
    pass

  def test_Set(self):
    pass

  def test_UnsetAll(self):
    pass
