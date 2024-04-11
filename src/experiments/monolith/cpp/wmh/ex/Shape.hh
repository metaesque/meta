#pragma once

namespace wmh {
namespace ex {

class Shape {
  public:
    Shape();

    virtual float area() const = 0;
};

}  // namespace ex
}  // namespace wmh


