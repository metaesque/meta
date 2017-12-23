cc_library(
  name = "Person",
  srcs = ['Person.cc'],
  hdrs = ['Person.h'],
  deps = [],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

# https://docs.bazel.build/versions/master/cpp-use-cases.html#writing-and-running-c-tests
cc_test(
  name = "PersonTest",
    # Note that cc_test does not have hdrs, so we add the .h file to srcs.
    # See https://docs.bazel.build/versions/master/be/c-cpp.html#cc_test.srcs
    srcs = ["PersonTest.cc", "PersonTest.h"],
    copts = ["-Iexternal/gtest/include"],
    deps = [
      "@gtest//:main",
      "//src:Person",
    ],
)    
