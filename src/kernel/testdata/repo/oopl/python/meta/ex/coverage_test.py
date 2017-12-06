import meta.ex.coverage
import meta.testing


class TestCase(meta.testing.TestCase):
  """no docstr"""
  pass


class TestA(meta.ex.coverage.A):
  """no docstr"""

  def f(self):
    """no docstr

    Returns: void
    """
    f = 1

pc = 10


class ATest(meta.testing.TestCase):
  pass


class BTest(meta.testing.TestCase):
  pass


if __name__ == '__main__':
  meta.testing.main()
