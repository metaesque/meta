#include "metax/test/TestCase.h"

namespace metax {
namespace test {


TestCase::TestCase(const std::string& method_name) {
  this->_debug = false;
  this->_stdout = nullptr;
  this->_stderr = nullptr;
  this->_stdin = nullptr;
  this->_fs = nullptr;
  this->_stubs = nullptr;
  // User-provided code follows.
  int count = MetaTestCase->InstanceCount() + 1;
  MetaTestCase->InstanceCountIs(count);
  this->deblog(
    std::string("Invoking ") + this->name() + " initializer for "
    + method_name);
  this->method_nameIs(method_name);
}

const std::string& TestCase::status() {
  static std::string result("FIXME");
  return result;
}

void TestCase::deblog(const std::string& msg) {
  if (this->debug()) {
    std::cout << this->uid() << ": " << msg << std::endl;
  }
}

const std::string& TestCase::name() {
  static std::string result(typeid(*this).name());
  return result;
}

const std::string& TestCase::methname() {
  return this->method_name();
}

void TestCase::setenv(const std::string* evar, const std::string* value) {
  throw metax::root::Error("TestCase.setenv() not yet implemented");
}

std::stringstream* TestCase::newStr(const std::string* content) {
  std::stringstream* result;
  if (content == nullptr) {
    result = new std::stringstream();
  } else {
    result = new std::stringstream(*content);
  }
  // TODO(wmh): Add result to a C++-specific streams() field. In teardown(),
  // iterate over streams() and delete all elements.
  return result;
}

std::stringstream* TestCase::fp(const std::string* content) {
  std::stringstream* result;
  if (content == nullptr) {
    result = new std::stringstream();
  } else {
    result = new std::stringstream(*content);
  }
  // TODO(wmh): Add result to a C++-specific streams() field. In teardown(),
  // iterate over streams() and delete all elements.
  return result;
}

void TestCase::tmpFile(bool create) {
  throw metax::root::Error("TestCase.tmpFile() not yet implemented");
}

void TestCase::tmpDir(bool create) {
  throw metax::root::Error("TestCase.tmpDir() not yet implemented");
}

void TestCase::fileContents(void** path) {
  throw metax::root::Error("TestCase.fileContents() not yet implemented");
}

bool TestCase::isInteractive() {
  return MetaTestCase->Interactive();
}

bool TestCase::allowNetwork(void** guarding) {
  throw metax::root::Error("TestCase.allowNetwork() not yet implemented");
}

void TestCase::assertDictContains(std::map<std::string,void**>* data, std::map<std::string,void**>* subdata) {
  throw metax::root::Error(
    "TestCase.assertDictContains() not yet implemented");
}

void TestCase::startswith(const std::string* prefix, const std::string* strval) {
  throw metax::root::Error("TestCase.startswith() not yet implemented");
}

void TestCase::endswith(const std::string* suffix, const std::string* strval) {
  throw metax::root::Error("TestCase.endswith() not yet implemented");
}

void TestCase::contains(void** member, void** container, const std::string* msg) {
  throw metax::root::Error("TestCase.contains() not yet implemented");
}

void TestCase::matches(const std::string* restr, const std::string* value) {
  throw metax::root::Error("TestCase.matches() not yet implemented");
}

void TestCase::iseq(void** expected, void** item, void** message) {
  throw metax::root::Error("TestCase.iseq() not yet implemented");
}

void TestCase::noteq(void** expected, void** item, void** message) {
  throw metax::root::Error("TestCase.noteq() not yet implemented");
}

void TestCase::iseqstr(const std::string& expected, const std::string& item, const std::string* message) {
  throw metax::root::Error("TestCase.iseq() not yet implemented");
  if (message == nullptr) {
  } else {
  }
}

void TestCase::noteqstr(const std::string& expected, const std::string& item, const std::string* message) {
  throw metax::root::Error("TestCase.iseq() not yet implemented");
  if (message == nullptr) {
  } else {
  }
}

void TestCase::iseqvec(std::vector<void**>* expected, std::vector<void**>* items, const std::string* message) {
  throw metax::root::Error("TestCase.iseqvec() not yet implemented");
}

void TestCase::iseqmap(void** expected, void** data, void** msg, int32_t width) {
  throw metax::root::Error("TestCase.iseqmap() not yet implemented");
}

void TestCase::iseqtext(const std::string* first, const std::string* second, const std::string* text) {
  throw metax::root::Error("TestCase.iseqtext() not yet implemented");
}

void TestCase::iseqfile(void** file1, void** file2) {
  throw metax::root::Error("TestCase.iseqfile() not yet implemented");
}

void TestCase::iseqstrgold(void** content, void** golden) {
  throw metax::root::Error("TestCase.iseqstrgold() not yet implemented");
}

void TestCase::iseqfilegold(void** path, void** golden) {
  throw metax::root::Error("TestCase.iseqfilegold() not yet implemented");
}

void TestCase::isapprox(double f1, double f2, double delta, const std::string* msg) {
  throw metax::root::Error("TestCase.isapprox() not yet implemented");
}

void TestCase::islt(void** expected, void** item, void** message) {
  throw metax::root::Error("TestCase.islt() not yet implemented");
}

void TestCase::isle(void** expected, void** item, void** message) {
  throw metax::root::Error("TestCase.isle() not yet implemented");
}

void TestCase::isgt(void** expected, void** item, void** message) {
  throw metax::root::Error("TestCase.isgt() not yet implemented");
}

void TestCase::isge(void** expected, void** item, void** message) {
  throw metax::root::Error("TestCase.isge() not yet implemented");
}

void TestCase::raises(void** eclass, const void*& func, ...) {
  throw metax::root::Error("TestCase.raises() not yet implemented");
}

void TestCase::issame(void** obj1, void** obj2) {
  throw metax::root::Error("TestCase.issame() not yet implemented");
}

void TestCase::notsame(void** obj1, void** obj2) {
  throw metax::root::Error("TestCase.notsame() not yet implemented");
}

void TestCase::istrue(bool val, const std::string* msg) {
  throw metax::root::Error("TestCase.istrue() not yet implemented");
}

void TestCase::isfalse(bool val, const std::string* msg) {
  throw metax::root::Error("TestCase.isfalse() not yet implemented");
}

void TestCase::isnull(void** val, const std::string* msg) {
  throw metax::root::Error("TestCase.isnull() not yet implemented");
}

void TestCase::notnull(void** val, const std::string* msg) {
  throw metax::root::Error("TestCase.notnull() not yet implemented");
}

void TestCase::isinst(void** obj, void** cls) {
  throw metax::root::Error("TestCase.isinst() not yet implemented");
}

void TestCase::fail(const std::string* msg) {
  throw metax::root::Error("TestCase.fail() not yet implemented");
}

metax::root::ObjectMetaRoot* TestCase::meta() {
  return MetaTestCase;
}

void TestCase::SetUp() {
  this->::testing::Test::SetUp();
  // User-provided code follows.
  this->deblog(
    "Invoking " + this->name() + " setUp for " + this->methname());
}

void TestCase::SetUpTestCase() {
  if (MetaTestCase->Debug()) {
    std::cout << "Invoking " << MetaTestCase->metaname() << " SetUp" << std::endl;
  }
}

void TestCase::TearDown() {
  std::cerr << "Fix C++ teardown" << std::endl;
  this->::testing::Test::TearDown();
}

void TestCase::TearDownTestCase() {
  if (MetaTestCase->Debug()) {
    std::cerr << "Invoking " << MetaTestCase->metaname() << " TearDown" << std::endl;
  }
}


}  // test
}  // metax
