#include <iostream>
#include <string>
#include <experimental/any>

int main() {
  std::experimental::any val1 = 1;
  std::experimental::any val2 = 'a';
  std::experimental::any val3 = std::string("hello world");

# ifdef CAST
  std::cout << "val1 = " << std::experimental::any_cast<int>(val1) << std::endl;
  std::cout << "val2 = " << std::experimental::any_cast<char>(val2) << std::endl;
  std::cout << "val3 = " << std::experimental::any_cast<std::string>(val3) << std::endl;
  std::cout << (val1 == val2) << std::endl;
# endif  // CAST
}
