# Imports for class A
import meta.root
import meta.root
# End imports for class A

GLOBAL = 1
def Global ():
  print 'Hello World'


class A(meta.root.Object):
  """A class inheriting from the Meta Object class."""

  Hi = 'Hi'

  # instance field _count : @vec
  #   A field without accessors.
  @meta.root.protected
  def count(self): return self._count
  @meta.root.protected
  def countIs(self, value): self._count = value
  @meta.root.protected
  def countRef(self): return self._count

  # instance field _num : @int
  #   A simple read-only integer field.
  def num(self): return self._num
  @meta.root.protected
  def numIs(self, value): self._num = value
  @meta.root.protected
  def numRef(self): return self._num

  def g(self):
    """no docstr

    Returns: int
    """
    g = 1
    return g

  # instance field _name : &str
  #   A simple read-write string field.
  def name(self): return self._name
  def nameIs(self, value): self._name = value
  @meta.root.protected
  def nameRef(self): return self._name

  # instance field _next : *A
  #   Another instance of A, which is read-write-mutatable, and has specialized
  #   definitions for all three.
  def next(self): return self._next
  def nextIs(self, value): self._next = value
  def nextRef(self): return self._next

  # meta field _ClassIntVariable : @int
  #   A basic class variable not explicitly initialized. The user will
  #   presumably manually initialize it somewhere (e.g. an Initialize method,
  #   etc).
  _ClassIntVariable = 0
  @classmethod
  def ClassIntVariable(cls): return cls._ClassIntVariable
  @classmethod
  def ClassIntVariableIs(cls, value): cls._ClassIntVariable = value
  @classmethod
  def ClassIntVariableRef(cls): return cls._ClassIntVariable

  # meta field _ClassFloatVariable : @float
  #   A basic class variable that is explicitly initialized. If the base
  #   language does not provide explicit support for initializing such
  #   variables at the point of definition, Meta will generate appropriate
  #   code within an auto-generated class-initialization method and ensure
  #   it is invoked when the class is first defined.
  _ClassFloatVariable = 3.14
  @classmethod
  def ClassFloatVariable(cls): return cls._ClassFloatVariable
  @classmethod
  def ClassFloatVariableIs(cls, value): cls._ClassFloatVariable = value
  @classmethod
  def ClassFloatVariableRef(cls): return cls._ClassFloatVariable

  def __init__(self):
    """Initializer."""
    super(A, self).__init__()
    self.countIs([])
    self.numIs(0)
    self.nameIs('')
    self.nextIs(None)
    # User-provided code follows.
    self._num = 0
    self.nameIs('')
    self.count = {'get': 0, 'set': 0, 'ref': 0}
    self.nextIs(None)

  @classmethod
  def Initialize(cls):
    """no docstr"""
    cls._ClassIntVariable = 10

  def func(self, obj, num=3):
    """no docstr

    Args:
      obj: *A
        A required argument.
      num: int
        A simple parameter with a default value.

    Returns: int
    """
    return num * obj.num()

  def func2(self, obj, num=3):
    """no docstr

    Args:
      obj: *A
        A required argument.
      num: int
        A simple parameter with a default value.

    Returns: int
    """
    return num * obj.num()

  Bye = 'Bye'
