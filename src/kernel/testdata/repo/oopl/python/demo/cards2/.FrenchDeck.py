import demo.cards2  # target=//demo/cards2:cards2
import demo.cards2  # target=//demo/cards2:cards2
import demo.cards2  # target=//demo/cards2:cards2
##########  End Imports  ##########


class FrenchDeck(demo.cards2.Deck):
  """https://en.wikipedia.org/wiki/French_playing_cards"""
  __metaclass__ = FrenchDeckMeta

  def __init__(self, jokers=False):
    """here

    Args:
      jokers: bool
        If true, the deck includes high and low joker.
    """
    super(FrenchDeck, self).__init__()
    # User-provided code follows.
    cards = self.cards()
    for suit in range(1, 5):
      for rank in range(1, 14):
        card = demo.cards2.Card(rank, suit)
        cards.append(card)
    if jokers:
      lowjoker = Card(0, 0)
      cards.append(lowjoker)
      highjoker = Card(14, 0)
      cards.append(highjoker)

  def asStr(self, card, full=False):
    """here
    Provide a string representation of a given card.

    Args:
      card: Card
      full: bool
        If true, result is '<rank> of <suit>'. If false,
        result is two letters.

    Returns:
      Testing to see how things work.
    """
    meta = self.__class__
    if full:
      result = meta.Ranks()[card.rank()] + ' of ' + meta.Suits()[card.suit()]
    else:
      result = meta.Ranks()[card.rank()][0] + meta.Suits()[card.suit()][0]
    return result

  def meta(self):
    """here"""
    result = self.__class__
    assert result is FrenchDeck
    assert result is MetaFrenchDeck
    return result

MetaFrenchDeck = FrenchDeck
