import demo.cards2  # target=//demo/cards2:cards2
import demo.cards2  # target=//demo/cards2:cards2
import meta.root  # target=//meta/root:root
##########  End Imports  ##########


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
