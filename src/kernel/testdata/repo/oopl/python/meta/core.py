# -*- coding: utf-8 -*-
"""# Important classes relied on everywhere."""
import sys

import meta.root


class LoggerMetaClass(meta.root.ObjectMetaClass):
  """Meta class of meta.core.Logger."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(LoggerMetaClass, cls).__init__(meta__dct, meta__bases, meta__name)
    # User-provided code follows.


class Logger(meta.root.Object):
  """# Indent-based logging support."""
  __metaclass__ = LoggerMetaClass

  # field _fp : *meta.io.OStream
  #   Where to write logging output.

  def fp(self):
    """Returns: meta.io.OStream"""
    return self._fp

  def fpIs(self, value):
    """Setter for field fp

    Args:
      value: meta.io.OStream

    Returns: meta.core.Logger
    """
    self._fp = value
    return self

  # field _level : int
  # Current indentation level

  def level(self):
    """Returns: int"""
    return self._level

  def levelIs(self, value):
    """Setter for field level

    Args:
      value: int

    Returns: meta.core.Logger
    """
    self._level = value
    return self

  def __init__(self, fp=sys.stdout):
    """Initializer.

    Args:
      fp: file
    """
    super(Logger, self).__init__()
    self._level = 0
    # User-provided code follows.
    self._fp = fp

  def info(self, msg, *args):
    """# Write a message to the log.

    Args:
      msg: str
        # The message template to write (printf syntax allowed)
      args: list
        # Values to be interpolated into msg.
    """
    if msg[-1] != '\n':
      msg += '\n'
    self._fp.write('  ' * self._level)
    self._fp.write(msg % args)

  def uninfo(self, msg, *args):
    """# Write a message to stdout if this log does not write there.

    Args:
      msg: str
        # The message template to write (printf syntax allowed)
      args: list
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

  def metaSummary(self, indent=''):
    """Auto-generated one-line summary of the object.

    Args:
      indent: str
        Indentation to insert before each line.

    Returns: str
    """
    return 'meta.core.Logger %s' % id(self)

  def metaStream(self, fp=sys.stdout, indent='', depth=1):
    """Auto-generated human-readable description of the object.

    Args:
      fp: file
        Where to write the output.
      indent: str
        Indentation to insert before each line.
      depth: int
        How many levels to recurse.
    """
    subindent = indent + '  '

    # instance field fp : *meta.io.OStream
    f_fp = self.fp()
    fp.write(indent + 'fp : *meta.io.OStream = ' + str(((f_fp.metaSummary()) if f_fp else "null")) + '\n')
    if (depth > 0) and f_fp:
      f_fp.metaStream(fp=fp, indent=subindent, depth=depth-1)

    # instance field level : int
    fp.write(indent + 'level : int = ' + str(self.level()) + '\n')

# The singleton instance of the metaclass.
LoggerClass = Logger


class Meta__Logger(meta.root.Meta__Object):
  """Meta class of meta.core.Logger."""
  pass

# The singleton instance of the metaclass.
MetaLogger = Meta__Logger()
