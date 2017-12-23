#include <iostream>
#include <any>

int main() {
  std::any val1 = 1;
  std::cout << "val1 = " << std::any_cast<int>(val1) << std::endl;
}
