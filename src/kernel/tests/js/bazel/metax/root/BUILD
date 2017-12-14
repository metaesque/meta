load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_library")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_binary")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_test")

closure_js_library(
  name = "Object",
  srcs = ['Object.js'],
  deps = [":ObjectMeta"],
  suppress = ["JSC_UNKNOWN_EXPR_TYPE"],
  language = "ECMASCRIPT6_STRICT",
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "ObjectMeta",
  srcs = ['ObjectMeta.js'],
  deps = [],
  suppress = ["JSC_UNKNOWN_EXPR_TYPE"],
  language = "ECMASCRIPT6_STRICT",
  visibility = ['//visibility:public'],
)
