
######################################
# Language: Javascript
######################################
# - installation: https://github.com/aspect-build/rules_js
# - releases: https://github.com/aspect-build/rules_js/releases
# - docs: https://github.com/aspect-build/rules_js/tree/main/docs
# - parsers for Javascript syntax:
#    - https://www.npmjs.com/package/acorn
#    - https://esprima.org/
# - examples
#    - multiple packages and pnpm: https://stackoverflow.com/questions/75445658/how-to-setup-a-bazel-workspace-with-rules-js-for-a-monorepo-with-multiple-pack
#    - Creating a React Application in a Bazel Monorepo: https://betterprogramming.pub/creating-a-react-application-in-a-bazel-monorepo-9bbf67ce2030
#    - Getting started with Bazel for web developers: https://younessssssss.github.io/2023/09/22/getting-started-with-bazel-for-web-developper.html

# NOTE: Before aspect_rules_js existed, there was
# build_bazel_rules_nodejs
#  - referenced in lots of documentation
#  - no longer being maintained
#  - DO NOT USE
#  - example usage:
#     - https://levelup.gitconnected.com/build-and-run-your-first-node-js-application-with-bazel-898e1a92fac5

# Using aspect_rules_js:
#  - I had to perform the following one-time setup to get things working:
#     % npm install -g pnpm
#     % pnpm add three  # to create a pnpm-lock.yaml file
#     % echo -e 'node_modules' > .bazelignore
#     % bazel run -- @pnpm//:pnpm --dir $PWD install --lockfile-only
#     % bazel fetch @npm//...
#  - NOTE: The 'bazel run' command above may need to be executed anytime
#      % bazel clean --expunge
#    is invoked
#
#  - Further reading on pnpm:
#     - https://refine.dev/blog/how-to-use-pnpm/#how-to-use-pnpm
#
# WORKSPACE: https://github.com/aspect-build/rules_js/releases "Paste this snippet into your WORKSPACE file:"

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
http_archive(
    name = "aspect_rules_js",
    sha256 = "76a04ef2120ee00231d85d1ff012ede23963733339ad8db81f590791a031f643",
    strip_prefix = "rules_js-1.34.1",
    url = "https://github.com/aspect-build/rules_js/releases/download/v1.34.1/rules_js-v1.34.1.tar.gz",
)

load("@aspect_rules_js//js:repositories.bzl", "rules_js_dependencies")
rules_js_dependencies()

load("@rules_nodejs//nodejs:repositories.bzl", "DEFAULT_NODE_VERSION", "nodejs_register_toolchains")
nodejs_register_toolchains(
    name = "nodejs",
    node_version = DEFAULT_NODE_VERSION,
)

# For convenience, npm_translate_lock does this call automatically.
# Uncomment if you don't call npm_translate_lock at all.
#load("@bazel_features//:deps.bzl", "bazel_features_deps")
#bazel_features_deps()

# TODO(wmh): The instructions in
#   https://github.com/aspect-build/rules_js/releases
# differ slightly from those in
#   https://github.com/aspect-build/rules_jest/releases
# WRT npm_translate_lock (different src, and latter adds npmrc attr)

load("@aspect_rules_js//npm:repositories.bzl", "npm_translate_lock")
npm_translate_lock(
    name = "npm",
    npmrc = "//:.npmrc",
    pnpm_lock = "//:pnpm-lock.yaml",
    verify_node_modules_ignored = "//:.bazelignore",
)

load("@npm//:repositories.bzl", "npm_repositories")
npm_repositories()

####
# Unit Testing in Javascript using Jest
#  - docs:
#     - https://github.com/aspect-build/rules_jest/blob/main/docs/jest_test.md
#     - https://jestjs.io/docs/setup-teardown
#  - releases: https://github.com/aspect-build/rules_jest/releases
#
# WORKSPACE: https://github.com/aspect-build/rules_jest/releases  "WORKSPACE snippet:"

http_archive(
    name = "aspect_rules_jest",
    sha256 = "cae44cf7862b71f30c2ba6df6473bc8021c7a6c92c7d1771a58ebf5c99eb5776",
    strip_prefix = "rules_jest-0.19.6",
    url = "https://github.com/aspect-build/rules_jest/releases/download/v0.19.6/rules_jest-v0.19.6.tar.gz",
)

# aspect_rules_jest setup
#  - Fetches the aspect_rules_jest dependencies.
#  - If you want to have a different version of some dependency,
#    you should fetch it *before* calling this.
#  - Alternatively, you can skip calling this function, so long as
#    you've already fetched all the dependencies.
load("@aspect_rules_jest//jest:dependencies.bzl", "rules_jest_dependencies")
rules_jest_dependencies()

####
# Using npm packages in Bazel
#  - https://github.com/aspect-build/rules_js/tree/main/docs#fetch-third-party-packages-from-npm
#  - https://github.com/aspect-build/rules_js/tree/main/docs#link-the-node_modules
#  - https://github.com/aspect-build/rules_js/blob/main/docs/npm_import.md
#  - in BUILD:
#      load("@aspect_rules_js//npm:repositories.bzl", "npm_import")
#      npm_import(
#        name = "npm__at_types_node__15.12.2",
#        package = "@types/node",
#        version = "15.12.2",
#        integrity = "sha512-zjQ69G564OCIWIOHSXyQEEDpdpGl+G348RAKY0XXy9Z5kU9Vzv1GMNnkar/ZJ8dzXB3COzD9Mo9NtRZ4xfgUww==",
#      )
