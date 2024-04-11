cc_library(
  name = "Shape",
  srcs = ["Shape.cc"],
  hdrs = ["Shape.hh"],
  visibility = ["//visibility:public"],
)

cc_library(
  name = "Rectangle",
  srcs = ["Rectangle.cc"],
  hdrs = ["Rectangle.hh"],
  deps = [":Shape"],
  visibility = ["//visibility:public"],
)

cc_binary(
  name = "area",
  srcs = ["area.cc"],
  deps = [":Rectangle"],
  visibility = ["//visibility:public"],
)
