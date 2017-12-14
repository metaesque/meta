
class A(object):
  def instance(self):
    pass

  @classmethod
  def Meta(cls):
    pass

  @staticmethod
  def Static():
    pass

def Function():
  pass

lam = lambda a: 1

a = A()

print 'A.instance = %s' % type(a.instance)
print 'A.Meta     = %s' % type(a.Meta)
print 'A.Static   = %s' % type(a.Static)
print 'Function   = %s' % type(Function)
print 'lam        = %s' % type(lam)

