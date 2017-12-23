load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_library")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_binary")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_test")

closure_js_library(
  name = "TestCase",
  srcs = ['TestCase_test.js'],
  deps = ['//metax/test:TestCase'],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "CardTestMeta",
  srcs = ['CardTestMeta.js'],
  deps = ['//metax/test:TestCaseMeta'],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "CardTest",
  srcs = ['Card_test.js'],
  deps = [
    "//demo/cards2:Card",
    "//demo/cards2_test:CardTestMeta",
    "//demo/cards2_test:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "SIMPLE",
  entry_points = ['demo.cards2_test.CardTest'],
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "CardMetaTest",
  srcs = ['CardMeta_test.js'],
  deps = [
    "//demo/cards2:CardMeta",
    "//demo/cards2_test:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "SIMPLE",
  entry_points = ['demo.cards2_test.CardMetaTest'],
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "PileTestMeta",
  srcs = ['PileTestMeta.js'],
  deps = ['//metax/test:TestCaseMeta'],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "PileTest",
  srcs = ['Pile_test.js'],
  deps = [
    "//demo/cards2:Pile",
    "//demo/cards2_test:PileTestMeta",
    "//demo/cards2_test:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "SIMPLE",
  entry_points = ['demo.cards2_test.PileTest'],
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "PileMetaTest",
  srcs = ['PileMeta_test.js'],
  deps = [
    "//demo/cards2:PileMeta",
    "//demo/cards2_test:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "SIMPLE",
  entry_points = ['demo.cards2_test.PileMetaTest'],
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "DeckTestMeta",
  srcs = ['DeckTestMeta.js'],
  deps = ['//metax/test:TestCaseMeta'],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "DeckTest",
  srcs = ['Deck_test.js'],
  deps = [
    "//demo/cards2:Deck",
    "//demo/cards2_test:DeckTestMeta",
    "//demo/cards2_test:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "SIMPLE",
  entry_points = ['demo.cards2_test.DeckTest'],
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "DeckMetaTest",
  srcs = ['DeckMeta_test.js'],
  deps = [
    "//demo/cards2:DeckMeta",
    "//demo/cards2_test:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "SIMPLE",
  entry_points = ['demo.cards2_test.DeckMetaTest'],
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "FrenchDeckTestMeta",
  srcs = ['FrenchDeckTestMeta.js'],
  deps = ['//metax/test:TestCaseMeta'],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "FrenchDeckTest",
  srcs = ['FrenchDeck_test.js'],
  deps = [
    "//demo/cards2:FrenchDeck",
    "//demo/cards2_test:FrenchDeckTestMeta",
    "//demo/cards2_test:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "SIMPLE",
  entry_points = ['demo.cards2_test.FrenchDeckTest'],
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "FrenchDeckMetaTest",
  srcs = ['FrenchDeckMeta_test.js'],
  deps = [
    "//demo/cards2:FrenchDeckMeta",
    "//demo/cards2_test:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "SIMPLE",
  entry_points = ['demo.cards2_test.FrenchDeckMetaTest'],
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  testonly = 1,
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
