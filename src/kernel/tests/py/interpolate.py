#!/Users/wmh/src/wmh/bin/python
import os
import sys
import timeit

def Cat():
  # Interpolate via concatenation
  lstr = 'left'
  rstr = 'right'
  cstr = 'center'
  clen = len(cstr)
  return (
    ('Left %-10s' % lstr) +
    (' Right %10s' % rstr) +
    ' Center ' + (
        cstr[:10] if clen >= 10
        else ((' ' * ((10-clen)/2)) + cstr).ljust(10)) +
    (' int %3d' % 17) +
    (' real %10.5f' % 3.1415926))

def Cat2():
  # Interpolate via concatenation
  lstr = 'left'
  rstr = 'right'
  cstr = 'center'
  clen = len(cstr)
  return (
    'Left ' + lstr.ljust(10) +
    ' Right ' + rstr.rjust(10) +
    ' Center ' + (
        cstr[:10] if clen >= 10
        else ((' ' * ((10-clen)/2)) + cstr).ljust(10)) +
    (' int %3d' % 17) + (' real %10.5f' % 3.1415926))

def Cat3():
  # Interpolate via concatenation, variant 2
  lstr = 'left'
  rstr = 'right'
  cstr = 'center'
  clen = len(cstr)
  return (
    'Left ' + lstr.ljust(10) +
    ' Right ' + rstr.rjust(10) +
    ' Center ' + (
        cstr[:10] if clen >= 10
        else ((' ' * ((10-clen)/2)) + cstr).ljust(10)) +
    # This is slower than ' int %3d' % 17 by 30%.  Is there a more efficient
    # way to convert an int to an aligned string?
    ' int ' + str(17).rjust(3) +
    # This is probably the most efficient way to convert a float (but check
    # if format is faster)
    (' real %10.5f' % 3.1415926))

def Cat4():
  # Interpolate via concatenation, variant 2
  lstr = 'left'
  rstr = 'right'
  cstr = 'center'
  clen = len(cstr)
  return (
    'Left ' + lstr.ljust(10) +
    ' Right ' + rstr.rjust(10) +
    ' Center ' + (
        cstr[:10] if clen >= 10
        else ((' ' * ((10-clen)/2)) + cstr).ljust(10)) +
    # This is slower than ' int %3d' % 17 by 30%.  Is there a more efficient
    # way to convert an int to an aligned string?
    ' int ' + str(17).rjust(3) +
    # This is probably the most efficient way to convert a float (but check
    # if format is faster)
    (' real {0:10.5f}'.format(3.1415926)))


def Percent():
  # Interpolate using %
  lstr = 'left'
  rstr = 'right'
  cstr = 'center'
  clen = len(cstr)
  return (
    'Left %(left)s Right %(right)s Center %(center)s '
    'int %(int)3d real %(real)10.5f' % {
      'left': lstr.ljust(10),
      'right': rstr.rjust(10),
      'center': (
        cstr[:10] if clen >= 10
        else ((' ' * ((10-clen)/2)) + cstr).ljust(10)),
      'int': 17,
      'real': 3.1415926,
    })

def Format():
  # Interpolate using format
  lstr = 'left'
  rstr = 'right'
  cstr = 'center'
  clen = len(cstr)
  return (
    'Left {left} Right {right} Center {center} '
    'int {int:3d} real {real:10.5f}'.format(
      left=lstr.ljust(10),
      right=rstr.rjust(10),
      center=(
        cstr[:10] if clen >= 10
        else ((' ' * ((10-clen)/2)) + cstr).ljust(10)),
      int=17,
      real=3.1415926,
    )
  )

def main():
  args = sys.argv[1:]
  number = int(args[0]) if args else 5000000

  print(Cat())
  print(Cat2())
  print(Cat3())
  print(Cat4())
  print(Percent())
  print(Format())

  first = None
  for func in ('Cat', 'Cat2', 'Cat3', 'Cat4', 'Percent', 'Format'):
    code = '%s()' % func
    seconds = timeit.timeit(
      stmt=code, number=number, setup='from __main__ import %s' % func)
    if first is None:
      first = seconds
      mult = 1.0
    else:
      mult = seconds / first
    print('%-20s = %6.2f (%4.2f)' % (code, seconds, mult))


if __name__ == '__main__':
  main()
