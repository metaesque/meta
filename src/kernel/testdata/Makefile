NEWSUFFIX := 2
BAZEL = /usr/local/bin/bazel
BASELANGS = python javascript cpp

default:
	echo "Specify explicit target"

# target: metac-*
#   Compile testdata2/$*.meta using meta2
metac-%:
	meta2 compile $*.meta2 2>&1 | metafilt

# target: can-*
#   Canonicalize a named .meta2 file
can-%:
	meta2 canonical $*.meta2 2>&1 | metafilt

# target: can-*
#   Canonicalize a named .meta2 file showing the expanded version
canx-%:
	meta2 --expand canonical $*.meta2 2>&1 | metafilt

# target: sample_logs
#   WARNING: Be careful about regenerating these logs ... new data will
#   break metax.c.Compiler.{parseBazelOutput,formatBazelOutput} tests.
#	
#   How to create new sample_logs for use in metax.c.Compiler.parseBazelOutput
#    % cd $METAROOT/src/kernel/testdata2
#    % cd sample_logs
#    % mv bazel_output bazel_output.old
#    % mv demo demo.old
#    % cd ..
#    % meta2 --raw --test_output=summary demo.cards2 > sample_logs/bazel_stdout 2> sample_logs/bazel_stderr
#    % grep 'blaze: Entering directory ' sample_logs/bazel_stdout
#    - the directory output by the above command is $root
#    % ls $root/bazel-out/local-fastbuild/testlogs/demo
#    - verify that the directory contains cards2_test
#    % mv ./sample_logs/demo ./sample_logs/demo.old
#    % cp -r $root/bazel-out/local-fastbuild/testlogs/demo sample_logs/demo
sample_logs:
	@echo "Read the docs associated with the 'sample_logs' target in Makefile'"

# target refresh_repo:
#   Recreate the 'repo' subdir from local live repository.
#
#   WARNING: This will probably break tests (they will need to be fixed).
#
#   NOTE: We do NOT use the 'meta2' capability of implicitly detecting 
#   .meta2 and fqns because this target is used when we are first setting
#   up bazel log parsing code in a new language (the files in the repo
#   directory will help us parse the logs for a new baselang).
#
#   The directory is made read-only to ensure that no tests write into it.
refresh_repo:
	find repo | xargs chmod +w
	rm -rf repo.bk
	mv repo repo.bk
	mkdir repo; cd repo; tar xzf ../../../templates/oopl.tgz
	for basel in $(BASELANGS) ; do \
		meta2 -b $$basel --metadir=repo ../root.meta2 ../test.meta2 cards2.meta2; \
		cd repo/oopl/$${basel}; \
		$(BAZEL) build //demo/cards2:cards2; \
		$(BAZEL) test //demo/cards2_test:cards2_test; \
		cd ../../..; \
	done
	find repo | xargs chmod -w

# target err:
#   Generates data useful for testing method Compiler.filterMetaOutput
err: .FORCE
	metac err.meta
	cp $(shell metac config repository_path)/oopl/python/demo/err/* err


.FORCE:
