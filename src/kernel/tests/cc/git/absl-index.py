#!/usr/local/bin/python3
"""Create an index of methods defined in Abseil.

Assumes one has invoked
 % git clone https://github.com/abseil/abseil-cpp.git
in current directory.
"""
import os
import re
import subprocess
import sys

MCRE = re.compile(
  r'^\s*// '
  r'(?:Function Template:\s*)?'
  r'(?P<name>[a-zA-Z0-9_]+)'
  r'(?:<(?P<tmpl>.*)>\s*)?'
  r'\((?P<params>.*)\)'
  r'(?P<rest>.*)')
CRE = re.compile('^\s*// ?(?P<line>.*)')

def HtmlSafe(val):
  return val.replace('<', '&lt;').replace('>', '&gt;')

def ParseFile(path):
  """Parse function names and comments from a .h path.

  Returns mapping from function name to comment.
  """
  result = {}
  with open(path, 'r') as fp:
    lines = fp.readlines()
    i = 0
    n = len(lines)
    while i < n:
      line = lines[i]
      m = MCRE.match(line)
      if m and not m.group('rest') and not m.group('params'):
        # Looks like a function definition. Consume all adjacent following
        # comment lines.
        name = m.group('name')
        tmpl = m.group('tmpl')
        params = m.group('params')
        if tmpl is not None:
          name += '<%s>' % tmpl
        if params is not None:
          name += '(%s)' % params
        # print '%3d: %s' % (i+1, m.groupdict())
        comments = []
        i += 1
        while i < n:
          m = CRE.match(lines[i])
          if not m: break
          comments.append(m.group('line'))
          i += 1
        result[name] = comments
      else:
        i += 1
  return result

def main():
  args = sys.argv[1:]
  rootdir = './abseil-cpp/absl'
  text = subprocess.check_output(['find', '.', '-name', '*.h'], cwd=rootdir)
  paths = {}
  for path in text.strip().split('\n'):
    assert path.startswith('./')
    path = path[2:]
    fullpath = os.path.join(rootdir, path)
    paths[path] = ParseFile(fullpath)

  # Create html file.
  gitroot = 'https://github.com/abseil/abseil-cpp/tree/master/absl'
  outpath = './absl.html'
  with open(outpath, 'w') as fp:
    fp.write('<html>\n')
    fp.write(' <head>\n')
    fp.write('  <style>\n')
    fp.write('   body {\n')
    fp.write('     color: white;\n')
    fp.write('     background-color: black;\n')
    fp.write('   }\n')
    fp.write('   .file {\n')
    fp.write('     border: 1px solid black;\n')
    fp.write('     width: 650px;\n')
    fp.write('     padding: 10px;\n')
    fp.write('     margin: 10px auto;\n')
    fp.write('     color: black;\n')
    fp.write('     background-color: white;\n')
    fp.write('   }\n')
    fp.write('   .func {\n')
    fp.write('     color: black;\n')
    fp.write('     background-color: #E5E5E5;\n')
    fp.write('     border: 1px solid black;\n')
    fp.write('     margin: 10px;\n')
    fp.write('     padding: 10px;\n')
    fp.write('   }\n')
    fp.write('  </style>\n')
    fp.write(' </head>\n')
    fp.write(' <body>\n')

    for path in sorted(paths):
      decls = paths[path]
      if not decls: continue
      fp.write('\n')
      fp.write('  <div class="file">\n')
      fp.write('   <h2>%s</h2>\n' % path)
      fp.write(
        '   <p><a href="%s/%s" target="git">git</a></p>\n' % (gitroot, path))
      for name in sorted(decls):
        comments = decls[name]
        fp.write('\n')
        fp.write('   <div class="func">\n')
        fp.write('    <h3>%s</h3>\n' % HtmlSafe(name))
        fp.write('    <pre><code>\n')
        text = '\n'.join(comments).strip()
        text = HtmlSafe(text)
        fp.write(text + '\n')
        fp.write('    </code></pre>\n')
        fp.write('   </div>\n')
      fp.write('\n')
      fp.write('  </div>\n')

    fp.write('\n')
    fp.write(' </body>\n')
    fp.write('</html>\n')

if __name__ == '__main__':
  main()
