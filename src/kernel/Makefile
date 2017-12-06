DIFF_FLAGS = -y --suppress-common-lines -W 160

# target default:
#   Default targets are dangerous
default:
	@echo "Specify a target."""

# target test:
#   Run tests on the Meta implementation of Meta.
test: meta
	metac -r metax.fs metax.logs metax.c 

# target slowtest:
#   Run tests on the Meta implementation of Meta.
#   Why is this so slow???
slowtest: meta
	metac metax.fs metax.logs metax.c 

# target meta:
#   Compile all code needed for the rewrite of Meta into Meta<Pyton> (meta2)
#   Note that the rewrite is written using the meta1 technology, so most of
#   the source code has .meta suffixes.  However, root.meta2 and test.meta2
#   represent code written in Meta2 that define the top-level classes relied
#   on by everything in Meta2.	Note that source files that are to be parsed
#   with the meta2 compiler should end in .meta2.	
meta:
	metac fs.meta logs.meta parser.meta 
	meta2 root.meta2 test.meta2

# target oopl:
#   Ensure that ${METAREP}${NEWSUFFIX}/oopl is bazel-ready by overlaying
#   ../templates${NEWSUFFIX}/oopl.tgz on ${METAREP}${NEWSUFFIX}/oopl.
oopl: 
	@cd ../templates2; make update

# target emacs:
#   Create the emacs major mode for a given metalang, version 2
emacs: meta
	meta2 emacs

cards2:
	metac parser.meta
	cd testdata; meta2 -r cards2.meta2 demo.cards2

tmp2:
	metac parser.meta
	cd testdata; meta2 ex1.meta2 2>&1 | metafilt
