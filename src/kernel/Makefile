DIFF_FLAGS = -y --suppress-common-lines -W 160

METAGROUP = "Meta"
METAFILES = parser.meta attr.meta fs.meta cli.meta shells.meta logs.meta \
	    root.meta test.meta metameta.meta metaoopl.meta metadoc.meta \
	    ../lib/markdown.meta ../lib/shells.meta ../lib/units.meta	

include $(WMH)/Makefile.meta

# target default:
#   Default targets are dangerous
default:
	@echo "Specify a target."""

t:
	@echo $(METAFILES)

# target full:
#   Compile the meta source (including meta files from schemas if changed)
full: fullmeta-py

# target test:
#   Run tests on the Meta implementation of Meta.
test: fullmeta-py
	metac -b py -r metax.c metax.attr metax.fs metax.logs \
	metax.root metax.cli metax.test \
	metax.meta metax.oopl \
	metax.lib.markdown metax.lib.shell metax.units

# target vtest:
#   Run tests on the Meta implementation of Meta.
vtest: fullmeta-py
	metac -b py -rv metax.fs metax.logs metax.c metax.root metax.cli metax.test

# target diff-%:
#   Compare beta *.meta with current *.meta
diff-%: .FORCE
	diff --width=160 --recursive --suppress-common-lines -y \
	  ../../lib/versions/current/src/kernel/$*.meta \
	  $*.meta

# target pdiff-%:
#   Compare beta *.py with current *.py
#   Currently only works for $* equal to immediate child namespace within metax
#   e.g. make pdiff-c diffs metax.c
#   e.g. make pdiff-fs diffs metax.fs
pdiff-%: .FORCE
	diff --width=160 --recursive --suppress-common-lines -y \
	  $(shell metac --meta_version=current config repository_path)/oopl/python/metax/$*/__init__.py \
	  ../../lib/versions/current/lib/metax/$*/__init__.py

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

up%:
	cd ../schema/$*; metac meta$*.meta

schema%:
	cd ../schema/$*; metac schema $* schema.meta

cup%:
	cd ../schema/$*; metac --meta_version=current meta$*.meta

cschema%:
	cd ../schema/$*; metac --meta_version=current schema $* schema.meta

# target fullmeta-%:
#   Compile all code needed to compile Meta in the specified baselang.
fullmeta-%:
	echo "HHHHHHHHHHHHHHHHHEEEEEEEEEEEEEERRRRRRRRRRRRREEE"
	echo metac -b $* $(METAFILES)
	@echo "================================================================================"

fullmeta-py: ../schema/meta/metameta.meta ../schema/oopl/metaoopl.meta ../schema/doc/metadoc.meta .FORCE
	metac -b py $(METAFILES)
	@echo "================================================================================"

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
emacs-oopl emacs: fullmeta-py
	metac emacs oopl
emacs-%:
	metac emacs $*

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

# target bootstrap:
#   Perform an initial setup of code needed to get Meta working.
#   This target should work even if <repository_path>/oopl/python doesn't
#   exist, as long as <src_root>/lib/versions/current points to a valid
#   directory and <src_root>/src/bootstrap/metac.py exists.
bootstrap: .FORCE
	python ../bootstrap/metac.py --meta_version=current *.meta ../lib/*.meta
	python ../bootstrap/metac.py --meta_version=current *.meta ../lib/*.meta
	cd ../schema/meta; \
	python ../../bootstrap/metac.py --meta_version=current schema meta schema.meta; \
	python ../../bootstrap/metac.py --meta_version=current metameta.meta
	cd ../schema/oopl; \
	python ../../bootstrap/metac.py --meta_version=current schema oopl schema.meta; \
	python ../../bootstrap/metac.py --meta_version=current metaoopl.meta
	cd ../schema/doc; \
	python ../../bootstrap/metac.py --meta_version=current schema doc schema.meta; \
	python ../../bootstrap/metac.py --meta_version=current metadoc.meta


# target snapshot:
#   Create a snapshot (e.g. v0.7.0.12, with no .tgz files)
snapshot: .FORCE
	metac snapshot

# target release:
#   Create a release (e.g. v0.7.1, with .tgz files)
release: .FORCE
	metac snapshot --release

status:
	metac --metasrcfile=SRC --summary_counts


find-%:
	grep $* *.meta ../schema/*/schema.meta

.FORCE:
