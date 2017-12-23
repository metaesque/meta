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
    A suit symbol (e.g. spades, hearts, diamonds, clubs) on a card.
"""
import demo.cards2
import metax.root
import random


class CardMeta(metax.root.ObjectMeta):
  """Auto-generated meta class for Card."""


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


class PileMeta(metax.root.ObjectMeta):
  """Auto-generated meta class for Pile."""


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


class DeckMeta(PileMeta):
  """Auto-generated meta class for Deck."""


class Deck(Pile):
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
    raise NotImplementedError('Deck.asStr');
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


class FrenchDeckMeta(DeckMeta):
  """Auto-generated meta class for FrenchDeck."""

  # field Suits : @vec<@str>
  #   Indices are suit integers, values are suit names.

  def Suits(cls):
    """here"""
    return cls._Suits

  def SuitsIs(cls, value):
    """here

    Args:
      value: @vec<@str>
    """
    cls._Suits = value

  def SuitsRef(cls):
    """here"""
    return cls._Suits

  # field Ranks : @vec<@str>
  #   Indices are suit integers, values are suit names.

  def Ranks(cls):
    """here"""
    return cls._Ranks

  def RanksIs(cls, value):
    """here

    Args:
      value: @vec<@str>
    """
    cls._Ranks = value

  def RanksRef(cls):
    """here"""
    return cls._Ranks

  def __init__(cls, name, bases, symbols):
    """here

    Args:
      name: &str
      bases: &vec<class>
      symbols: &map
    """
    super(FrenchDeckMeta, cls).__init__(name, bases, symbols)
    # User-provided code follows.
    cls.SuitsIs(
      ['Joker', 'Spades', 'Diamonds', 'Clubs', 'Hearts'])
    cls.RanksIs([
      'Low',
      'Ace', '2', '3', '4', '5', '6', '7', '8', '9',
      'Ten', 'Jack', 'Queen', 'King',
      'High'])


class FrenchDeck(Deck):
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
        card = Card(rank, suit)
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
