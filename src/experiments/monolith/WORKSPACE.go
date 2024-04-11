
######################################
# Language: Go
######################################

# Go Rules
#   http_archive(
#       name = "io_bazel_rules_go",
#       url = "https://github.com/bazelbuild/rules_go/releases/download/0.18.3/rules_go-0.18.3.tar.gz",
#       sha256 = "86ae934bd4c43b99893fc64be9d9fc684b81461581df7ea8fc291c816f5ee8c5",
#   )
#
#   load("@io_bazel_rules_go//go:deps.bzl", "go_rules_dependencies", "go_register_toolchains")
#   go_rules_dependencies()
#   go_register_toolchains()

# Gazelle (creates Bazel rules from standard Go builds)
#   http_archive(
#       name = "bazel_gazelle",
#       urls = ["https://github.com/bazelbuild/bazel-gazelle/releases/download/0.17.0/bazel-gazelle-0.17.0.tar.gz"],
#       sha256 = "3c681998538231a2d24d0c07ed5a7658cb72bfb5fd4bf9911157c0e9ac6a2687",
#   )
#   load("@bazel_gazelle//:deps.bzl", "gazelle_dependencies", "go_repository")
#   gazelle_dependencies()

# Go libraries
#   go_repository(
#       name = "io_rsc_quote",
#       importpath = "rsc.io/quote",
#       tag = "v1.5.2",
#   )
#
#   go_repository(
#       name = "io_rsc_sampler",
#       importpath = "rsc.io/sampler",
#       tag = "v1.3.0",
#   )
#
#   go_repository(
#       name = "org_golang_x_text",
#       commit = "14c0d48ead0c",
#       importpath = "golang.org/x/text",
#   )
