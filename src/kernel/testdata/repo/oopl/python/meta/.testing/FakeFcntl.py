# Imports for class FakeFcntl
import sys                                # core 
# End imports for class FakeFcntl


class FakeFcntl(object):
  """A fake fcntl object."""
  __metaclass__ = FakeFcntlMetaClass

  LOCK_UN = fcntl.LOCK_UN
  LOCK_SH = fcntl.LOCK_SH
  LOCK_EX = fcntl.LOCK_EX

  # field _filesystem : any

  def filesystem(self):
    """Returns: any"""
    return self._filesystem

  def filesystemIs(self, value):
    """Setter for field filesystem

    Args:
      value: any

    Returns: meta.testing.FakeFcntl
    """
    self._filesystem = value
    return self

  def __init__(self, fs):
    """Initializer.

    Args:
      fs: any
    """
    super(FakeFcntl, self).__init__()
    # User-provided code follows.
    self._filesystem = fs

  def fcntl(self, fd, op, arg=0):
    """Args:
      fd: any
      op: any
      arg: any
    """
    pass

  def ioctl(self, fd, op, arg=0, mutate_flag=False):
    """Args:
      fd: any
      op: any
      arg: any
      mutate_flag: any
    """
    pass

  def flock(self, fd, op):
    """Args:
      fd: any
      op: any
    """
    pass

  def lockf(self, fd, op, length=0, start=0, whence=0):
    """Args:
      fd: any
      op: any
      length: any
      start: any
      whence: any
    """
    pass

# The singleton instance of the metaclass.
FakeFcntlClass = FakeFcntl
