"""Exception classes for the Meta compiler.

IMPORTANT: Classes in this namespace cannot inherit from any class
in meta.root or a BUILD circularity will result (since meta.root.Object
relies on meta.errors).
"""

import meta.errors
# Imports for class Error
# End imports for class Error


class Error(Exception):
  """no docstr"""
  pass


class InvalidType(Error):
  """no docstr"""
  pass


class InvalidConstructId(Error):
  """no docstr"""
  pass


class InvalidAttributeKey(Error):
  """no docstr"""
  pass


class RequiredAttributeValue(Error):
  """no docstr"""
  pass


class InternalError(Error):
  """no docstr"""
  pass


class SyntaxError(Error):
  """no docstr"""
  pass


class Exiting(Error):
  """no docstr"""
  pass


class PrivateMethod(Error):
  """no docstr"""
  pass


class ProtectedMethod(Error):
  """no docstr"""
  pass
