# TODO(wmh): Should this be placed in <root>/javascript/BUILD instead of
# <root>/BUILD? We want all javascript-specific functionality in
#  <root>/javascript if possible.

# npm_link_all_packages:
#  - creates target "node_modules", which contains all the npm packages
#    required by the project.
#  - will be used by other bazel targets that depend on these packages
#  - dlLinks all npm packages to bazel-bin/node_modules from:
#     - /WORKSPACE npm_translate_lock(name = "npm")
#     - packages from manual /WORKSPACE npm_import rules
#  - does something with the virtual store
#      bazel-bin/node_modules/.aspect_rules_js
#    since /pnpm-lock.yaml is the root of the pnpm workspace.
#    TODO(wmh): what exactly is done with this?
#  - scans package.json in current directory and creates a symlink for each
#    dependency listed in the file (symlinks are placed in the node_modules
#    directory of the current workspace).
#  - cretes directory node_modules in the root of the Bazel workspace
#  - see https://betterprogramming.pub/creating-a-react-application-in-a-bazel-monorepo-9bbf67ce2030
#    for context on above comments.
load("@npm//:defs.bzl", "npm_link_all_packages")
npm_link_all_packages(
    name = "node_modules"
)
