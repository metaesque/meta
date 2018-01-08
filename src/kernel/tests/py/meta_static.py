# Explore meta fields vs static fields.

def InitVar(msg, val):
  print 'HERE in InitVar with %s and %s' % (msg, val)
  return val


class AMeta(type):

  def __init__(cls, name, bases, symbols):
    print 'In AMeta init'
    super(AMeta, cls).__init__(name, bases, symbols)
    cls.MetaVar1 = 1
    cls.MetaVar2 = 2
    cls.VarA4 = 'AMeta'


class A(object):
  __metaclass__ = AMeta

  VarA = 6
  VarA2 = InitVar('A.VarA2', 16)
  VarA4 = 'A'

  def __init__(self, a=1):
    self._a = a

  @classmethod
  def Initialize(cls):
    cls.VarA3 = InitVar('A.VarB3 via Initialize', 108)

A.Initialize()


class BMeta(AMeta):

  def __init__(cls, name, bases, symbols):
    print 'In BMeta init'
    super(BMeta, cls).__init__(name, bases, symbols)
    cls.MetaVar2 = 20
    cls.MetaVar3 = 'hello'


class B(A):

  __metaclass__ = BMeta

  VarB = 8
  VarA4 = 'B'

  def __init__(self, a=1, b=17):
    super(B, self).__init__(a=a)
    self._b = b

  @classmethod
  def Initialize(cls):
    cls.VarB2 = InitVar('B.VarB2 via Initialize', 93)

B.Initialize()


def main():
  # The output will be:
  #   |HERE in InitVar with A.VarA2 and 16
  #   |In AMeta init
  #   |HERE in InitVar with A.VarB3 via Initialize and 108
  #   |In BMeta init
  #   |In AMeta init
  #   | HERE in InitVar with B.VarB2 via Initialize and 93
  #
  # The first 'HERE in InitVar' line demonstrates that "class" variables defined
  # within a class are not implicitly inserted into the metaclass initializer;
  # if they were, we would have seen two such lines printed, one when A was created and
  # one when B was created.
  #
  # The first 'In AMeta init' occurs when AMeta is initialized.
  # The 'In BMeta init' and 'In AMeta init' lines occur
  # when BMeta is initialized ... BMeta invokes super on AMeta after
  # printing out the 'In BMeta init' line).
  #
  # The 'HERE in InitVar with A.VarB3 via Initialize and 108' line
  # occurs when A.Initialize() is invoked.
  #
  # The 'HERE in InitVar with B.VarB2 via Initialize and 93' line
  # occurs when B.Initialize() is invoked.
  
  a = A()
  b = B()

  assert A.MetaVar1 == 1
  assert A.MetaVar2 == 2
  assert A.VarA == 6
  assert B.MetaVar1 == 1  # inherits from AMeta
  assert B.MetaVar2 == 20
  assert B.MetaVar3 == 'hello'
  assert B.VarB == 8
  assert B.VarA == 6   # inherits from AMeta (so not really static!)
  assert b.VarA == 6   # visible from class or instance
  assert b.MetaVar1 == 1  # meta fields are also visible from class or instance

  assert a._a == 1
  assert b._a == 1
  assert b._b == 17

  # Changing a meta-var in A does not affect the same metavar in B.
  A.MetaVar1 = 81
  assert B.MetaVar1 == 1

  # Changing a meta-var in B does not affect the same var in A.
  B.MetaVar1 = 2
  assert A.MetaVar1 == 81

  # Changing a class-level var in B does not affect the same var in A.
  #  - which means class-level vars are definitely not like static fields
  assert A.VarA == 6
  assert B.VarA == 6
  B.VarA = 66
  assert A.VarA == 6
  assert B.VarA == 66

  # If a variable is defined both as a class variable with Foo,
  # and as an instance variable within FooMeta, the definition
  # in FooMeta trumps the definitions in Foo, presumably because
  # the initialization of the metaclass happens after the
  # class variable initialization (TODO(wmh): Verify this).
  assert A.VarA4 == 'AMeta'
  assert B.VarA4 == 'AMeta'
  assert a.VarA4 == 'AMeta'
  assert b.VarA4 == 'AMeta'
  

if __name__ == '__main__':
  main()
