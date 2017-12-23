
cc_library(
  name = "TestCaseMeta",
  srcs = ['TestCaseMeta.cc'],
  hdrs = ['TestCaseMeta.h'],
  deps = ['//metax/root:ObjectMetaRoot'],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_library(
  name = "TestCase",
  srcs = ['TestCase.cc'],
  hdrs = ['TestCase.h'],
  deps = [
    "//metax/root:Error",
    "//metax/test:TestCaseMeta",
    "@gtest//:main",
  ],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)
