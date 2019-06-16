#include "nm/Class.h"

namespace nm {

int Variable = 10;

int Function(int a) {
  std::cout << "Here in nm namespace with a=" << a
            << " Variable=" << Variable
            << std:: endl;
  return a * Variable;
}

Class::Class() {
  std::cout << "In nm::Class::Class" << std::endl;
  this->instance_ = 1;
}

int Class::Static = 100;

}  // namespace nm
