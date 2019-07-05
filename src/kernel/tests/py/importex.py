# Experiment with how to provide access to nm.sp.A within nm.sp using
# either A or nm.sp.A.
import sys
sys.path.insert(0, '.')

# Note that in importing nm.sp.ace, nm/__init__.py is executed, then
# nm/sp/__init__.py is executed, then nm/sp/ace/__init__.py is executed.
import nm.sp.ace

