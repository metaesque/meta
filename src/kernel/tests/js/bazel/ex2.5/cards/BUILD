load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_library")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_binary")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_test")

closure_js_library(
  name = "Card",
  srcs = ['Card.js'],
  deps = [],
  suppress = [],
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "CardTest",
  srcs = ['Card_test.js'],
  deps = [
    "//ex2/cards:Card",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  entry_points = ['ex2.cards.CardTest'],
)

closure_js_library(
  name = "Pile",
  srcs = ['Pile.js'],
  deps = [":Card"],
  suppress = [],
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "PileTest",
  srcs = ['Pile_test.js'],
  deps = [
    "//ex2/cards:Pile",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  entry_points = ['ex2.cards.PileTest'],
)
