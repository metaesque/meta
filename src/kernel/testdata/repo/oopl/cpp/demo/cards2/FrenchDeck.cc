#include "demo/cards2/FrenchDeck.h"

namespace demo {
namespace cards2 {


FrenchDeck::FrenchDeck(bool jokers) {
  auto& cards = this->cardsRef();
  for (int suit = 1; suit < 5; ++suit) {
    for (int rank = 1; rank < 14; ++rank) {
      Card* card = new Card(rank, suit);
      cards.push_back(card);
    }
  }
  if (jokers) {
    Card* lowjoker = new Card(0, 0);
    cards.push_back(lowjoker);
    Card* highjoker = new Card(14, 0);
    cards.push_back(highjoker);
  }
}

std::string FrenchDeck::asStr(demo::cards2::Card* card, bool full) {
  auto* meta = dynamic_cast<FrenchDeckMeta*>(this->meta());
  auto& suits = meta->Suits();
  auto& ranks = meta->Ranks();
  std::string result;
  if (full) {
    result.append(ranks[card->rank()]);
    result.append(" of ");
    result.append(suits[card->suit()]);
  } else {
    result.push_back(ranks[card->rank()][0]);
    result.push_back(suits[card->suit()][0]);
  }
  return result;
}

metax::root::ObjectMetaRoot* FrenchDeck::meta() {
  return MetaFrenchDeck;
}


}  // cards2
}  // demo
