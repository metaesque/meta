import collections
import os
import platform
import re
import requests   # must ensure this is installed!
import subprocess
import sys
import tempfile


def ValidPath(path):
  # Expand env.vars.
  epath = re.sub(r'\$([a-zA-Z_]+)', lambda m: os.getenv(m.group(1), ''), path)
  return os.path.exists(epath)


VARS = collections.OrderedDict([
  ('default_metalang', {
    'desc': 'The default metalang (when -L aka --metalang is not specified)',
    'default': 'oopl',
  }),
  ('default_baselang', {
    'desc': (
      'The default baselang (when -b aka --baselang is not specified).\n'
      'Note that this is only used when metalang matches default_metalang.'),
    'default': 'python',
  }),
  ('version', {
    'desc': (
      'Which version of the Meta source code to use.  This can be one of\n'
      "'beta', 'current', 'stable', or an explicit version like v0.7.5.59"),
    'default': 'current',
    'type': lambda s: bool(re.match('^(beta|current|stable|v[\d+.]+)$', s)),
  }),
  ('src_root', {
    'desc': 'The path of where Meta has been installed on this computer.',
    'default': '$HOME/src/meta',
    'type': ValidPath,
  }),
  ('repository_path', {
    'desc': 'The path wherein all Meta-generated code will be written.',
    'default': '$HOME/lib/meta',
    'type': ValidPath,
  }),
  ('bazel', {
    'desc': 'The path of the bazel executable.',
    'default': '$HOME/bin/bazel',
    'type': ValidPath,
  }),
  ('python', {
    'desc': 'The path of the python executable.',
    'default': '/usr/bin/python',
    'type': ValidPath,
  }),
  ('cpp_compiler', {
    'desc': 'The compiler to use for C++.',
    'default': '/usr/bin/g++',
    'type': ValidPath,
  }),
])


def CreateConfig(outpath):

  ifp = sys.stdin
  ofp = sys.stdout
  lines = []
  for var, data in VARS.iteritems():
    dlines = data['desc'].split('\n')
    ofp.write('\n')
    ofp.write('%s:\n' % var)
    for dline in dlines:
      ofp.write('  ' + dline + '\n')

    while True:
      ofp.write('value [%s]: ' % data['default'])
      ans = ifp.readline()
      if ans == '':
        # EOF
        sys.exit(1)
      elif ans == '\n':
        ans = data['default']
      else:
        ans = ans.strip()
      typecheck = data.get('type', None)
      if typecheck and not typecheck(ans):
        print 'ERROR: "%s" is invalid for var %s' % (ans, var)
      else:
        break

    if lines:
      lines.append('')
    lines.append('var %s = %s #:' % (var, ans))
    for dline in dlines:
      lines.append('  ' + dline)

  with open(outpath, 'w') as cfp:
    for line in lines:
      cfp.write(line + '\n')

def InstallBazel():
  # Establish the latest version of bazel.

  # Download the releases page
  github_bazel_releases = 'https://github.com/bazelbuild/bazel/releases'
  r = requests.get(github_bazel_releases)
  version = None
  if not r.ok:
    print 'ERROR: Failed to download %s' % github_bazel_releases
    sys.exit(1)

  # Extract the latest version from the page.
  m = re.search(r'/bazelbuild/bazel/tree/([\d.]+)', r.text)
  if not m:
    print r.text
    print 'ERROR: Failed to obtain bazel version from %s' % github_bazel_releases
    sys.exit(1)
  version = m.group(1)

  # Create temp dir to write to.
  tmpdir = tempfile.mkdtemp()

  # Establish which release url to use based on platform.
  system = platform.system()
  url = 'https://github.com/bazelbuild/bazel/releases/download/%s/' % version
  if system == 'Darwin':
    # Alternatively we could use brew (prompt user?)
    # TODO(wmh): Must ensure xcode is installed and that license is accepted
    #  % sudo xcodebuild -license accept
    base = 'bazel-%s-installer-darwin-x86_64.sh' % version
    url += base
    installer = os.path.join(tmpdir, base)
    executable = os.path.join(os.getenv('HOME'), 'bin', 'bazel')
  elif system == 'Linux':
    # Alternatively we could use yum (prompt user?)
    # TODO(wmh): Must install prereqs:
    #  % sudo apt-get install pkg-config zip g++ zlib1g-dev unzip python
    base = 'bazel-%s-installer-linux-x86_64.sh' % version
    url += base
    installer = os.path.join(tmpdir, base)
    executable = os.path.join(os.getenv('HOME'), 'bin', 'bazel')
  elif system == 'Windows':
    # This is different than mac and linux ... executable binary, not bash script.
    base = 'bazel-%s-windows-x86_64.exe' % version
    url += base
    executable = os.path.join(tmpdir, base)
    installer = None
  else:
    print 'ERROR: Do not know how to install bazel on %s' % system
    sys.exit(1)

  print 'system = %s' % system
  print 'url = %s' % url
  print 'executable = %s' % executable
  print 'installer = %s' % installer

  # Download the bazel installer/executable.
  subprocess.check_output(['curl', '-L', '-O', url], cwd=tmpdir)

  # Install
  if installer:
    os.chmod(installer, 0755)
    subprocess.check_output([installer, '--user'])

  # Verify executable
  if not os.path.exists(executable):
    print 'ERROR: Failed to obtain %s' % executable
    sys.exit(1)


def main():

  # Create the $HOME/.config/metaxy/config.meta file
  if False:
    config_dir = os.path.join(os.getenv('HOME'), '.config', 'metaxy')
    if not os.path.exists(config_dir):
      print 'Note: created %s' % config_dir
      os.makedirs(config_dir, 0700)
    config_path = os.path.join(config_dir, 'config.meta')
    if os.path.exists(config_path):
      print 'WARNING: %s already exists\nWARNING: (nothing done, delete to recreate)' % config_path
    else:
      CreateConfig(config_path)

  # Install bazel.
  #  - https://docs.bazel.build/versions/master/install.html
  InstallBazel()

if __name__ == '__main__':
  main()
