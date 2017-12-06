import demo.cards2  # target=//demo/cards2:cards2
import demo.cards2_test  # target=//demo/cards2_test:cards2_test
import meta.testing  # target=//meta/testing:testing
##########  End Imports  ##########


class FrenchDeckTest(meta.testing.TestCase):
  """Auto-generated test class for demo.cards2.FrenchDeck"""
  __metaclass__ = FrenchDeckTest__Meta

  def __init__(test, meta__name):
    super(FrenchDeckTest, test).__init__(meta__name)
    # User-provided code follows.

  def test___init__(test):
    pass

  def test_asStr(test):
    deck = demo.cards2.FrenchDeck()
    test.iseq('DKDK', deck.asStr(deck.cards()[0]))
    test.iseq('7C', deck.asStr(deck.cards()[17]))
########## Start Harness ##########


if __name__ == '__main__':
  meta.testing.main()
