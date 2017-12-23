#include <iostream>
#include <string>
#include <any>

int main() {
  std::any val1 = 1;
  std::any val2 = 'a';
  std::any val3 = std::string("hello world");

  std::cout << "hello" << std::endl;
  std::cout << "val1 = " << std::any_cast<int>(val1) << std::endl;
  std::cout << "val2 = " << std::any_cast<char>(val2) << std::endl;
  std::cout << "val3 = " << std::any_cast<std::string>(val3) << std::endl;
  // std::cout << (val1 == val2) << std::endl;
}
