"""Playing cards.

Terminology: https://en.wikipedia.org/wiki/Glossary_of_card_game_terms

  pack:
    A complete set of cards. A double pack may be used (i.e. 104/108 instead
    of 52/54).
  pile:
    A set of cards placed on a surface so that they partially or completely
    overlap.
  stack:
    Cards are placed directly on top of each other, disallowing the player to
    see any card other than the top. In most cases, these cards are and should
    be kept hidden. Viewing these cards during a deal is often considered
    illegal, so they should be dealt face down.
  stock:
    A pile of cards, face down, which are left over after setting up the rest
    of the game (i.e. dealing hands, setting up other layout areas).
  kitty:
    Additional cards dealt face down in some card games.
  deck:
    May refer to either pack or stock and is thus ambigous. However, it is
    more common to refer to a deck of cards than a pack of cards, and since
    there is already a word for stock, we choose to define deck to mean
    pack in this code, and name classes representing complete sets of cards
    using Deck rather than Pack.

  rank: (aka kind)
    The position of a card relative to others in the same suit. The order of
    the ranks depends on the game being played.
  suit:
    All cards that share the same pips
  pip:
    A suit symbol (e.g. spades, hearts, diamonds, clubs) on a card."""
import demo.cards2
import meta.root
import random


class Card__Meta(meta.root.ObjectMetaClass):
  """Auto-generated meta class for Card"""

  def __init__(meta, meta__name, meta__bases, meta__dict):
    super(Card__Meta, meta).__init__(meta__name, meta__bases, meta__dict)
    # User-provided code follows.


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


class Pile__Meta(meta.root.ObjectMetaClass):
  """Auto-generated meta class for Pile"""

  def __init__(meta, meta__name, meta__bases, meta__dict):
    super(Pile__Meta, meta).__init__(meta__name, meta__bases, meta__dict)
    # User-provided code follows.


class Pile(meta.root.Object):
  """A set of cards that partially or completely overlap."""
  __metaclass__ = Pile__Meta

  def __init__(self):
    super(Pile, self).__init__()
    self._cards = []
    # User-provided code follows.

  def cards(self):
    return self._cards

  def cardsIs(self, value):
    self._cards = value
    return self

  def cardsRef(self):
    return self._cards


class Deck__Meta(Pile__Meta):
  """Auto-generated meta class for Deck"""

  def __init__(meta, meta__name, meta__bases, meta__dict):
    super(Deck__Meta, meta).__init__(meta__name, meta__bases, meta__dict)
    # User-provided code follows.


class Deck(Pile):
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


class FrenchDeck__Meta(Deck__Meta):
  """Auto-generated meta class for FrenchDeck"""

  def Suits(meta):
    return meta._Suits

  def SuitsIs(meta, value):
    meta._Suits = value
    return meta

  def SuitsRef(meta):
    return meta._Suits

  def Ranks(meta):
    return meta._Ranks

  def RanksIs(meta, value):
    meta._Ranks = value
    return meta

  def RanksRef(meta):
    return meta._Ranks

  def __init__(meta, meta__name, meta__bases, meta__dict):
    super(FrenchDeck__Meta, meta).__init__(meta__name, meta__bases, meta__dict)
    # User-provided code follows.
    meta.SuitsIs(
      ['Joker', 'Spades', 'Diamonds', 'Clubs', 'Hearts'])
    meta.RanksIs([
      'Low',
      'Ace', '2', '3', '4', '5', '6', '7', '8', '9',
      'Ten', 'Jack', 'Queen', 'King',
      'High'])


class FrenchDeck(Deck):
  """https://en.wikipedia.org/wiki/French_playing_cards"""
  __metaclass__ = FrenchDeck__Meta

  def __init__(self, jokers=False):
    super(FrenchDeck, self).__init__()
    # User-provided code follows.
    cards = self.cards()
    for suit in range(1, 5):
      for rank in range(1, 14):
        card = Card(self, rank, suit)
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
