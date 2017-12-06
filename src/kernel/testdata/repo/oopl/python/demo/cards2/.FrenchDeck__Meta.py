import demo.cards2  # target=//demo/cards2:cards2
##########  End Imports  ##########


class FrenchDeck__Meta(demo.cards2.Deck__Meta):
  """Auto-generated meta class for demo.cards2.FrenchDeck"""

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
