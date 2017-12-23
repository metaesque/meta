
cc_library(
  name = "ObjectTestMeta",
  srcs = ['ObjectTestMeta.cc'],
  hdrs = ['ObjectTestMeta.h'],
  deps = ['//metax/test:TestCaseMeta'],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_test(
  name = "ObjectTest",
  srcs = [
    "ObjectTest.cc",
    "ObjectTest.h",
  ],
  deps = [
    "//metax/root:Object",
    "//metax/root_test:ObjectTestMeta",
    "//metax/test:TestCase",
  ],
  copts = ['-Iexternal/gtest/include'],
  size = "small",
  visibility = ['//visibility:public'],
)

cc_test(
  name = "ObjectMetaTest",
  srcs = [
    "ObjectMetaTest.cc",
    "ObjectMetaTest.h",
  ],
  deps = [
    "//metax/root:ObjectMeta",
    "//metax/test:TestCase",
  ],
  copts = ['-Iexternal/gtest/include'],
  size = "small",
  visibility = ['//visibility:public'],
)

cc_library(
  name = "ErrorTestMeta",
  srcs = ['ErrorTestMeta.cc'],
  hdrs = ['ErrorTestMeta.h'],
  deps = ['//metax/test:TestCaseMeta'],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_test(
  name = "ErrorTest",
  srcs = [
    "ErrorTest.cc",
    "ErrorTest.h",
  ],
  deps = [
    "//metax/root:Error",
    "//metax/root_test:ErrorTestMeta",
    "//metax/test:TestCase",
  ],
  copts = ['-Iexternal/gtest/include'],
  size = "small",
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
