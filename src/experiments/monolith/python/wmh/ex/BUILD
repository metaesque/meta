py_library(
  name = "ex",
  srcs = ["__init__.py"],
  # TODO: Define and add metax/root:root to deps
  deps = [],
  visibility = ['//visibility:public'],
)

py_binary(
  name = "area",
  srcs = ["area.py"],
  # See comment in ../ex_test/BUILD about imports.
  imports = ['../..'],
  deps = [":ex"],
)

