# ----------------------------------------------------------------------
# Build targets for namespace meta.core

py_library(
  name = "core",
  srcs = ['core.py'],
  deps = ['//meta:root'],
  visibility = ['//visibility:public'],
)

py_test(
  name = "core_test",
  srcs = ['core_test.py'],
  deps = [
    "//meta:core",
    "//meta:testing",
  ],
  visibility = ['//visibility:public'],
)
# ----------------------------------------------------------------------
# Build targets for namespace meta.errors

py_library(
  name = "errors",
  srcs = ['errors.py'],
  deps = [],
  visibility = ['//visibility:public'],
)

py_test(
  name = "errors_test",
  srcs = ['errors_test.py'],
  deps = [
    "//meta:errors",
    "//meta:testing",
  ],
  visibility = ['//visibility:public'],
)
# ----------------------------------------------------------------------
# Build targets for namespace meta.root

py_library(
  name = "root",
  srcs = ['root.py'],
  deps = ['//meta:errors'],
  visibility = ['//visibility:public'],
)

py_test(
  name = "root_test",
  srcs = ['root_test.py'],
  deps = [
    "//meta:root",
    "//meta:testing",
  ],
  visibility = ['//visibility:public'],
)
# ----------------------------------------------------------------------
# Build targets for namespace meta.testing

py_library(
  name = "testing",
  srcs = ['testing.py'],
  deps = [
    "//meta:root",
    "@moxlib//:main",
    "@pyfakefs//:fake_filesystem",
  ],
  visibility = ['//visibility:public'],
)

py_test(
  name = "testing_test",
  srcs = ['testing_test.py'],
  deps = [
    "//meta:testing",
    "@moxlib//:main",
    "@pyfakefs//:fake_filesystem",
  ],
  visibility = ['//visibility:public'],
)

test_suite(
  name = 'namespace_tests',
  tests = [
    ':core_test',
    ':errors_test',
    ':root_test',
    ':testing_test',
  ]
)
