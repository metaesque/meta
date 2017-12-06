load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_library")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_binary")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_test")

closure_js_library(
  name = "Card__Meta",
  srcs = ['Card__Meta.js'],
  deps = ['//meta/root:ObjectMetaClass'],
  suppress = ['JSC_NULLABLE_RETURN_WITH_NAME'],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "Card",
  srcs = ['Card.js'],
  deps = [
    "//demo/cards2:Card__Meta",
    "//demo/cards2:Deck",
    "//meta/root:Object",
  ],
  suppress = [
    "JSC_NULLABLE_RETURN_WITH_NAME",
    "JSC_EXTRA_REQUIRE_WARNING",
  ],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "Pile__Meta",
  srcs = ['Pile__Meta.js'],
  deps = ['//meta/root:ObjectMetaClass'],
  suppress = ['JSC_NULLABLE_RETURN_WITH_NAME'],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "Pile",
  srcs = ['Pile.js'],
  deps = [
    "//demo/cards2:Card",
    "//demo/cards2:Pile__Meta",
    "//meta/root:Object",
  ],
  suppress = [
    "JSC_NULLABLE_RETURN_WITH_NAME",
    "JSC_EXTRA_REQUIRE_WARNING",
  ],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "Deck__Meta",
  srcs = ['Deck__Meta.js'],
  deps = ['//demo/cards2:Pile__Meta'],
  suppress = ['JSC_NULLABLE_RETURN_WITH_NAME'],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "Deck",
  srcs = ['Deck.js'],
  deps = [
    "//demo/cards2:Deck__Meta",
    "//demo/cards2:Pile",
  ],
  suppress = [
    "JSC_NULLABLE_RETURN_WITH_NAME",
    "JSC_EXTRA_REQUIRE_WARNING",
  ],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "FrenchDeck__Meta",
  srcs = ['FrenchDeck__Meta.js'],
  deps = ['//demo/cards2:Deck__Meta'],
  suppress = ['JSC_NULLABLE_RETURN_WITH_NAME'],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "FrenchDeck",
  srcs = ['FrenchDeck.js'],
  deps = [
    "//demo/cards2:Card",
    "//demo/cards2:Deck",
    "//demo/cards2:FrenchDeck__Meta",
  ],
  suppress = [
    "JSC_NULLABLE_RETURN_WITH_NAME",
    "JSC_EXTRA_REQUIRE_WARNING",
  ],
  visibility = ['//visibility:public'],
)
