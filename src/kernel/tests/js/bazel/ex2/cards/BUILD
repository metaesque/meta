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

closure_js_library(
  name = "Pile",
  srcs = ['Pile.js'],
  deps = [":Card"],
  visibility = ['//visibility:public'],
  suppress = [
    "JSC_JSDOC_REFERENCE_TO_SHORT_IMPORT_BY_LONG_NAME_INCLUDING_SHORT_NAME",
    "CR_SUPERFLUOUS_SUPPRESS"
  ]
)

closure_js_binary(
  name = "cards",
  deps = [
    ":Card",
    ":Pile",
  ],
)
