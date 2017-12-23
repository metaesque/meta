#include "demo/cards2_test/PileTestMeta.h"

namespace demo {
namespace cards2_test {


static std::vector<void**> _bases;
static std::map<std::string, void**> _symbols;
PileTestMeta* MetaPileTest = new PileTestMeta("demo.cards2_test.PileTestMeta", _bases, _symbols);

}  // cards2_test
}  // demo
