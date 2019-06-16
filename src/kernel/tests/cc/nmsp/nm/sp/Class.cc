#include "nm/sp/Class.h"

namespace nm {
namespace sp {

int Variable = 10;

int Function(int a) {
  std::cout << "Here in nm namespace with a=" << a
            << " Variable=" << Variable
            << std:: endl;
  return a * Variable;
}

Class::Class() {
  std::cout << "In nm::sp::Class::Class" << std::endl;
  this->instance_ = 2;
}

int Class::Static = 200;

}  // namespace sp
}  // namespace nm
