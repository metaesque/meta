import sys
print('Here in nm/__init__.py with relevant modules:')
for mod in sorted(sys.modules):
  if mod.startswith('nm'):
    print('  ' + mod)

