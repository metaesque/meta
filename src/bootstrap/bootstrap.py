import collections
import os
import platform
import pprint
import re
import requests   # must ensure this is installed!
import shutil
import subprocess
import sys
import tempfile


def ValidPath(path):
  # Expand env.vars.
  epath = re.sub(r'\$([a-zA-Z_]+)', lambda m: os.getenv(m.group(1), ''), path)
  result = os.path.exists(epath)
  if not result:
    print('WARN: %s does not exist' % path)
  return result


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
    'desc': 'The path of the python2 executable.',
    'default': '/usr/bin/python',
    'type': ValidPath,
  }),
  ('cpp_compiler', {
    'desc': 'The compiler to use for C++.',
    'default': '/usr/bin/g++',
    'type': ValidPath,
  }),
])

def CreateConfig(src_root, bazel_path):
  # Create the ~/.config/metaxy/config.meta file.
  #  - VARS specifies the variables for which values are required, along
  #    with a description, default value, and value validator.
  #  - If the destination file exists, the value of each var defined within
  #    that file is used as an initial default, with VARS[var]['default']
  #    only used for vars that do not have a value in config.meta.
  #  - vars in config.meta not defined in VARS are ignored and not written
  #    to the new version.

  # This relies on SetupBootstrap() having already been invoked to ensure that
  # metastrap is in PYTHONPATH.
  import metastrap

  # Establish (default) config path.
  config_path = metastrap.ConfigPath()
  if not os.path.exists(config_path):
    # This is the very first setup ... make an initial version of config.meta.
    tmpl_path = config_path + '.tmpl'
    if os.path.exists(tmpl_path):
      with open(tmpl_path, 'r') as ifp:
        with open(config_path, 'w') as ofp:
          for line in ifp:
            line = re.sub(
              r'var src_root = (\S+)', 'var src_root = ' + src_root, line)
            ofp.write(line)
    else:
      print('ERROR: Failed to find %s or %s' % (config_path, tmpl_path))

  # Establish the config path and parse it into key/value pairs.
  config = metastrap.Config()
  if config_path != config['config_path']:
    print(
      'ERROR: Mismatch between %s and %s' % (config_path, config['config_path']))
    sys.exit(1)

  # Set the src_root and bazel_path
  config['src_root'] = src_root
  config['bazel'] = bazel_path

  # We will write to a tmp file, and move the tmp file to destination if no
  # errors occur.
  new_path = config_path + '.new'

  # Interactive obtain values for each var in VARS.
  ifp = sys.stdin
  ofp = sys.stdout
  with open(new_path, 'w') as cfp:
    for var, data in VARS.iteritems():
      dlines = data['desc'].split('\n')
      ofp.write('\n')
      ofp.write('%s:\n' % var)
      for dline in dlines:
        ofp.write('  ' + dline + '\n')

      default_value = config.get(var, data['default'])

      while True:
        ofp.write('value [%s]: ' % default_value)
        ans = ifp.readline()
        if ans == '':
          # EOF
          sys.exit(1)
        elif ans == '\n':
          ans = default_value
        else:
          ans = ans.strip()
        typecheck = data.get('type', None)
        if typecheck and not typecheck(ans):
          print('ERROR: "%s" is invalid for var %s' % (ans, var))
        else:
          break

      # Write the result to our tmp file.
      cfp.write('\n')
      cfp.write('var %s = %s #:\n' % (var, ans))
      for dline in dlines:
        cfp.write('  ' + dline + '\n')
      cfp.flush()

  # Move tmpfile to destination file.
  if os.path.exists(new_path):
    shutil.copyfile(config_path, config_path + '.old')
    shutil.copyfile(new_path, config_path)
    os.unlink(new_path)

  config = metastrap.Config()
  return config


def InstallBazel():
  # Establish the latest version of bazel.

  # Where the bazel executable should be installed
  print('Please specify the path within which to install bazel. You can use')
  print('environment variables in the path.')
  default_install_dir = os.path.join(os.getenv('HOME'), 'bin')
  install_dir = os.path.expandvars(
    raw_input('Path [%s]: ' % default_install_dir) or default_install_dir)

  # Download the releases page
  github_bazel_releases = 'https://github.com/bazelbuild/bazel/releases'
  r = requests.get(github_bazel_releases)
  version = None
  if not r.ok:
    print('ERROR: Failed to download %s' % github_bazel_releases)
    sys.exit(1)

  # Extract the latest version from the page.
  m = re.search(r'/bazelbuild/bazel/tree/([\d.]+)', r.text)
  if not m:
    print(r.text)
    print('ERROR: Failed to obtain bazel version from %s' % github_bazel_releases)
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
    executable = os.path.join(install_dir, 'bazel')
  elif system == 'Linux':
    # Alternatively we could use yum (prompt user?)
    # TODO(wmh): Must install prereqs:
    #  % sudo apt-get install pkg-config zip g++ zlib1g-dev unzip python
    base = 'bazel-%s-installer-linux-x86_64.sh' % version
    url += base
    installer = os.path.join(tmpdir, base)
    executable = os.path.join(install_dir, 'bazel')
  elif system == 'Windows':
    # This is different than mac and linux ... executable binary, not bash script.
    base = 'bazel-%s-windows-x86_64.exe' % version
    url += base
    executable = os.path.join(tmpdir, base)
    installer = None
  else:
    print('ERROR: Do not know how to install bazel on %s' % system)
    sys.exit(1)

  print('system = %s' % system)
  print('url = %s' % url)
  print('executable = %s' % executable)
  print('installer = %s' % installer)

  # Download the bazel installer/executable.
  subprocess.check_output(['curl', '-L', '-O', url], cwd=tmpdir)

  # Install
  if installer:
    os.chmod(installer, 0755)
    args = [
      installer,
      os.path.expandvars('--base=$HOME/.bazel'),
      os.path.expandvars('--bin=%s' % install_dir)
    ]
    print('Command: %s' % ' '.join(args))
    subprocess.check_output(args)

  # Verify executable
  if not os.path.exists(executable):
    print('ERROR: Failed to obtain %s' % executable)
    sys.exit(1)
  return executable


def SetupBootstrap(src_root):
  """Ensure that, for each baselang, we can bootstrap Meta."""
  # In python, metastrap.py must be discoverable.
  pp = os.environ.get('PYTHONPATH', '')
  paths = []
  if pp:
    for pstr in pp.split(':'):
      paths.append(os.path.realpath(pstr))
  while True:
    default_pdir = os.path.expandvars('$HOME/src/$USER/lib/python')
    pdir = (
      raw_input('Preferred path for python libraries [%s]: ' % default_pdir) or
      default_pdir)
    python_dir = os.path.realpath(os.path.expandvars(pdir))
    if python_dir in paths:
      break
    print('ERROR: %s not in PYTHONPATH' % python_dir)

  metastrap_path = os.path.join(src_root, 'lib', 'metastrap.py')
  full_path = os.path.join(python_dir, 'metastrap.py')
  if not os.path.exists(metastrap_path):
    print('ERROR: Failed to find %s' % metastrap_path)
    sys.exit(1)
  elif os.path.exists(full_path):
    if os.path.islink(full_path) and os.readlink(full_path) == metastrap_path:
      # We are all set up
      print('NOTE: confirmed %s -> %s' % (full_path, metastrap_path))
    else:
      print('ERROR: %s exists' % full_path)
      sys.exit(1)
  else:
    print('src %s link %s' % (metastrap_path, full_path))
    os.symlink(metastrap_path, full_path)

def ExtractCode(src_root):
  # In $src_root/lib/versions, 'current' should be a symlink to another
  # local dir. If the child dir doesn't exist, there should be a .tgz version.
  # Extract.
  vdir = os.path.join(src_root, 'lib', 'versions')
  if not os.path.isdir(vdir):
    raise Error('Failed to find %s' % vdir)
  current = os.path.join(vdir, 'current')
  if not os.path.islink(current):
    raise Error('Expecting %s to be a symlink' % vdir)
  link = os.readlink(current)
  cdir = os.path.join(vdir, link)
  if os.path.exists(cdir):
    print('TRUE: %s exists' % cdir)
  else:
    # We require link to start with 'v' and end with '.00'
    assert link.startswith('v') and link.endswith('.00')
    # Obtain the .tgz file (strip off .00)
    tgzpath = cdir[:-3] + '.tgz'
    if not os.path.exists(tgzpath):
      raise Error('ERROR: Failed to find %s' % tgzpath)
    # Extract the tar file
    print('NOTE: Extracting %s into %s' % (tgzpath, vdir))
    cmd = 'tar xzf %s' % tgzpath
    print('CMD: %s' % cmd)
    subprocess.check_output(cmd, cwd=vdir, shell=True)
    basedir = tgzpath.replace('.tgz', '')
    assert os.path.exists(basedir), basedir
    basedir_00 = basedir + '.00'
    if not os.path.exists(basedir_00):
      base00_name = os.path.basename(basedir_00)
      subprocess.check_output(
        'ln -s %s %s' % (os.path.basename(basedir), base00_name),
        cwd=vdir, shell=True)
      print('NOTE: Linked %s to %s' % (basedir, base00_name))
  assert os.path.exists(current), current


def BuildMeta(src_root):
  os.system('pip install future')
  os.system('pip3 install future')
  kdir = os.path.join(src_root, 'src', 'kernel')

  # Execute metac a first time (lots of warnings/errors are printed as various
  # dependencies are not present, so we do not show the output.
  command = (
    'python ../bootstrap/metac.py --meta_version=current *.meta ../lib/*.meta')
  print('COMMAND: cd %s; %s' % (kdir, command))
  out, err = subprocess.Popen(
    command, cwd=kdir, shell=True,
    stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

  # Now execute a similar command, using the 'metac' binary.
  command = 'metac *.meta ../lib/*.meta'
  print('COMMAND: cd %s; %s' % (kdir, command))
  out, err = subprocess.Popen(
    command, cwd=kdir, shell=True,
    stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
  print(out)
  print(err)


def main():
  default_src_root = os.path.expandvars('$HOME/src/meta')
  src_root = raw_input(
    'Directory containing local Meta github client [%s]: ' % default_src_root
  ) or default_src_root
  src_root = os.path.expandvars(src_root)
  if not os.path.exists(src_root):
    print('%s does not exist.' % src_root)
    print('')
    print('Download Meta with:')
    print(' % cd <somedir>')
    print(' % git clone https://github.com/metaesque/meta.git meta')
    sys.exit(1)

  # Ensure we can compile meta code using --meta_version=current
  ExtractCode(src_root)

  # Ensure that, for each baselang, the Meta bootstrapping functionality is
  # discoverable.
  SetupBootstrap(src_root)

  # Install bazel.
  #  - https://docs.bazel.build/versions/master/install.html
  bazel_path = InstallBazel()

  # Create the $HOME/.config/metaxy/config.meta file
  config = CreateConfig(src_root, bazel_path)
  # pprint.pprint(config)

  # Build Meta
  BuildMeta(src_root)


if __name__ == '__main__':
  main()
