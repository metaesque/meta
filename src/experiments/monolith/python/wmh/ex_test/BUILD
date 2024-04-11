py_test(
  name = "ex_test",
  main = "__init__.py",
  srcs = ['__init__.py'],
  deps = [
    "//python/wmh/ex:ex",
    # "//metax/test:test",
  ],
  # IMPORTANT: In the old setup (one WORKSPACE per baselang),
  # the default PYTHONPATH was sufficient to find fully-qualified
  # python modules out-of-the-box. But with all baselangs in one
  # WORKSPACE, we need to add <root>/python to PYTHONPATH. This
  # can be done via the 'import' attribute of py_test, but I do not
  # yet understand how to use $(rootpath ...) etc. The following
  # import works but is fragile (needs to be changed for each
  # build file depending on where this directory is relative to
  # <rootdir>/python.  Does $(bazel info bazel-bin) work??
  #
  # see 'imports' in
  #   https://bazel.build/reference/be/python#py_binary_args
  # and Makefile variables in
  #   https://bazel.build/reference/be/make-variables
  # also
  #  % bazel info --show_make_env
  imports = ['../..'],
  size = "small",
  visibility = ['//visibility:public'],
)
