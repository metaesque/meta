load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_library")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_binary")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_test")

closure_js_library(
  name = "TestCaseMeta",
  srcs = ['TestCaseMeta.js'],
  deps = ['//metax/root:ObjectMetaRoot'],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "TestCase",
  srcs = ['TestCase.js'],
  deps = [
    "//metax/test:TestCaseMeta",
    "@io_bazel_rules_closure//closure/library:library",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)
