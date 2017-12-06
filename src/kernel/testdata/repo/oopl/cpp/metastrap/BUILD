cc_library(
  # This target is included in every C++ header file, so any files defined by
  # it or its dependencies are available.
  name = "__Meta__",
  hdrs = ["__Meta__.h"],
  deps = [
    ":Any",
  ],
  visibility = ["//visibility:public"],
)


cc_library(
  name = "Any",
  hdrs = ["Any.h"],
  visibility = ["//visibility:public"],
)
