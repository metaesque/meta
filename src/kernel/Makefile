DIFF_FLAGS = -y --suppress-common-lines -W 160

# target default:
#   Default targets are dangerous
default:
	@echo "Specify a target."""

# target test:
#   Run tests on the Meta implementation of Meta.
test: meta-py
	metac -r metax.fs metax.logs metax.c 

# target slowtest:
#   Run tests on the Meta implementation of Meta.
#   Why is this so slow???
slowtest: meta-py
	metac metax.fs metax.logs metax.c 

# target meta-%:
#   Compile all code needed for the rewrite of Meta into Meta<Pyton> (meta2)
#   Note that the rewrite is written using the meta1 technology, so most of
#   the source code has .meta suffixes.  However, root.meta2 and test.meta2
#   represent code written in Meta2 that define the top-level classes relied
#   on by everything in Meta2.	Note that source files that are to be parsed
#   with the meta2 compiler should end in .meta2.	
meta-%:
	metac fs.meta logs.meta parser.meta 2>&1 | metafilt
	meta2 -b $* root.meta2 test.meta2

# target oopl:
#   Ensure that ${METAREP}${NEWSUFFIX}/oopl is bazel-ready by overlaying
#   ../templates${NEWSUFFIX}/oopl.tgz on ${METAREP}${NEWSUFFIX}/oopl.
oopl: 
	@cd ../templates; make update

# target shell:
#   Pull up the interactive meta shell
shell: meta-py
	meta2 shell

# target emacs:
#   Create the emacs major mode for a given metalang, version 2
emacs: meta-py
	meta2 emacs

# target cards1-%:
#   Compile a very simple .meta2 file into a baselang.
cards1-%: meta-%
	cd testdata; meta2 -b $* cards1.meta2

# target cards2-%:
#   Compile a simple .meta2 file into a baselang and invoke unit tests.
cards2-%: meta-%
	cd testdata; meta2 -b $* -r cards2.meta2 demo.cards2

# target html-%:
#   Generate the HTML files for a metafile and its basefiles.
html-%: meta-%
	cd testdata; meta2 -b $* html cards1.meta2
