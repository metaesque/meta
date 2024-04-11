import unittest

# The following are useful when debugging the 'imports' attribute of
# py_test to see how values specified therein affect sys.path
#   import sys
#   import pprint
#   pprint.pprint(sys.path)

import wmh.ex

# TODO(wmh): Introduce metax.test.TestCase
class RectangleTest(unittest.TestCase):

  def __init__(self, meta__name=""):
    super(RectangleTest, self).__init__()
    self._rect1 = wmh.ex.Rectangle(5,7)

  def rect1(): return self._rect1

  def test_draw():
      self.assertTrue(35, self.rect1().area())
