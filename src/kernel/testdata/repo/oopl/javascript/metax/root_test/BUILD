load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_library")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_binary")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_test")

closure_js_library(
  name = "ObjectTestMeta",
  srcs = ['ObjectTestMeta.js'],
  deps = ['//metax/test:TestCaseMeta'],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "ObjectTest",
  srcs = ['Object_test.js'],
  deps = [
    "//metax/root:Object",
    "//metax/root_test:ObjectTestMeta",
    "//metax/test:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "SIMPLE",
  entry_points = ['metax.root_test.ObjectTest'],
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "ObjectMetaTest",
  srcs = ['ObjectMeta_test.js'],
  deps = [
    "//metax/root:ObjectMeta",
    "//metax/test:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "SIMPLE",
  entry_points = ['metax.root_test.ObjectMetaTest'],
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "ErrorTestMeta",
  srcs = ['ErrorTestMeta.js'],
  deps = ['//metax/test:TestCaseMeta'],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "ErrorTest",
  srcs = ['Error_test.js'],
  deps = [
    "//metax/root:Error",
    "//metax/root_test:ErrorTestMeta",
    "//metax/test:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "SIMPLE",
  entry_points = ['metax.root_test.ErrorTest'],
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

test_suite(
  name = "root_test",
  tests = [
    ":ObjectTest",
    ":ObjectMetaTest",
    ":ErrorTest",
  ],
)
