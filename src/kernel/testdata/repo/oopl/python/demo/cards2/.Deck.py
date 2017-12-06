import demo.cards2  # target=//demo/cards2:cards2
import demo.cards2  # target=//demo/cards2:cards2
import random
##########  End Imports  ##########


class Deck(demo.cards2.Pile):
  """A pre-determined collection of Card instances."""
  __metaclass__ = Deck__Meta

  def __init__(self):
    super(Deck, self).__init__()
    # User-provided code follows.

  def asStr(self, card):
    """Provide a string representation of a given card."""
    pass

  def shuffle(self):
    """http://wikipedia.org/wiki/Fisher-Yates_shuffle"""
    cards = self.cards()
    n = len(cards)
    for i in range(0, n):
      # 0 <= j <= i
      j = random.randint(0, i)  
      tmp = cards[j]
      cards[j] = cards[i]
      cards[i] = tmp
