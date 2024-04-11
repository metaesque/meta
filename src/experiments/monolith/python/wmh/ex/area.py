#import sys
#import pprint
#pprint.pprint(sys.path)

# See the 'imports' attribute of the 'py_binary' rule for :area.
import wmh.ex

rect = wmh.ex.Rectangle(5,7)
print('Area: %s' % rect.area())
