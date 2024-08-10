#!/usr/bin/python3

#
# MIT License
#
#  Copyright (C) 2018, 2024 Rafael Senties Martinelli.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import inspect
from datetime import datetime

__version__ = "1.1"


class DebugCodes:
    class Error:
        _color = "\033[1;31m"  # Red
        _value = 0
        _text = "ERROR"

    class Warning:
        _color = "\033[0;93m"  # Light Yellow
        _value = 1
        _text = "WARNING"

    class Info:
        _color = "\033[0;32m"  # Green
        _value = 2
        _text = "INFO"

    class Debug:
        _color = "\033[1;36m"  # Cyan
        _value = 3
        _text = "DEBUG"


if 'PRINT' in os.environ:
    match os.environ['PRINT']:
        case DebugCodes.Error._text:
            _DEBUG = DebugCodes.Error._value
        case DebugCodes.Warning._text:
            _DEBUG = DebugCodes.Warning._value
        case DebugCodes.Info._text:
            _DEBUG = DebugCodes.Info._value
        case DebugCodes.Debug._text:
            _DEBUG = DebugCodes.Debug._value
        case _:
            _DEBUG = DebugCodes.Error._value
else:
    _DEBUG = DebugCodes.Warning._value


def print_error(message: str, direct_output=False) -> None:
    __print_message(message=message,
                    code_type=DebugCodes.Error._value,
                    direct_output=direct_output)


def print_warning(message: str, direct_output=False):
    __print_message(message=message,
                    code_type=DebugCodes.Warning._value,
                    direct_output=direct_output)


def print_info(message: str, direct_output=False):
    __print_message(message=message,
                    code_type=DebugCodes.Info._value,
                    direct_output=direct_output)


def print_debug(message: str = "", direct_output=False):
    __print_message(message=message,
                    code_type=DebugCodes.Debug._value,
                    direct_output=direct_output)


def __print_message(message: str, code_type: int, direct_output: bool) -> None:
    if _DEBUG < code_type:
        return

    if direct_output:
        print(message, flush=True)
        return

    isp1 = inspect.stack()[1]
    module_name = str(inspect.getmodule(isp1[0])).split("from '", 1)[1].split("'>", 1)[0]
    method_name = isp1[3]
    datetime_str = str(datetime.now()).split(".")[0]

    match code_type:

        case DebugCodes.Error._value:
            code_str = DebugCodes.Error._text
            code_col = DebugCodes.Error._color

        case DebugCodes.Warning._value:
            code_str = DebugCodes.Warning._text
            code_col = DebugCodes.Warning._color

        case DebugCodes.Debug._value:
            code_str = DebugCodes.Debug._text
            code_col = DebugCodes.Debug._color

        case DebugCodes.Warning._value:
            code_str = DebugCodes.Warning._text
            code_col = DebugCodes.Warning._color

        case DebugCodes.Info._value:
            code_str = DebugCodes.Info._text
            code_col = DebugCodes.Info._color

        case _:
            code_str = "UNDEFINED"
            code_col = DebugCodes.Warning._color

    message = message.strip()
    if message != "":
        message = "\n" + message

    print('\n{color}{dt} [{code_str}]: "{module_name}" {method_name}\033[0;0m{msg}'.format(color=code_col,
                                                                                           dt=datetime_str,
                                                                                           code_str=code_str,
                                                                                           module_name=module_name,
                                                                                           method_name=method_name,
                                                                                           msg=message), flush=True)


if __name__ == '__main__':
    _DEBUG = DebugCodes.Debug._value
    print_error('this is ERROR')
    print_warning('this is WARNING')
    print_info("this is INFO")
    print_debug('this is DEBUG')

    def test():
        print_debug()

    test()

    __print_message("this is UNDEFINED", -1, False)
