load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_library")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_binary")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_test")

closure_js_test(
  name = "CardTest",
  srcs = ['Card_test.js'],
  deps = [
    "//ex/cards:Card",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  entry_points = ['ex.cards_test.CardTest'],
  # compilation_level = "ADVANCED",
  compilation_level = "SIMPLE",
  # compilation_level = "WHITESPACE_ONLY",
  size = "small",
  suppress = ["JSC_UNKNOWN_EXPR_TYPE"],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "PileTest",
  srcs = ['Pile_test.js'],
  deps = [
    "//ex/cards:Pile",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  entry_points = ['ex.cards_test.PileTest'],
  # compilation_level = "ADVANCED",
  compilation_level = "SIMPLE",
  # compilation_level = "WHITESPACE_ONLY",
  size = "small",
  testonly = 1,
  visibility = ['//visibility:public'],
)
