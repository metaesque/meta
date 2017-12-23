load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_library")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_binary")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_test")

closure_js_library(
  name = "TestCaseTestMeta",
  srcs = ['TestCaseTestMeta.js'],
  deps = ['//metax/test:TestCaseMeta'],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "TestCaseTest",
  srcs = ['TestCase_test.js'],
  deps = [
    "//metax/test:TestCase",
    "//metax/test_test:TestCaseTestMeta",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "SIMPLE",
  entry_points = ['metax.test_test.TestCaseTest'],
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "TestCaseMetaTest",
  srcs = ['TestCaseMeta_test.js'],
  deps = [
    "//metax/test:TestCase",
    "//metax/test:TestCaseMeta",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "SIMPLE",
  entry_points = ['metax.test_test.TestCaseMetaTest'],
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

test_suite(
  name = "test_test",
  tests = [
    ":TestCaseTest",
    ":TestCaseMetaTest",
  ],
)
