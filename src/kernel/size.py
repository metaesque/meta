import sys

class A(object):
  def __init__(self):
    object.__init__(self)
    self._a = 1

class B(A):
  def __init__(self):
    A.__init__(self)
    self._b = 2

class C(B):
  def __init__(self):
    B.__init__(self)
    self._c = 3

class As(object):
  __slots__ = ['_a']
  def __init__(self):
    object.__init__(self)
    self._a = 1

class Bs(As):
  __slots__ = ['_b']
  def __init__(self):
    A.__init__(self)
    self._b = 2

class Cs(Bs):
  __slots__ = ['_c']
  def __init__(self):
    B.__init__(self)
    self._c = 3

import sys
from numbers import Number
from collections import deque
from collections.abc import Set, Mapping

ZERO_DEPTH_BASES = (str, bytes, Number, range, bytearray)

def getsize(obj_0):
  """Recursively iterate to sum size of object & members."""
  _seen_ids = set()
  def inner(obj):
    obj_id = id(obj)
    if obj_id in _seen_ids:
      return 0
    _seen_ids.add(obj_id)
    size = sys.getsizeof(obj)
    if isinstance(obj, ZERO_DEPTH_BASES):
      pass # bypass remaining control flow and return
    elif isinstance(obj, (tuple, list, Set, deque)):
      size += sum(inner(i) for i in obj)
    elif isinstance(obj, Mapping) or hasattr(obj, 'items'):
      size += sum(inner(k) + inner(v) for k, v in getattr(obj, 'items')())
    # Check for custom object instances - may subclass above too
    if hasattr(obj, '__dict__'):
      size += inner(vars(obj))
    if hasattr(obj, '__slots__'): # can have __slots__ with __dict__
      size += sum(inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s))
    return size
  return inner(obj_0)

for cls in (A, B, C, As, Bs, Cs):
  obj = cls()
  print('%-2s = %d' % (cls.__name__, getsize(obj)))
