
cc_library(
  name = "CardMeta",
  srcs = ['CardMeta.cc'],
  hdrs = ['CardMeta.h'],
  deps = ['//metax/root:ObjectMeta'],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_library(
  name = "Card",
  srcs = ['Card.cc'],
  hdrs = ['Card.h'],
  deps = [
    "//demo/cards2:CardMeta",
    "//metax/root:Object",
  ],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_library(
  name = "PileMeta",
  srcs = ['PileMeta.cc'],
  hdrs = ['PileMeta.h'],
  deps = ['//metax/root:ObjectMeta'],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_library(
  name = "Pile",
  srcs = ['Pile.cc'],
  hdrs = ['Pile.h'],
  deps = [
    "//demo/cards2:Card",
    "//demo/cards2:PileMeta",
    "//metax/root:Object",
  ],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_library(
  name = "DeckMeta",
  srcs = ['DeckMeta.cc'],
  hdrs = ['DeckMeta.h'],
  deps = ['//demo/cards2:PileMeta'],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_library(
  name = "Deck",
  srcs = ['Deck.cc'],
  hdrs = ['Deck.h'],
  deps = [
    "//demo/cards2:DeckMeta",
    "//demo/cards2:Pile",
  ],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_library(
  name = "FrenchDeckMeta",
  srcs = ['FrenchDeckMeta.cc'],
  hdrs = ['FrenchDeckMeta.h'],
  deps = ['//demo/cards2:DeckMeta'],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_library(
  name = "FrenchDeck",
  srcs = ['FrenchDeck.cc'],
  hdrs = ['FrenchDeck.h'],
  deps = [
    "//demo/cards2:Card",
    "//demo/cards2:Deck",
    "//demo/cards2:FrenchDeckMeta",
  ],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)
