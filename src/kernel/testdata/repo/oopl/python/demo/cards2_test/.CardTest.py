import demo.cards2  # target=//demo/cards2:cards2
import demo.cards2_test  # target=//demo/cards2_test:cards2_test
import demo.cards2_test  # target=//demo/cards2_test:cards2_test
##########  End Imports  ##########


class CardTest(demo.cards2_test.TestCase):
  """Auto-generated test class for demo.cards2.Card"""
  __metaclass__ = CardTestMeta

  def test___init__(self):
    """here"""
    pass

  def test_meta(self):
    """here"""
    # noop
    pass
########## Start Harness ##########


if __name__ == '__main__':
  metax.test.main()
