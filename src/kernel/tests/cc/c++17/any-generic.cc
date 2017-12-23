#include <iostream>
#include <string>
#ifdef CLANG
#   include <experimental/any>
    typedef std::experimental::any Any;
#   define AnyCast(thetype, theval) std::experimental::any_cast<thetype>(theval)
#else
#   include <any>
    typedef std::any Any;
#   define AnyCast(thetype, theval) std::any_cast<thetype>(theval)
#endif  // CLANG

int main() {
  Any val1 = 1;
  Any val2 = 'a';
  Any val3 = std::string("hello world");

  std::cout << "hello" << std::endl;
  std::cout << "val1 = " << AnyCast(int, val1) << std::endl;
  std::cout << "val2 = " << AnyCast(char, val2) << std::endl;
  std::cout << "val3 = " << AnyCast(std::string, val3) << std::endl;
  // std::cout << (val1 == val2) << std::endl;
}
