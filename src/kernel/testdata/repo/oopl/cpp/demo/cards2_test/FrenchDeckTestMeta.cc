#include "demo/cards2_test/FrenchDeckTestMeta.h"

namespace demo {
namespace cards2_test {


static std::vector<void**> _bases;
static std::map<std::string, void**> _symbols;
FrenchDeckTestMeta* MetaFrenchDeckTest = new FrenchDeckTestMeta("demo.cards2_test.FrenchDeckTestMeta", _bases, _symbols);

}  // cards2_test
}  // demo
