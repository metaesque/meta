import demo.cards2  # target=//demo/cards2:cards2
import demo.cards2  # target=//demo/cards2:cards2
import meta.root  # target=//meta/root:root
##########  End Imports  ##########


class Card(meta.root.Object):
  """A card with suit and rank, belonging to a Deck.

  The Deck is responsible for display functionality."""
  __metaclass__ = Card__Meta

  def rank(self):
    return self._rank

  def rankIs(self, value):
    self._rank = value
    return self

  def rankRef(self):
    return self._rank

  def suit(self):
    return self._suit

  def suitIs(self, value):
    self._suit = value
    return self

  def suitRef(self):
    return self._suit

  def deck(self):
    return self._deck

  def deckIs(self, value):
    self._deck = value
    return self

  def deckRef(self):
    return self._deck

  def __init__(self, deck, rank, suit):
    """It should not be necessary to create Card instances directly.
    Instead, one should create instances of Deck, and use the cards
    it contains."""
    super(Card, self).__init__()
    # User-provided code follows.
    self.deckIs(deck)
    self.rankIs(rank)
    self.suitIs(suit)
