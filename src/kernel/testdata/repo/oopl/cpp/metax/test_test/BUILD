
cc_library(
  name = "TestCaseTestMeta",
  srcs = ['TestCaseTestMeta.cc'],
  hdrs = ['TestCaseTestMeta.h'],
  deps = ['//metax/test:TestCaseMeta'],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_test(
  name = "TestCaseTest",
  srcs = [
    "TestCaseTest.cc",
    "TestCaseTest.h",
  ],
  deps = [
    "//metax/test:TestCase",
    "//metax/test_test:TestCaseTestMeta",
  ],
  copts = ['-Iexternal/gtest/include'],
  size = "small",
  visibility = ['//visibility:public'],
)

cc_test(
  name = "TestCaseMetaTest",
  srcs = [
    "TestCaseMetaTest.cc",
    "TestCaseMetaTest.h",
  ],
  deps = [
    "//metax/test:TestCase",
    "//metax/test:TestCaseMeta",
  ],
  copts = ['-Iexternal/gtest/include'],
  size = "small",
  visibility = ['//visibility:public'],
)

test_suite(
  name = "test_test",
  tests = [
    ":TestCaseTest",
    ":TestCaseMetaTest",
  ],
)
