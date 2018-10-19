CC = /usr/local/wmh/gcc-8.2/bin/g++

# For clang:
#
#  This causes an infinite loop in the compiler
#  % make raw-clang-any
#
#  This works (but doesn't use any_cast)
#  % make raw-clang-custom
#
#  This fails (cannot find any-cast)
#  % make raw-clang-cast
#
# For g++:
#
#  This works as desired:
#  % make raw-gcc
#
#  This uses clang instead of g++. Works on any-clang.cc not using any_cast
#  % make clobber
#  % make bazel-default
#
#  This uses clang instead of g++. Fails on any-clang.cc when using any_cast.
#  % make clobber
#  % make bazel-default-cast
#
#  This rebuilds the CROSSTOOL using g++ (disabling ObjC).
#   - Fails because -Wthread-safety and -Wself-assign unrecognized
#  % make bazel-gcc
#  % make crosstool
#
#  If one edits the CROSSTOOL file and deletes the first occurrences of
#  -Wthread-safety and -Wself-assign unrecognized

run: any
	./any

raw-gcc: any.cc
	$(CC) -std=c++17 -O3 -o any any.cc && ./any

raw-clang-any: any.cc
	clang++ -std=c++1z -O3 -o any any.cc -stdlib=libc++ && ./any

raw-clang-custom: any-clang.cc
	clang++ -std=c++1z -O3 -o any any-clang.cc -stdlib=libc++ && ./any

raw-clang-cast: any-clang.cc
	clang++ -DCAST -std=c++1z -O3 -o any any-clang.cc -stdlib=libc++ && ./any

raw-gcc-gen: any.cc
	$(CC) -std=c++17 -O3 -o any any.cc && ./any

raw-clang-gen: any.cc
	clang++ -DCLANG -std=c++1z -O3 -o any any.cc -std=c++1z -stdlib=libc++ && ./any

bazel-gcc: .FORCE
	bazel build --cxxopt=-std=c++17 --verbose_failures --sandbox_debug :any

bazel-gcc-safe: .FORCE
	CC=$(CC) BAZEL_USE_CPP_ONLY_TOOLCHAIN=1 bazel build --cxxopt=-std=c++17 --verbose_failures --sandbox_debug :any

crosstool:
	@echo $$(bazel info execution_root)/external/local_config_cc/CROSSTOOL
	@echo $$(readlink $$(bazel info execution_root)/external/local_config_cc/CROSSTOOL)
	@mtime $$(bazel info execution_root)/external/local_config_cc/CROSSTOOL

hello: .FORCE
	bazel build :hello
	bazel-bin/hello
	bazel build --cxxopt=-std=c++1z --verbose_failures --sandbox_debug :hello
	bazel-bin/hello

bazel-default: .FORCE
	bazel build --cxxopt=-std=c++1z --verbose_failures --sandbox_debug :any_clang && bazel-bin/any_clang

bazel-default-cast: .FORCE
	bazel build --cxxopt=-DCAST --cxxopt=-std=c++1z --verbose_failures --sandbox_debug :any_clang && bazel-bin/any_clang

clobber:
	bazel clean --expunge
	touch WORKSPACE

bazel-version:
	bazel info release

# https://blog.bazel.build/2018/08/22/bazel-homebrew.html
bazel-upgrade:
	brew upgrade bazel

.FORCE:
