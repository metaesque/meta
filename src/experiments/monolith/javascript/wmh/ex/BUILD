load("@aspect_rules_js//js:defs.bzl", "js_binary", "js_library", "js_test")

# https://github.com/aspect-build/rules_js/blob/main/docs/js_library.md
js_library(
  name = "Shape",
  srcs = ['Shape.mjs'],
  visibility = ['//visibility:public'],
)

js_library(
  name = "Rectangle",
  srcs = ["Rectangle.mjs"],
  deps = [":Shape"],
  visibility = ['//visibility:public'],
)

# https://github.com/aspect-build/rules_js/blob/main/docs/js_binary.md
js_binary(
  name = "area",
  entry_point = "area.mjs",
  data = [":Rectangle"],
)
