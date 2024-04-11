load("@aspect_rules_js//js:defs.bzl", "js_binary", "js_library", "js_test")

# https://github.com/aspect-build/rules_js/blob/main/docs/js_binary.md#js_test

js_test(
  name = "RectangleTest",
  size = "small",
  entry_point = "RectangleTest.mjs",
  data = ["//javascript/wmh/ex:Rectangle"],
  visibility = ["//visibility:public"],
)

test_suite(
  name = "ex_test",
  tests = [
    ":RectangleTest",
  ],
)
