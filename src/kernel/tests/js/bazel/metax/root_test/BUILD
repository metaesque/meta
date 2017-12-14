load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_library")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_binary")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_test")

closure_js_test(
  name = "ObjectTest",
  srcs = ['Object_test.js'],
  deps = [
    ":ObjectTestMeta",
    "//metax/root:Object",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  entry_points = ['metax.root_test.ObjectTest'],
  compilation_level = "SIMPLE",
  size = "small",
  suppress = [
    "JSC_UNKNOWN_EXPR_TYPE",
    "JSC_REFERENCE_TO_SHORT_IMPORT_BY_LONG_NAME_INCLUDING_SHORT_NAME",
    "JSC_MISSING_REQUIRE_WARNING",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "ObjectTestMeta",
  srcs = ['ObjectTestMeta.js'],
  deps = [],
  suppress = [],
  visibility = ['//visibility:public'],
)
