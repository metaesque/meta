load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_library")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_binary")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_test")

closure_js_library(
  name = "CardMeta",
  srcs = ['CardMeta.js'],
  deps = ['//metax/root:ObjectMeta'],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "Card",
  srcs = ['Card.js'],
  deps = [
    "//demo/cards2:CardMeta",
    "//metax/root:Object",
  ],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "PileMeta",
  srcs = ['PileMeta.js'],
  deps = ['//metax/root:ObjectMeta'],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "Pile",
  srcs = ['Pile.js'],
  deps = [
    "//demo/cards2:Card",
    "//demo/cards2:PileMeta",
    "//metax/root:Object",
  ],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "DeckMeta",
  srcs = ['DeckMeta.js'],
  deps = ['//demo/cards2:PileMeta'],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "Deck",
  srcs = ['Deck.js'],
  deps = [
    "//demo/cards2:DeckMeta",
    "//demo/cards2:Pile",
  ],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "FrenchDeckMeta",
  srcs = ['FrenchDeckMeta.js'],
  deps = ['//demo/cards2:DeckMeta'],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "FrenchDeck",
  srcs = ['FrenchDeck.js'],
  deps = [
    "//demo/cards2:Card",
    "//demo/cards2:Deck",
    "//demo/cards2:FrenchDeckMeta",
  ],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)
