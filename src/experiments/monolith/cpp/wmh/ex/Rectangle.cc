#include "Rectangle.hh"

namespace wmh {
namespace ex {

Rectangle::Rectangle(float width, float height) {
  this->_width = width;
  this->_height = height;
}

float
Rectangle::area() const {
  return this->_width * this->_height;
}

}  // namespace ex
}  // namespace wmh
