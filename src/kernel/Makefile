DIFF_FLAGS = -y --suppress-common-lines -W 160

# target default:
#   Default targets are dangerous
default:
	@echo "Specify a target."""


# target test:
#   Run tests on the Meta implementation of Meta.
test: meta-py
	meta2 -r metax.fs metax.logs metax.c metax.root metax.cli metax.test

# target slowtest:
#   Run tests on the Meta implementation of Meta.
#   Why is this so slow???
slowtest: meta-py
	meta2 metax.fs metax.logs metax.c metax.root metax.cli metax.test

# target meta-%:
#   Compile all code needed for Meta to function.
meta-%:
	meta2 -b $* *.meta2

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

##############################################################################
# Targets for the older version of meta2
#  - this older version was implemented by parser.meta
#  - parser.meta is compiled using parser.py
#  - with the existence of parser.meta2, we can completely remove
#    parser.py and parser.meta and make 'meta2' be 'metac', remove
#    the 2 suffix from files, etc.

# target otest:
#   Run tests on the Meta implementation of Meta.
otest: ometa-py
	metac -r metax.fs metax.logs metax.c 

# target oslowtest:
#   Run tests on the Meta implementation of Meta.
#   Why is this so slow???
oslowtest: ometa-py
	metac metax.fs metax.logs metax.c 

# target ometa-%:
#   Compile all code needed for the rewrite of Meta into Meta<Pyton> (meta2)
#   based on {parser,fs,logs}.meta and {root,test}.meta2.
ometa-%:
	metac fs.meta logs.meta parser.meta 2>&1 | metafilt
	meta2old -b $* root.meta2 test.meta2

# target oshell:
#   Pull up the interactive meta shell
oshell: ometa-py
	meta2old shell

# target oemacs:
#   Create the emacs major mode for a given metalang, version 2
oemacs: ometa-py
	meta2old emacs

# target ocards1-%:
#   Compile a very simple .meta2 file into a baselang.
ocards1-%: ometa-%
	cd testdata; meta2old -b $* cards1.meta2

# target ocards2-%:
#   Compile a simple .meta2 file into a baselang and invoke unit tests.
ocards2-%: ometa-%
	cd testdata; meta2old -b $* -r cards2.meta2 demo.cards2

# target ohtml-%:
#   Generate the HTML files for a metafile and its basefiles.
ohtml-%: ometa-%
	cd testdata; meta2old -b $* html cards1.meta2
