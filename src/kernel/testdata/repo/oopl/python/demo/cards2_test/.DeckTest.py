import demo.cards2  # target=//demo/cards2:cards2
import demo.cards2_test  # target=//demo/cards2_test:cards2_test
import meta.testing  # target=//meta/testing:testing
##########  End Imports  ##########


class DeckTest(meta.testing.TestCase):
  """Auto-generated test class for demo.cards2.Deck"""
  __metaclass__ = DeckTest__Meta

  def __init__(test, meta__name):
    super(DeckTest, test).__init__(meta__name)
    # User-provided code follows.

  def test_shuffle(test):
    import random
    random.seed(0)
    deck = demo.cards2.FrenchDeck()
    deck.shuffle()
    test.iseqvec(
      [deck.asStr(card) for card in deck.cards()[:10]],
      ['JS', 'AD', '7H', '4S', '4D', '3H', '6S', '2H', 'QC', '4C'])
########## Start Harness ##########


if __name__ == '__main__':
  meta.testing.main()
