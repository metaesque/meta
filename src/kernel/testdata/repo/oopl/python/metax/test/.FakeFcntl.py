import fcntl
import metax.test  # target=//metax/test:test
##########  End Imports  ##########


class FakeFcntl(object):
  """A fake fcntl object."""
  __metaclass__ = FakeFcntlMeta

  # field filesystem : any

  def filesystem(self):
    """here"""
    return self._filesystem

  def filesystemIs(self, value):
    """here

    Args:
      value: any
    """
    self._filesystem = value

  def filesystemRef(self):
    """here"""
    return self._filesystem

  def __init__(self, fs):
    """here

    Args:
      fs: any
    """
    super(FakeFcntl, self).__init__()
    # User-provided code follows.
    self._filesystem = fs

  def fcntl(self, fd, op, arg=0):
    """here

    Args:
      fd: any
      op: any
      arg: any
    """
    pass

  def ioctl(self, fd, op, arg=0, mutate_flag=False):
    """here

    Args:
      fd: any
      op: any
      arg: any
      mutate_flag: any
    """
    pass

  def flock(self, fd, op):
    """here

    Args:
      fd: any
      op: any
    """
    pass

  def lockf(self, fd, op, length=0, start=0, whence=0):
    """here

    Args:
      fd: any
      op: any
      length: any
      start: any
      whence: any
    """
    pass

  def meta(self):
    """here"""
    result = self.__class__
    assert result is FakeFcntl
    assert result is MetaFakeFcntl
    return result

MetaFakeFcntl = FakeFcntl
