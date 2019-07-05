import sys
print('Here in nm/sp/ace/__init__.py with relevant modules:')
for mod in sorted(sys.modules):
  if mod.startswith('nm'):
    print('  ' + mod)

class A(object):
  def __init__(self):
    pass

# Now, can we refer to class 'A' as both 'A' and 'nm.sp.ace.A'?
a = A

# Note that 'nm.sp.ace' does exist in sys.modules
b = sys.modules[__name__].A
assert a is b

# By default, 'nm.sp.ace.A' is available until AFTER nm/sp/ace/__init__.py
# finishes loading, so within nm/sp/ace/__init__.py it is not legal.
try:
  # We cannot refer to class A by its fully qualified name 'nm.sp.ace.A'
  # within nm/sp/ace/__init__.py. That is unfortunate!
  c = nm.sp.ace.A
  assert a is c
except NameError as e:
  print('Warning: Failed to reference nm.sp.A within nm.sp [%s]' % e)

# Note that 'nm', 'nm.sp' and 'nm.sp.ace' all exist in sys.modules, but
# 'sp' is not yet added to 'nm', and 'ace' is not yet added to 'nm.sp'.
# So, to allow nm.sp.ace.A to be legal within nm/sp/ace/__init__.py, we
# need only insert sp into nm and ace in nm.sp.
nm = sys.modules['nm']
setattr(nm, 'sp', sys.modules['nm.sp'])
setattr(nm.sp, 'ace', sys.modules['nm.sp.ace'])
d = nm.sp.ace.A
assert a is d
print('Success!')



