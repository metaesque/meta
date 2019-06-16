#include <iostream>
#include "nm/namespace.h"
#include "nm/Class.h"
#include "nm/sp/namespace.h"
#include "nm/sp/Class.h"

int main(int argc, char** argv) {
  std::cout << "Hello World" << std::endl;

  std::cout << "From main "
            << "nm.VARIABLE=" << nm::VARIABLE
            << std:: endl;

  std::cout << "From main "
            << "nm.Variable=" << nm::Variable
            << std:: endl;

  nm::FUNCTION(1);
  nm::Function(1);
  nm::Class nm_class;

  std::cout << "From main "
            << "nm.sp.VARIABLE=" << nm::sp::VARIABLE
            << std:: endl;

  std::cout << "From main "
            << "nm.sp.Variable=" << nm::sp::Variable
            << std:: endl;

  nm::sp::FUNCTION(2);
  nm::sp::Function(2);
  nm::sp::Class nm_sp_class;

  return 0;
}
