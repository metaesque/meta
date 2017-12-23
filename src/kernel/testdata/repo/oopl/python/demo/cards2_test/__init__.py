"""Auto-generated test namespace for demo.cards2."""
import demo.cards2
import demo.cards2_test
import metax.test
import random


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


class CardTestMeta(metax.test.TestCaseMeta):
  """Auto-generated meta class for auto-generated test class CardTest"""


class CardTest(TestCase):
  """Auto-generated test class for demo.cards2.Card"""
  __metaclass__ = CardTestMeta

  def test___init__(self):
    """here"""
    pass

  def test_meta(self):
    """here"""
    # noop
    pass


class CardMetaTest(TestCase):
  """Auto-generated test class for auto-generated meta class demo.cards2.CardMeta."""


class PileTestMeta(metax.test.TestCaseMeta):
  """Auto-generated meta class for auto-generated test class PileTest"""


class PileTest(TestCase):
  """Auto-generated test class for demo.cards2.Pile"""
  __metaclass__ = PileTestMeta

  def test_meta(self):
    """here"""
    # noop
    pass


class PileMetaTest(TestCase):
  """Auto-generated test class for auto-generated meta class demo.cards2.PileMeta."""


class DeckTestMeta(metax.test.TestCaseMeta):
  """Auto-generated meta class for auto-generated test class DeckTest"""


class DeckTest(TestCase):
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


class DeckMetaTest(TestCase):
  """Auto-generated test class for auto-generated meta class demo.cards2.DeckMeta."""


class FrenchDeckTestMeta(metax.test.TestCaseMeta):
  """Auto-generated meta class for auto-generated test class FrenchDeckTest"""


class FrenchDeckTest(TestCase):
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


class FrenchDeckMetaTest(TestCase):
  """Auto-generated test class for auto-generated meta class demo.cards2.FrenchDeckMeta."""

  def test___init__(self):
    """here"""
    pass


if __name__ == '__main__':  metax.test.main()
