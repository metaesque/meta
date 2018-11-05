# -*- coding: utf-8 -*-
"""An intentionally broken codebase."""
try:
  import demo.err
except ImportError:
  pass
if not getattr(demo, 'err', None):
  import sys
  demo.err = sys.modules[__name__]
import metax.root
import sys


class AMeta(metax.root.ObjectMeta):
  """Auto-generated meta class for demo.err.A."""

  def __init__(cls, name, bases, symbols):
    """No comment provided.

    Args:
      name: &str
      bases: &#vec<class>
      symbols: &#map
    """
    super(AMeta, cls).__init__(name, bases, symbols)
    # User-provided code follows.


class A(metax.root.Object):
  """Undocumented."""
  __metaclass__ = AMeta

  def __init__(self):
    super(A, self).__init__()
    # User-provided code follows.

  def f(self):
    self.g()

  def g(self):
    self.h()

  def h(self):
    raise Exception()

  def meta(self):
    result = self.__class__
    assert issubclass(result, A)
    assert issubclass(result, MetaA)
    return result

  def printMeta(self, fp=sys.stdout, indent=''):
    """Auto-generated human-readable summary of this object.

    Args:
      fp: ostream
      indent: str
    """
    subindent = indent + "  "
    fp.write('A %x:\n' % id(self))

MetaA = A

# Class initialization methods
