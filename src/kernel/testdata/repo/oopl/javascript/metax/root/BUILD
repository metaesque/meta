load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_library")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_binary")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_test")

closure_js_library(
  name = "ObjectMetaRoot",
  srcs = ['ObjectMetaRoot.js'],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "ObjectMeta",
  srcs = ['ObjectMeta.js'],
  deps = ['//metax/root:ObjectMetaRoot'],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "Object",
  srcs = ['Object.js'],
  deps = ['//metax/root:ObjectMeta'],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
    "JSC_UNKNOWN_EXPR_TYPE",
  ],
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "Error",
  srcs = ['Error.js'],
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_NULLABLE_RETURN_WITH_NAME",
  ],
  visibility = ['//visibility:public'],
)
