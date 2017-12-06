# Imports for class B
import meta.ex.coverage
import meta.root
# End imports for class B

postA = 'A'
preB = 'B'


class B(A):
  """A class inheriting from class A."""

  def func2(self, obj, num=10):
    """no docstr

    Args:
      obj: *A
        A required argument.
      num: int
        A simple parameter with a default value.

    Returns: int
    """
    return num * obj.num()
