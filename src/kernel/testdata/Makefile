NEWSUFFIX := 2

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
#   WARNING: This will probably break tests (they will need to be fixed).
#
#   The directory is made read-only to ensure that no tests write into it.
refresh_repo:
	find repo | xargs chmod +w
	rm -rf repo.bk
	mv repo repo.bk
	mkdir repo; cd repo; tar xvf ../../../templates2/oopl.tgz
	for basel in python javascript ; do \
		meta2 -b $$basel cards2.meta2; \
		mkdir -p repo/oopl/$$basel/demo; \
		cp -r $(METAREP)$(NEWSUFFIX)/oopl/$$basel/demo/{cards2,cards2_test} repo/oopl/$$basel/demo; \
	done
	touch repo/oopl/python/demo/__init__.py
	cp -r $(METAREP)$(NEWSUFFIX)/oopl/python/meta repo/oopl/python
	cd repo/oopl/python; /Users/wmh/src/meta/root/bin/bazel build //demo/cards2:cards2
	cd repo/oopl/python; /Users/wmh/src/meta/root/bin/bazel test //demo/cards2_test:cards2_test
	find repo | xargs chmod -w




