load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_library")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_binary")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_test")

closure_js_library(
  name = "Card",
  srcs = ['Card.js'],
  deps = [],
  suppress = ["JSC_UNKNOWN_EXPR_TYPE"],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "Pile",
  srcs = ['Pile.js'],
  deps = [],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "play_lib",
  srcs = ['play.js'],
  deps = [":Card", ":Pile"],
  visibility = ['//visibility:public'],
)

closure_js_binary(
  name = "main",
  deps = [
    ":play_lib",
    ":Card",
    ":Pile",
  ],
  entry_points = [
    "goog:ex.cards.game"
  ],
)
