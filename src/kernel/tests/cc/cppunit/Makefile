CXX     := g++
CFLAGS  := -Wall -Wno-c++11-extensions -g -O0 -I$(METAROOT)/root/include
LDFLAGS := -fprofile-generate -L$(METAROOT)/root/lib -lcppunit

SRCS    := $(shell ls *.cc)

# target default:
#   Default targets are dangerous
default:
	@echo "Specify an explicit target"

# Include any dependencies specified in .depend if they
# exist. One can recreate them with 'make depend'.
-include .depend

# target depend:
#   Alias for .depend
depend: .depend

# target .depend:
#   Compute all dependencies for .cc files in this dir.
.depend: $(SRCS)
	rm -f ./.depend
	$(CC) $(CFLAGS) -MM $^ >>./.depend;

# target Str.o:
#   Compile our class.
%.o:
	$(CXX) $(CFLAGS) -o $@ -c $<

# target StrTest:
#   An executable that will test the StrTest class.
%Test: %.o %Test.o
	$(CXX) $(LDFLAGS) -o $@ $^
	./$@

# target StrTest.txt:
#   Dumps expanded version of StrTest.cc so that one can see how
#   the various macros expand. Relies on some special // REM
#   hackery in the files to make it easy to find various portions
#   in the output.
StrTest.txt: .FORCE
	perl -i.bk -pe 's%// REM%REM%;' StrTest.cc StrTest.h
	$(CXX) $(CFLAGS) -E StrTest.cc > StrTest.txt
	cp StrTest.cc.bk StrTest.cc
	cp StrTest.h.bk StrTest.h
	rm -f StrTest.*.bk

# target testit:
#   An executable that will test all classes in the testit namespace.
testit: testit.o Str.o StrTest.o Complex.o ComplexTest.o
	$(CXX) $(LDFLAGS) -o $@ $^

.PHONY: StrTestCode
.FORCE:

