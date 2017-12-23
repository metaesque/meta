#include "demo/cards2_test/CardTestMeta.h"

namespace demo {
namespace cards2_test {


static std::vector<void**> _bases;
static std::map<std::string, void**> _symbols;
CardTestMeta* MetaCardTest = new CardTestMeta("demo.cards2_test.CardTestMeta", _bases, _symbols);

}  // cards2_test
}  // demo
