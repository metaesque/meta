import metax.test  # target=//metax/test:test
import metax.test  # target=//metax/test:test
import metax.test_test  # target=//metax/test_test:test_test
##########  End Imports  ##########


class FakeFcntlTest(metax.test.TestCase):
  """Auto-generated test class for metax.test.FakeFcntl"""
  __metaclass__ = FakeFcntlTestMeta

  def test___init__(self):
    """here"""
    pass

  def test_fcntl(self):
    """here"""
    # noop
    # TODO(wmh): Is there a way to verify this method does nothing?
    pass

  def test_ioctl(self):
    """here"""
    # noop
    # TODO(wmh): Is there a way to verify this method does nothing?
    pass

  def test_flock(self):
    """here"""
    # noop
    # TODO(wmh): Is there a way to verify this method does nothing?
    pass

  def test_lockf(self):
    """here"""
    # noop
    # TODO(wmh): Is there a way to verify this method does nothing?
    pass

  def test_meta(self):
    """here"""
    # noop
    pass
########## Start Harness ##########


if __name__ == '__main__':
  metax.test.main()
