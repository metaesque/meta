"""Auto-generated test namespace for demo.cards2"""
import demo.cards2
import demo.cards2_test
import meta.testing


class CardTest__Meta(meta.testing.TestCaseMetaClass):
  """Auto-generated meta class for auto-generated test class CardTest"""

  def __init__(meta, meta__name, meta__bases, meta__dict):
    super(CardTest__Meta, meta).__init__(meta__name, meta__bases, meta__dict)
    # User-provided code follows.


class CardTest(meta.testing.TestCase):
  """Auto-generated test class for demo.cards2.Card"""
  __metaclass__ = CardTest__Meta

  def __init__(test, meta__name):
    super(CardTest, test).__init__(meta__name)
    # User-provided code follows.

  def test___init__(test):
    pass


class Card__MetaTest(meta.testing.TestCase):
  """Auto-generated test class for auto-generated meta class demo.cards2.Card__Meta"""

  def __init__(test, meta__name):
    super(Card__MetaTest, test).__init__(meta__name)
    # User-provided code follows.


class PileTest__Meta(meta.testing.TestCaseMetaClass):
  """Auto-generated meta class for auto-generated test class PileTest"""

  def __init__(meta, meta__name, meta__bases, meta__dict):
    super(PileTest__Meta, meta).__init__(meta__name, meta__bases, meta__dict)
    # User-provided code follows.


class PileTest(meta.testing.TestCase):
  """Auto-generated test class for demo.cards2.Pile"""
  __metaclass__ = PileTest__Meta

  def __init__(test, meta__name):
    super(PileTest, test).__init__(meta__name)
    # User-provided code follows.


class Pile__MetaTest(meta.testing.TestCase):
  """Auto-generated test class for auto-generated meta class demo.cards2.Pile__Meta"""

  def __init__(test, meta__name):
    super(Pile__MetaTest, test).__init__(meta__name)
    # User-provided code follows.


class DeckTest__Meta(meta.testing.TestCaseMetaClass):
  """Auto-generated meta class for auto-generated test class DeckTest"""

  def __init__(meta, meta__name, meta__bases, meta__dict):
    super(DeckTest__Meta, meta).__init__(meta__name, meta__bases, meta__dict)
    # User-provided code follows.


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


class Deck__MetaTest(meta.testing.TestCase):
  """Auto-generated test class for auto-generated meta class demo.cards2.Deck__Meta"""

  def __init__(test, meta__name):
    super(Deck__MetaTest, test).__init__(meta__name)
    # User-provided code follows.


class FrenchDeckTest__Meta(meta.testing.TestCaseMetaClass):
  """Auto-generated meta class for auto-generated test class FrenchDeckTest"""

  def __init__(meta, meta__name, meta__bases, meta__dict):
    super(FrenchDeckTest__Meta, meta).__init__(meta__name, meta__bases, meta__dict)
    # User-provided code follows.


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


class FrenchDeck__MetaTest(meta.testing.TestCase):
  """Auto-generated test class for auto-generated meta class demo.cards2.FrenchDeck__Meta"""

  def __init__(test, meta__name):
    super(FrenchDeck__MetaTest, test).__init__(meta__name)
    # User-provided code follows.

  def test___init__(test):
    pass


if __name__ == '__main__':
  meta.testing.main()
