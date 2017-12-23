import demo.cards2  # target=//demo/cards2:cards2
import demo.cards2  # target=//demo/cards2:cards2
import metax.root  # target=//metax/root:root
##########  End Imports  ##########


class Pile(metax.root.Object):
  """A set of cards that partially or completely overlap."""
  __metaclass__ = PileMeta

  def __init__(self):
    """here"""
    super(Pile, self).__init__()
    self._cards = []
    # User-provided code follows.

  # field cards : @vec<Card>
  #   The Card instances in this Pile

  def cards(self):
    """here"""
    return self._cards

  def cardsIs(self, value):
    """here

    Args:
      value: @vec<Card>
    """
    self._cards = value

  def cardsRef(self):
    """here"""
    return self._cards

  def meta(self):
    """here"""
    result = self.__class__
    assert result is Pile
    assert result is MetaPile
    return result

MetaPile = Pile
