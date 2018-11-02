DIFF_FLAGS = -y --suppress-common-lines -W 160

METAGROUP = "Meta"
METAFILES = $(shell ls *.meta ../lib/*.meta)

include $(WMH)/Makefile.meta

# target default:
#   Default targets are dangerous
default:
	@echo "Specify a target."""

# target test:
#   Run tests on the Meta implementation of Meta.
test: fullmeta-py
	metac -b py -r metax.fs metax.logs metax.c metax.root metax.cli metax.test

# target vtest:
#   Run tests on the Meta implementation of Meta.
vtest: fullmeta-py
	metac -b py -rv metax.fs metax.logs metax.c metax.root metax.cli metax.test

# target slowtest:
#   Run tests on the Meta implementation of Meta.
#   Why is this so slow???
slowtest: fullmeta-py
	metac -b py metax.fs metax.logs metax.c metax.root metax.cli metax.test

# target meta-%:
#   Compile all code needed in order to compile and execute a Meta program in
#   the specified baselang.
#   - required:
#     - root.meta: everything inherits from metax.root.Object and relies on 
#       metax.root.MetaObject for resources, etc.
#     - test.meta: all unit tests inherit from metax.test.TestCase
#   - pseudo-optional:
#     - cli.meta: only needed if the Meta code needs metax.root.MetaObject.CLI(),
#       which is simply set to null when the CLI is unavailable.
#   - not required:
#     - parser.meta: only needed if one wants to compile Meta in this baselang
#     - fs.meta: only needed by parser.meta
#     - logs.meta: only needed by parser.meta
#     - shell.meta: only needed if the Meta code uses metax.c.shell or metax.lib.shell
meta-%:
	metac -b $* root.meta test.meta

# target fullmeta-%:
#   Compile all code needed to compile Meta in the specified baselang.
fullmeta-%:
	metac -b $* *.meta

# target oopl:
#   Ensure that ${METAREP}${NEWSUFFIX}/oopl is bazel-ready by overlaying
#   ../templates${NEWSUFFIX}/oopl.tgz on ${METAREP}${NEWSUFFIX}/oopl.
oopl: 
	@cd ../templates; make update

# target shell:
#   Pull up the interactive meta shell
shell: fullmeta-py
	metac shell

# target emacs:
#   Create the emacs major mode for a given metalang, version 2
emacs: fullmeta-py
	metac emacs

# target cards1-%:
#   Compile a very simple .meta file into a baselang.
cards1-%: fullmeta-py
	cd testdata; metac -b $* cards1.meta

# target cards2-%:
#   Compile a simple .meta file into a baselang and invoke unit tests.
cards2-%: fullmeta-py
	cd testdata; metac -b $* -rv cards2.meta demo.cards2

# target html-%:
#   Generate the HTML files for a metafile and its basefiles.
html-%: fullmeta-py
	cd testdata; metac -b $* html cards1.meta

# target setup:
#   Perform an initial setup of code needed to get Meta working.
setup: .FORCE
	metac --meta_version current root.meta test.meta fs.meta logs.meta shell.meta
	metac --meta_version current parser.meta shell.meta cli.meta
	cd ../lib; metac --meta_version current markdown.meta shell.meta

# target snapshot:
#   Create a snapshot (e.g. v0.7.0.12, with no .tgz files)
snapshot: .FORCE
	metac snapshot

# target release:
#   Create a release (e.g. v0.7.1, with .tgz files)
release: .FORCE
	metac snapshot --release

.FORCE:
