
cc_library(
  name = "TestCase",
  srcs = ['TestCase.cc'],
  hdrs = ['TestCase.h'],
  deps = ['//metax/test:TestCase'],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_library(
  name = "CardTestMeta",
  srcs = ['CardTestMeta.cc'],
  hdrs = ['CardTestMeta.h'],
  deps = ['//metax/test:TestCaseMeta'],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_test(
  name = "CardTest",
  srcs = [
    "CardTest.cc",
    "CardTest.h",
  ],
  deps = [
    "//demo/cards2:Card",
    "//demo/cards2_test:CardTestMeta",
    "//demo/cards2_test:TestCase",
  ],
  copts = ['-Iexternal/gtest/include'],
  size = "small",
  visibility = ['//visibility:public'],
)

cc_test(
  name = "CardMetaTest",
  srcs = [
    "CardMetaTest.cc",
    "CardMetaTest.h",
  ],
  deps = [
    "//demo/cards2:CardMeta",
    "//demo/cards2_test:TestCase",
  ],
  copts = ['-Iexternal/gtest/include'],
  size = "small",
  visibility = ['//visibility:public'],
)

cc_library(
  name = "PileTestMeta",
  srcs = ['PileTestMeta.cc'],
  hdrs = ['PileTestMeta.h'],
  deps = ['//metax/test:TestCaseMeta'],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_test(
  name = "PileTest",
  srcs = [
    "PileTest.cc",
    "PileTest.h",
  ],
  deps = [
    "//demo/cards2:Pile",
    "//demo/cards2_test:PileTestMeta",
    "//demo/cards2_test:TestCase",
  ],
  copts = ['-Iexternal/gtest/include'],
  size = "small",
  visibility = ['//visibility:public'],
)

cc_test(
  name = "PileMetaTest",
  srcs = [
    "PileMetaTest.cc",
    "PileMetaTest.h",
  ],
  deps = [
    "//demo/cards2:PileMeta",
    "//demo/cards2_test:TestCase",
  ],
  copts = ['-Iexternal/gtest/include'],
  size = "small",
  visibility = ['//visibility:public'],
)

cc_library(
  name = "DeckTestMeta",
  srcs = ['DeckTestMeta.cc'],
  hdrs = ['DeckTestMeta.h'],
  deps = ['//metax/test:TestCaseMeta'],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_test(
  name = "DeckTest",
  srcs = [
    "DeckTest.cc",
    "DeckTest.h",
  ],
  deps = [
    "//demo/cards2:Deck",
    "//demo/cards2_test:DeckTestMeta",
    "//demo/cards2_test:TestCase",
  ],
  copts = ['-Iexternal/gtest/include'],
  size = "small",
  visibility = ['//visibility:public'],
)

cc_test(
  name = "DeckMetaTest",
  srcs = [
    "DeckMetaTest.cc",
    "DeckMetaTest.h",
  ],
  deps = [
    "//demo/cards2:DeckMeta",
    "//demo/cards2_test:TestCase",
  ],
  copts = ['-Iexternal/gtest/include'],
  size = "small",
  visibility = ['//visibility:public'],
)

cc_library(
  name = "FrenchDeckTestMeta",
  srcs = ['FrenchDeckTestMeta.cc'],
  hdrs = ['FrenchDeckTestMeta.h'],
  deps = ['//metax/test:TestCaseMeta'],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_test(
  name = "FrenchDeckTest",
  srcs = [
    "FrenchDeckTest.cc",
    "FrenchDeckTest.h",
  ],
  deps = [
    "//demo/cards2:FrenchDeck",
    "//demo/cards2_test:FrenchDeckTestMeta",
    "//demo/cards2_test:TestCase",
  ],
  copts = ['-Iexternal/gtest/include'],
  size = "small",
  visibility = ['//visibility:public'],
)

cc_test(
  name = "FrenchDeckMetaTest",
  srcs = [
    "FrenchDeckMetaTest.cc",
    "FrenchDeckMetaTest.h",
  ],
  deps = [
    "//demo/cards2:FrenchDeckMeta",
    "//demo/cards2_test:TestCase",
  ],
  copts = ['-Iexternal/gtest/include'],
  size = "small",
  visibility = ['//visibility:public'],
)

test_suite(
  name = "cards2_test",
  tests = [
    ":CardTest",
    ":CardMetaTest",
    ":PileTest",
    ":PileMetaTest",
    ":DeckTest",
    ":DeckMetaTest",
    ":FrenchDeckTest",
    ":FrenchDeckMetaTest",
  ],
)
