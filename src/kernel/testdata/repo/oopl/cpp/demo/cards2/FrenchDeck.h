#ifndef demo_cards2_FrenchDeck_h
#define demo_cards2_FrenchDeck_h 1

#include "demo/cards2/Card.h"
#include "demo/cards2/Deck.h"
#include "demo/cards2/FrenchDeckMeta.h"

namespace demo {
namespace cards2 {

// https://en.wikipedia.org/wiki/French_playing_cards
class FrenchDeck : public demo::cards2::Deck {
  public: FrenchDeck(bool jokers = false);
  // Provide a string representation of a given card.
  // 
  // Returns:
  //   Testing to see how things work.
  // Meta:suppress: reportUnknownTypes
  public: virtual std::string asStr(demo::cards2::Card* card, bool full = false);
  public: virtual metax::root::ObjectMetaRoot* meta();
};

}  // cards2
}  // demo


#endif // demo_cards2_FrenchDeck_h
