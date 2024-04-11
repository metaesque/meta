
######################################
# Language: Rust
######################################

# Rust Rules
#   git_repository(
#       name = "io_bazel_rules_rust",
#       commit = "d28b121396974a628b9cdb29b6ed7f4e370edb4e",
#       remote = "https://github.com/bazelbuild/rules_rust",
#       shallow_since = "1557167838 -0400",
#   )
#
#   load("@io_bazel_rules_rust//rust:repositories.bzl", "rust_repositories")
#   rust_repositories()
#
#   load("@io_bazel_rules_rust//:workspace.bzl", "bazel_version")
#   bazel_version(name = "bazel_version")

# FFI for Rust
#   new_git_repository(
#       name = "libc",
#       build_file = "libc.BUILD",
#       remote = "https://github.com/rust-lang/libc",
#       commit = "6ec4f81a3852797410b80296d3afd61f2b255a36",
#       shallow_since = "1484672371 +0000"
#   )
