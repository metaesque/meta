class Shape(object):
  def __init__(self):
    pass

  def area():
    raise NotImlementedError()


class Rectangle(Shape):

  def width(self): return self._width
  def height(self): return self._height

  def __init__(self, width, height):
    self._width = width
    self._height = height

  def area(self):
    return self.width() * self.height()
