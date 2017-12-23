import demo.cards2  # target=//demo/cards2:cards2
import metax.root  # target=//metax/root:root
##########  End Imports  ##########


class Card(metax.root.Object):
  """A card with suit and rank.

  In this implementation, Card instances do not know about the Deck they
  belong to. See cards3.meta2 for a version in which Card maintains a Deck
  (this introduces a circularity, as Deck needs Card and Card needs Deck).
  """
  __metaclass__ = CardMeta

  # field rank : int
  #   Rank as simple integer. Deck assigns display semantics to rank values.

  def rank(self):
    """here"""
    return self._rank

  def rankIs(self, value):
    """here

    Args:
      value: int
    """
    self._rank = value

  def rankRef(self):
    """here"""
    return self._rank

  # field suit : int
  #   Suit as simple integer. Deck assigns display semantics to suit values.

  def suit(self):
    """here"""
    return self._suit

  def suitIs(self, value):
    """here

    Args:
      value: int
    """
    self._suit = value

  def suitRef(self):
    """here"""
    return self._suit

  def __init__(self, rank, suit):
    """here
    It should not be necessary to create Card instances directly.
    Instead, one should create instances of Deck, and use the cards
    it contains.

    Args:
      rank: int
      suit: int
    """
    super(Card, self).__init__()
    # User-provided code follows.
    self.rankIs(rank)
    self.suitIs(suit)

  def meta(self):
    """here"""
    result = self.__class__
    assert result is Card
    assert result is MetaCard
    return result

MetaCard = Card
