# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# pylint: disable=wildcard-import, redefined-builtin, invalid-name
"""The Relay IR namespace containing the IR definition and compiler."""
import tvm._ffi
from tvm.ir.instrument import pass_instrument

# pylint: disable=unused-argument, import-outside-toplevel
def _debugger_init(expr, stack):
    import pdb

    pdb.set_trace()


@tvm._ffi.register_func("relay.debug")
def _debug(*args):
    import pdb

    pdb.set_trace()


# pylint: disable=unused-argument
@tvm._ffi.register_func("relay.debug_interp")
def _debug_interp(*args):
    _, _, _, ist = args
    print("Relay Debugger")
    print("  You can manipulate the expression under evaluation with the name `expr`.")
    print("  You can manipulate the call stack with the name `stack`.")
    print("--------------")
    print("--------------")
    _debugger_init(ist.current_expr, ist.stack)


@pass_instrument
class PassCounter:
    """Tool to count passes.

    with tvm.transform.PassContext(instruments=[PassCounter()]):
        ...

    Parameters
    ----------
    None

    """

    def __init__(self):
        self._total_cnt = 0
        self._nested = 0

    def run_before_pass(self, mod, info):
        self._nested += 1
        self._total_cnt += 1
        print("{}{} {}".format(self._total_cnt, " " * self._nested, info.name))

    def run_after_pass(self, mod, info):
        self._nested -= 1
