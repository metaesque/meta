load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_library")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_binary")
load("@io_bazel_rules_closure//closure:defs.bzl", "closure_js_test")

closure_js_library(
  name = "CardTest__Meta",
  srcs = ['CardTest__Meta.js'],
  deps = ['//meta/testing:TestCaseMetaClass'],
  suppress = [
    "JSC_NULLABLE_RETURN_WITH_NAME",
    "JSC_EXTRA_REQUIRE_WARNING",
  ],
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "CardTest",
  srcs = ['Card_test.js'],
  deps = [
    "//demo/cards2:Card",
    "//demo/cards2_test:CardTest__Meta",
    "//meta/testing:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "ADVANCED",
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_MISSING_PROVIDE",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "Card__MetaTest",
  srcs = ['Card__Meta_test.js'],
  deps = [
    "//demo/cards2:Card__Meta",
    "//meta/testing:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "ADVANCED",
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_MISSING_PROVIDE",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "PileTest__Meta",
  srcs = ['PileTest__Meta.js'],
  deps = ['//meta/testing:TestCaseMetaClass'],
  suppress = [
    "JSC_NULLABLE_RETURN_WITH_NAME",
    "JSC_EXTRA_REQUIRE_WARNING",
  ],
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "PileTest",
  srcs = ['Pile_test.js'],
  deps = [
    "//demo/cards2:Pile",
    "//demo/cards2_test:PileTest__Meta",
    "//meta/testing:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "ADVANCED",
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_MISSING_PROVIDE",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "Pile__MetaTest",
  srcs = ['Pile__Meta_test.js'],
  deps = [
    "//demo/cards2:Pile__Meta",
    "//meta/testing:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "ADVANCED",
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_MISSING_PROVIDE",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "DeckTest__Meta",
  srcs = ['DeckTest__Meta.js'],
  deps = ['//meta/testing:TestCaseMetaClass'],
  suppress = [
    "JSC_NULLABLE_RETURN_WITH_NAME",
    "JSC_EXTRA_REQUIRE_WARNING",
  ],
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "DeckTest",
  srcs = ['Deck_test.js'],
  deps = [
    "//demo/cards2:Deck",
    "//demo/cards2_test:DeckTest__Meta",
    "//meta/testing:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "ADVANCED",
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_MISSING_PROVIDE",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "Deck__MetaTest",
  srcs = ['Deck__Meta_test.js'],
  deps = [
    "//demo/cards2:Deck__Meta",
    "//meta/testing:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "ADVANCED",
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_MISSING_PROVIDE",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_library(
  name = "FrenchDeckTest__Meta",
  srcs = ['FrenchDeckTest__Meta.js'],
  deps = ['//meta/testing:TestCaseMetaClass'],
  suppress = [
    "JSC_NULLABLE_RETURN_WITH_NAME",
    "JSC_EXTRA_REQUIRE_WARNING",
  ],
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "FrenchDeckTest",
  srcs = ['FrenchDeck_test.js'],
  deps = [
    "//demo/cards2:FrenchDeck",
    "//demo/cards2_test:FrenchDeckTest__Meta",
    "//meta/testing:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "ADVANCED",
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_MISSING_PROVIDE",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

closure_js_test(
  name = "FrenchDeck__MetaTest",
  srcs = ['FrenchDeck__Meta_test.js'],
  deps = [
    "//demo/cards2:FrenchDeck__Meta",
    "//meta/testing:TestCase",
    "@io_bazel_rules_closure//closure/library:testing",
  ],
  compilation_level = "ADVANCED",
  size = "small",
  suppress = [
    "JSC_EXTRA_REQUIRE_WARNING",
    "JSC_MISSING_PROVIDE",
  ],
  testonly = 1,
  visibility = ['//visibility:public'],
)

test_suite(
  name = "cards2_test",
  tests = [
    ":CardTest",
    ":Card__MetaTest",
    ":PileTest",
    ":Pile__MetaTest",
    ":DeckTest",
    ":Deck__MetaTest",
    ":FrenchDeckTest",
    ":FrenchDeck__MetaTest",
  ],
)
