#include "demo/cards2_test/DeckTestMeta.h"

namespace demo {
namespace cards2_test {


static std::vector<void**> _bases;
static std::map<std::string, void**> _symbols;
DeckTestMeta* MetaDeckTest = new DeckTestMeta("demo.cards2_test.DeckTestMeta", _bases, _symbols);

}  // cards2_test
}  // demo
