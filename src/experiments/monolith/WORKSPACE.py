
######################################
# Language: Python
######################################
# - releases: https://github.com/bazelbuild/rules_python/releases
# - tutorials
#    - https://earthly.dev/blog/build-and-deploy-pyapp-with-bazel/
# - python parsers
#    - https://docs.python.org/3.9/library/parser.html
#    - https://github.com/lark-parser/lark

# WORKSPACE: https://github.com/bazelbuild/rules_python/releases "Paste this snippet into your WORKSPACE file:"

http_archive(
    name = "rules_python",
    sha256 = "e85ae30de33625a63eca7fc40a94fea845e641888e52f32b6beea91e8b1b2793",
    # sha256 = "9acc0944c94adb23fba1c9988b48768b1bacc6583b52a2586895c5b7491e2e31",
    strip_prefix = "rules_python-0.27.1",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.27.1/rules_python-0.27.1.tar.gz",
    # url = "https://github.com/bazelbuild/rules_python/releases/download/0.27.0/rules_python-0.27.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories")
py_repositories()
