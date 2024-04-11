cc_test(
  name = "RectangleTest",
  size = "small",
  srcs = ["RectangleTest.cc"],
  deps = ["//cpp/wmh/ex:Rectangle", "@gtest//:gtest_main"],
  visibility = ["//visibility:public"],
)

test_suite(
  name = "ex_test",
  tests = [
    ":RectangleTest",
  ],
)


# Initial testing ... can be removed if we want to clean up.
cc_test(
  name = "hello_test",
  size = "small",
  srcs = ["hello_test.cc"],
  deps = ["@gtest//:gtest_main"],
)

