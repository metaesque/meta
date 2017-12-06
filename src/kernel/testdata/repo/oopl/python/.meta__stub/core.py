"""# Important classes relied on everywhere."""
import sys

import meta.core
import meta.root


class Logger(meta.root.Object):
  """# Indent-based logging support."""

  # instance field _fp : *meta.io.OStream
  #   Where to write logging output.
  def fp(self): return self._fp
  def fpIs(self, value): self._fp = value; return self
  def fpRef(self): return self._fp

  # instance field _level : int
  # Current indentation level
  def level(self): return self._level
  def levelIs(self, value): self._level = value; return self
  def levelRef(self): return self._level

  def __init__(self, fp=sys.stdout):
    """Initializer.

    Args:
      fp: *meta.io.OStream
    """
    super(Logger, self).__init__()
    self.levelIs(0)
    # User-provided code follows.
    self._fp = fp

  def info(self, msg, *args):
    """# Write a message to the log.

    Args:
      msg: *str
        # The message template to write (printf syntax allowed)
      args: *list of *str
        # Values to be interpolated into msg.
    """
    if msg[-1] != '\n':
      msg += '\n'
    self._fp.write('  ' * self._level)
    self._fp.write(msg % args)

  def uninfo(self, msg, *args):
    """# Write a message to stdout if this log does not write there.

    Args:
      msg: *str
        # The message template to write (printf syntax allowed)
      args: *list of *str
        # Values to be interpolated into msg.
    """
    if self._fp is not sys.stdout:
      print msg % args

  def indent(self):
    """# Incremental level by one."""
    self._level += 1

  def undent(self):
    """# Decrement level by one."""
    self._level -= 1


class Meta__Logger(meta.root.Object):
  """Meta class of Logger."""
  pass
