# Imports for class FakeFcntlTest
import sys                                # core 

import meta.testing                       # target meta: -2
import meta.testing                       # target meta: -2
import meta.testing_test                  # target 
# End imports for class FakeFcntlTest


class FakeFcntlTest(TestCase):
  """Unit tests for class FakeFcntl."""
  __metaclass__ = FakeFcntlTestMetaClass

  def __init__(self, meta__name):
    """Initializer.

    Args:
      meta__name: str
    """
    super(FakeFcntlTest, self).__init__(meta__name)
    # User-provided code follows.

  def test_FakeFcntl(self):
    pass

  def test_fcntl(self):
    # noop
    # TODO(wmh): Is there a way to verify this method does nothing?
    pass

  def test_ioctl(self):
    # noop
    # TODO(wmh): Is there a way to verify this method does nothing?
    pass

  def test_flock(self):
    # noop
    # TODO(wmh): Is there a way to verify this method does nothing?
    pass

  def test_lockf(self):
    # noop
    # TODO(wmh): Is there a way to verify this method does nothing?
    pass
