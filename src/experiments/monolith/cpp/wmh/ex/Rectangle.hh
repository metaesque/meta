#pragma once
#include "Shape.hh"

namespace wmh {
namespace ex {

class Rectangle : public Shape {
  protected:
    float _width;
    float _height;
  public:
    Rectangle(float width, float height);

    virtual float area() const;
};

}  // namespace ex
}  // namespace wmh
