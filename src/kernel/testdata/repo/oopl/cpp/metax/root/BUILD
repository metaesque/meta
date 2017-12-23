
cc_library(
  name = "ObjectMetaRoot",
  srcs = ['ObjectMetaRoot.cc'],
  hdrs = ['ObjectMetaRoot.h'],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_library(
  name = "ObjectMeta",
  srcs = ['ObjectMeta.cc'],
  hdrs = ['ObjectMeta.h'],
  deps = ['//metax/root:ObjectMetaRoot'],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_library(
  name = "Object",
  srcs = ['Object.cc'],
  hdrs = ['Object.h'],
  deps = [
    "//metax/root:ObjectMeta",
    "//metax/root:ObjectMetaRoot",
  ],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)

cc_library(
  name = "Error",
  srcs = ['Error.cc'],
  hdrs = ['Error.h'],
  deps = ['//metax/root:ObjectMetaRoot'],
  copts = ['-Iexternal/gtest/include'],
  visibility = ['//visibility:public'],
)
