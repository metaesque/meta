import demo.cards2  # target=//demo/cards2:cards2
import demo.cards2  # target=//demo/cards2:cards2
import random
##########  End Imports  ##########


class Deck(demo.cards2.Pile):
  """A pre-determined collection of Card instances."""
  __metaclass__ = DeckMeta

  def asStr(self, card, full=False):
    """here
    Provide a string representation of a given card.

    Args:
      card: Card
      full: bool
        If true, result is '<rank> of <suit>'. If false,
        result is two letters.
    """
    raise NotImplementedError('demo.cards2.Deck.asStr');
    return ''

  def shuffle(self):
    """here
    http://wikipedia.org/wiki/Fisher-Yates_shuffle
    """
    cards = self.cards()
    n = len(cards)
    for i in range(0, n):
      # 0 <= j <= i
      j = random.randint(0, i)  
      tmp = cards[j]
      cards[j] = cards[i]
      cards[i] = tmp

  def meta(self):
    """here"""
    result = self.__class__
    assert result is Deck
    assert result is MetaDeck
    return result

MetaDeck = Deck
