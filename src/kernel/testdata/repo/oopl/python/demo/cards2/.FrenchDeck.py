import demo.cards2  # target=//demo/cards2:cards2
import demo.cards2  # target=//demo/cards2:cards2
import demo.cards2  # target=//demo/cards2:cards2
##########  End Imports  ##########


class FrenchDeck(demo.cards2.Deck):
  """https://en.wikipedia.org/wiki/French_playing_cards"""
  __metaclass__ = FrenchDeck__Meta

  def __init__(self, jokers=False):
    super(FrenchDeck, self).__init__()
    # User-provided code follows.
    cards = self.cards()
    for suit in range(1, 5):
      for rank in range(1, 14):
        card = demo.cards2.Card(self, rank, suit)
        cards.append(card)
    if jokers:
      lowjoker = Card(self, 0, 0)
      cards.append(lowjoker)
      highjoker = Card(self, 14, 0)
      cards.append(highjoker)

  def asStr(self, card, full=False):
    """Provide a string representation of a given card."""
    meta = self.__class__
    if full:
      result = meta.Ranks()[card.rank()] + ' of ' + meta.Suits()[card.suit()]
    else:
      result = meta.Ranks()[card.rank()][0] + meta.Suits()[card.suit()][0]
    return result
