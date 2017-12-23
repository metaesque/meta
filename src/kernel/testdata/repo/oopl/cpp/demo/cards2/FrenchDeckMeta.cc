#include "demo/cards2/FrenchDeckMeta.h"

namespace demo {
namespace cards2 {


FrenchDeckMeta::FrenchDeckMeta(const std::string& name, std::vector<void**>& bases, std::map<std::string,void**>& symbols) : demo::cards2::DeckMeta(name, bases, symbols) {
  std::vector<std::string> suits = {
    "Joker", "Spades", "Diamonds", "Clubs", "Hearts"};
  this->SuitsIs(suits);
  std::vector<std::string> ranks = {
    "Low",
    "Ace", "2", "3", "4", "5", "6", "7", "8", "9",
    "Ten", "Jack", "Queen", "King",
    "High"
  };
  this->RanksIs(ranks);

  if (false) {
    this->SuitsIs({"Joker", "Spades", "Diamonds", "Clubs", "Hearts"});
    this->RanksIs({
      "Low",
      "Ace", "2", "3", "4", "5", "6", "7", "8", "9",
      "Ten", "Jack", "Queen", "King",
      "High"
    });
  }
}

static std::vector<void**> _bases;
static std::map<std::string, void**> _symbols;
FrenchDeckMeta* MetaFrenchDeck = new FrenchDeckMeta("demo.cards2.FrenchDeckMeta", _bases, _symbols);

}  // cards2
}  // demo
