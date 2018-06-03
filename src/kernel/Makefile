DIFF_FLAGS = -y --suppress-common-lines -W 160

# target default:
#   Default targets are dangerous
default:
	@echo "Specify a target."""


# target test:
#   Run tests on the Meta implementation of Meta.
test: fullmeta-py
	meta2 -b py -r metax.fs metax.logs metax.c metax.root metax.cli metax.test

# target slowtest:
#   Run tests on the Meta implementation of Meta.
#   Why is this so slow???
slowtest: fullmeta-py
	meta2 -b py metax.fs metax.logs metax.c metax.root metax.cli metax.test

# target meta-%:
#   Compile all code needed in order to compile and execute a Meta program in
#   the specified baselang.
#   - required:
#     - root.meta2: everything inherits from metax.root.Object and relies on 
#       metax.root.MetaObject for resources, etc.
#     - test.meta2: all unit tests inherit from metax.test.TestCase
#   - pseudo-optional:
#     - cli.meta2: only needed if the Meta code needs metax.root.MetaObject.CLI(),
#       which is simply set to null when the CLI is unavailable.
#   - not required:
#     - parser.meta2: only needed if one wants to compile Meta in this baselang
#     - fs.meta2: only needed by parser.meta2
#     - logs.meta2: only needed by parser.meta2
#     - shell.meta2: only needed if the Meta code uses metax.c.shell or metax.lib.shell
meta-%:
	meta2 -b $* root.meta2 test.meta2

# target fullmeta-%:
#   Compile all code needed to compile Meta in the specified baselang.
fullmeta-%:
	meta2 -b $* *.meta2

# target oopl:
#   Ensure that ${METAREP}${NEWSUFFIX}/oopl is bazel-ready by overlaying
#   ../templates${NEWSUFFIX}/oopl.tgz on ${METAREP}${NEWSUFFIX}/oopl.
oopl: 
	@cd ../templates; make update

# target shell:
#   Pull up the interactive meta shell
shell: fullmeta-py
	meta2 shell

# target emacs:
#   Create the emacs major mode for a given metalang, version 2
emacs: fullmeta-py
	meta2 emacs

# target cards1-%:
#   Compile a very simple .meta2 file into a baselang.
cards1-%: fullmeta-py
	cd testdata; meta2 -b $* cards1.meta2

# target cards2-%:
#   Compile a simple .meta2 file into a baselang and invoke unit tests.
cards2-%: fullmeta-py
	cd testdata; meta2 -b $* -rv cards2.meta2 demo.cards2

# target html-%:
#   Generate the HTML files for a metafile and its basefiles.
html-%: fullmeta-py
	cd testdata; meta2 -b $* html cards1.meta2

# target setup:
#   Perform an initial setup of code needed to get Meta working.
setup: .FORCE
	meta2 --meta_version current root.meta2 test.meta2 fs.meta2 logs.meta2 shell.meta2
	meta2 --meta_version current parser.meta2 shell.meta2 cli.meta2
	cd ../lib; meta2 --meta_version current markdown.meta2 shell.meta2

# target snapshot:
#   Create a snapshot (e.g. v0.7.0.12, with no .tgz files)
snapshot: .FORCE
	meta2 snapshot

# target release:
#   Create a release (e.g. v0.7.1, with .tgz files)
release: .FORCE
	meta2 snapshot --release

.FORCE:
