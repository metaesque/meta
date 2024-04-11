
######################################
# Language: C++
######################################
# - releases: https://github.com/bazelbuild/rules_cc/releases
# - questions
#    - how do I specify g++ instead of clang?

# https://bazel.build/docs/cc-toolchain-config-reference
#   GCC
#    http_archive(
#        name = "aspect_gcc_toolchain",
#        sha256 = "3341394b1376fb96a87ac3ca01c582f7f18e7dc5e16e8cf40880a31dd7ac0e1e",
#        strip_prefix = "gcc-toolchain-0.4.2",
#        urls = [
#            "https://github.com/aspect-build/gcc-toolchain/archive/refs/tags/0.4.2.tar.gz",
#        ],
#    )
#
#    load("@aspect_gcc_toolchain//toolchain:repositories.bzl", "gcc_toolchain_dependencies")
#    gcc_toolchain_dependencies()
#    load("@aspect_gcc_toolchain//toolchain:defs.bzl", "gcc_register_toolchain", "ARCHS")
#    gcc_register_toolchain(
#        name = "gcc_toolchain_x86_64",
#        target_arch = ARCHS.x86_64,
#    )

# Unit Testing in C++
#  - https://google.github.io/googletest/quickstart-bazel.html
#  - https://google.github.io/googletest/primer.html
#  - TODO(wmh): How do I establish the sha256 value?
http_archive(
    name = "gtest",
    url = "https://github.com/google/googletest/archive/release-1.12.0.zip",
    #sha256 = "b58cb7547a28b2c718d1e38aee18a3659c9e3ff52440297e965f5edffe34b6d0",
    #build_file = "gtest.BUILD",
    strip_prefix = "googletest-release-1.12.0",
)
