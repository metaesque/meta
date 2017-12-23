import metax.test  # target=//metax/test:test
import random
##########  End Imports  ##########


class TestCase(metax.test.TestCase):

  # field TestVar : int

  def TestVar(self):
    """here"""
    return self._TestVar

  def TestVarIs(self, value):
    """here

    Args:
      value: int
    """
    self._TestVar = value

  def TestVarRef(self):
    """here"""
    return self._TestVar

  def __init__(self, meta__name=""):
    """here

    Args:
      meta__name: &str
    """
    super(TestCase, self).__init__(meta__name)
    self._TestVar = 0
    # User-provided code follows.

  def setUp(self):
    """here"""
    super(TestCase, self).setUp()
    # User-provided code follows.
    random.seed(0)
