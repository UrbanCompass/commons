# ==================================================================================================
# Copyright 2011 Twitter, Inc.
# --------------------------------------------------------------------------------------------------
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this work except in compliance with the License.
# You may obtain a copy of the License in the LICENSE file, or at:
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==================================================================================================

from __future__ import print_function

import os
import sys

from twitter.common.collections import OrderedSet
from twitter.common.python.pex import PEX

from twitter.pants.base import Target, Address
from twitter.pants.python.python_chroot import PythonChroot

def can_import(module_name):
  try:
    exec 'import ' + module_name
    return True
  except ImportError:
    return False

LINT_TOOLS = {
  'pylint': {
    'entry_point': 'pylint.lint',
    'interpreter_args': ['--rcfile=%s' % os.path.join(
      '%(root_dir)s', 'build-support', 'pylint', 'pylint.rc')],
    'lint_target': '3rdparty/python:pylint',
    'module_name': 'pylint',
  },
  'pyflakes': {
    'entry_point': 'pyflakes.__main__',
    'interpreter_args': [],
    'lint_target': '3rdparty/python:pyflakes',
    'module_name': 'pyflakes',
  },
  'flake8': {
    'entry_point': 'flake8.run',
    'interpreter_args': [],
    'lint_target': '3rdparty/python:flake8',
    'module_name': 'flake8',
  },
}

class PythonLintBuilder(object):
  def __init__(self, tool_name, targets, args, root_dir, conn_timeout=None):
    self._tool_name = tool_name
    assert self._tool_name in LINT_TOOLS
    self._opts = LINT_TOOLS[self._tool_name]
    self.targets = targets
    self.args = args
    self.root_dir = root_dir
    self._conn_timeout = conn_timeout

  def run(self):
    if not can_import(self._opts['module_name']):
      print('ERROR: %s not found!  Skipping.' % self._tool_name, file=sys.stderr)
      return 1
    return self._run_lints(self.targets, self.args)

  def _run_lint(self, target, args):
    lint_target = Target.get(Address.parse(self.root_dir, self._opts['lint_target']))
    assert lint_target, 'Could not find target %r' % self._opts['lint_target']
    chroot = PythonChroot(target, self.root_dir, extra_targets=[lint_target],
      conn_timeout=self._conn_timeout)
    chroot.builder.info().ignore_errors = True
    builder = chroot.dump()
    builder.info().entry_point = self._opts['entry_point']
    builder.info().run_name = 'main'
    builder.freeze()

    interpreter_args = self._opts['interpreter_args']
    interpreter_args.extend(args or [])
    sources = OrderedSet([])
    target.walk(lambda trg: sources.update(
      trg.sources if hasattr(trg, 'sources') and trg.sources is not None else []))
    pex = PEX(builder.path())
    pex.run(args=interpreter_args + list(sources), with_chroot=True)

  def _run_lints(self, targets, args):
    for target in targets:
      self._run_lint(target, args)
    return 0
