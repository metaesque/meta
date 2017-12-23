import demo.cards2  # target=//demo/cards2:cards2
##########  End Imports  ##########


class FrenchDeckMeta(demo.cards2.DeckMeta):
  """Auto-generated meta class for demo.cards2.FrenchDeck."""

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
