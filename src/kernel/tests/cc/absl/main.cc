#include <iostream>
#include "absl/strings/str_join.h"
#include "absl/strings/str_format.h"

int main(int argc, char**argv) {
  // std::cout << "Hello World" << std::endl;
  absl::PrintF("Hello %s\n", "World");
}
