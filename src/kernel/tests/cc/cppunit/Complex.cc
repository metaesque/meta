#include "Complex.h"

namespace testit {

bool operator==(const Complex &a, const Complex &b) {
  return a.real == b.real  &&  a.im == b.im;
}

}  // namespace testit
