// Executable program to compute area of rectangles.
#include "Rectangle.hh"
#include <string>
#include <iostream>

int main() {
  wmh::ex::Rectangle r1(5, 7);
  std::cout << "Area: " << r1.area() << std::endl;
}
