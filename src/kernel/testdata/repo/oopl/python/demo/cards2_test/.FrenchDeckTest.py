import demo.cards2  # target=//demo/cards2:cards2
import demo.cards2_test  # target=//demo/cards2_test:cards2_test
import demo.cards2_test  # target=//demo/cards2_test:cards2_test
##########  End Imports  ##########


class FrenchDeckTest(demo.cards2_test.TestCase):
  """Auto-generated test class for demo.cards2.FrenchDeck"""
  __metaclass__ = FrenchDeckTestMeta

  def test___init__(self):
    """here"""
    pass

  def test_asStr(self):
    """here"""
    deck = demo.cards2.FrenchDeck()
    self.iseq('AS', deck.asStr(deck.cards()[0]))
    self.iseq('5D', deck.asStr(deck.cards()[17]))

  def test_meta(self):
    """here"""
    # noop
    pass
########## Start Harness ##########


if __name__ == '__main__':
  metax.test.main()
