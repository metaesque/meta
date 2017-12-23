#ifndef demo_cards2_Pile_h
#define demo_cards2_Pile_h 1

#include "demo/cards2/Card.h"
#include "demo/cards2/PileMeta.h"
#include "metax/root/Object.h"

namespace demo {
namespace cards2 {

// A set of cards that partially or completely overlap.
class Pile : public metax::root::Object {
  using metax::root::Object::Object;

  // field cards : @vec<Card>
  //   The Card instances in this Pile
  private: std::vector<demo::cards2::Card*> _cards;
  public: virtual const std::vector<demo::cards2::Card*>& cards() const { return this->_cards; }
  public: virtual void cardsIs(std::vector<demo::cards2::Card*> value) { this->_cards = value; }
  public: virtual std::vector<demo::cards2::Card*>& cardsRef() { return this->_cards; }
  public: virtual metax::root::ObjectMetaRoot* meta();
};

}  // cards2
}  // demo


#endif // demo_cards2_Pile_h
