import demo.cards2  # target=//demo/cards2:cards2
import demo.cards2_test  # target=//demo/cards2_test:cards2_test
import demo.cards2_test  # target=//demo/cards2_test:cards2_test
##########  End Imports  ##########


class DeckTest(demo.cards2_test.TestCase):
  """Auto-generated test class for demo.cards2.Deck"""
  __metaclass__ = DeckTestMeta

  def test_shuffle(self):
    """here"""
    import random
    random.seed(0)
    deck = demo.cards2.FrenchDeck()
    deck.shuffle()
    self.iseqvec(
      [deck.asStr(card) for card in deck.cards()[:10]],
      ['2H', '4S', 'KD', 'KS', '3D', 'TS', '8D', '6S', '8H', '2D'])

  def test_meta(self):
    """here"""
    # noop
    pass
########## Start Harness ##########


if __name__ == '__main__':
  metax.test.main()
