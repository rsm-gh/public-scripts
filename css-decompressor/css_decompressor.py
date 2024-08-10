#!/usr/bin/python
# -*- coding: utf-8 -*-
#

#
# MIT License
#
#  Copyright (C) 2015-2016, 2018 Rafael Senties Martinelli
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


__version__ = "2018.10.28.1"

_MEASUREMENT_2DIGIT_UNITS = ('em', 'ex', 'px', 'cm', 'mm', 'in', 'pt', 'pc', 'ch', 'vh', 'vw')
_TAB_CHARACTER = "    "


def replace_multiple_spaces(text):
    return ' '.join(text.split())


def inside_closing_brace(start_index, text, end_index=-1):
    if end_index == -1:
        end_index = len(text)

    research_text = text[start_index:end_index]

    if "}" in research_text and "{" not in research_text.split("}", 1)[0]:
        return True

    return False


def format_line_with_left_code_and_right_comment(original_line, comment_separator):
    code_block = original_line.split(comment_separator, 1)[0]
    comment_block = original_line.split(comment_separator, 1)[1]

    code_block = replace_multiple_spaces(code_block)
    new_line = code_block + comment_separator + comment_block + '\n'
    new_line = new_line.replace(';' + comment_separator, '; ' + comment_separator)

    return new_line


def format_line_with_left_comment_and_right_code(original_line, comment_separator):
    comment_block = original_line.split(comment_separator, 1)[0]
    code_block = original_line.split(comment_separator, 1)[1]

    code_block = replace_multiple_spaces(code_block)
    new_line = comment_block + comment_separator + '\n' + code_block

    return new_line


def format_comments_and_spaces(original_text):
    new_text = ""
    inside_comment = False

    for original_line in original_text.split('\n'):

        if '/*' in original_line and '*/' in original_line:  # this will fail if the comment tags are inverted. To be improved.

            if original_line.rsplit('*/', 1)[1].strip() != '':
                new_text += format_line_with_left_comment_and_right_code(original_line, '*/')
            else:
                new_text += format_line_with_left_code_and_right_comment(original_line, '/*')

        elif '/*' in original_line:
            inside_comment = True

            code_text = original_line.split('/*', 1)[0].strip()
            comment_text = original_line.split('/*', 1)[1]

            if code_text == '':

                if new_text[-1:] != '\n':
                    new_text += '\n'

                new_text += original_line + '\n'
            else:
                new_text += code_text + '\n/*' + comment_text + '\n'

        elif inside_comment:

            if '*/' in original_line:
                inside_comment = False

                comment_text = original_line.rsplit('*/', 1)[0]
                code_text = original_line.rsplit('*/', 1)[1].strip()

                if code_text == '':
                    new_text += original_line + '\n\n'
                else:
                    new_text += comment_text + '*/\n' + code_text
            else:
                new_text += original_line + '\n'

        elif '//' in original_line:
            new_text += format_line_with_left_code_and_right_comment(original_line, '//')

        else:

            new_line = original_line

            for char in ('\t', '\n'):
                new_line = new_line.replace(char, '')

            new_line = replace_multiple_spaces(new_line)

            new_text += new_line

    return new_text


def needs_space_before(new_text_last_char, char, chars):
    if new_text_last_char in (' ', ':'):
        return False

    elif char == '#' and chars[-1] == ':':
        return True

    elif char == '.' and not chars[-1].isdigit() and chars[1].isdigit():
        return True

    elif char == '!' and ''.join(chars[x] for x in range(1, 4)) == 'imp':
        return True

    return False


def needs_space_after(char, char_index, chars, text):
    if chars[1] in (';', ' '):
        return False

    elif char in (',', ')'):
        return True

    elif char == ':' and inside_closing_brace(char_index, text):
        return True

    elif char == 's' and chars[-1].isdigit() and not chars[1] + chars[2] == 'ol':
        return True

    elif chars[-1] + char in _MEASUREMENT_2DIGIT_UNITS and chars[-2].isdigit():
        return True

    elif char == 'm' and chars[-3].isdigit() and ''.join(chars[x] for x in range(-2, 1)) == 'rem':
        return True

    elif char in ('n', 'x') and chars[-4].isdigit() and ''.join(chars[x] for x in range(-3, 1)) in ('vmin', 'vmax'):
        return True

    return False


def decompress_css(original_css):
    converted_css = format_comments_and_spaces(original_css)

    new_text = ""
    indent_level = 0
    inside_commented_block = False

    for i, char in enumerate(converted_css):

        #
        #
        #
        chars = {k: '' for k in range(-4, 4)}
        for k in range(-4, 4):
            try:
                chars[k] = converted_css[i + k]
            except Exception:
                pass

        new_text_last_char = new_text[-1:]

        #
        #
        #
        if (char == '/' and chars[1] == '*') or inside_commented_block:
            inside_commented_block = True

            if char == '/' and chars[-1] == '*':
                inside_commented_block = False

        elif char in ('>', '+'):

            if chars[-1] != ' ':
                char = ' ' + char

            if chars[1] != ' ':
                char = char + ' '

        elif needs_space_after(char, i, chars, converted_css):
            char += ' '

        elif needs_space_before(new_text_last_char, char, chars):
            char = ' ' + char

        elif char == '{':

            indent_level += 1

            if new_text_last_char != ' ':
                char = ' {\n'
            else:
                char = '{\n'

        elif char == '}':

            indent_level -= 1

            if new_text_last_char != '\n':
                new_text += '\n'
                new_text_last_char = '\n'

            if chars[1] == '}':
                char = '}\n'
            else:
                char = '}\n\n'

        elif char == ';':

            if chars[2] == '/' and chars[3] == '*':  # code; /* comment */
                pass
            elif chars[2] == '/' and chars[3] == '/':  # code; // comment
                pass
            else:
                char = ';\n'

        if new_text_last_char == '\n':
            new_text += _TAB_CHARACTER * indent_level

        new_text += char

    return new_text


if __name__ == '__main__':
    import sys

    css = sys.stdin.read()
    css = decompress_css(css)
    sys.stdout.write(css)
