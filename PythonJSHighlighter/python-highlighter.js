
/*
 *
 * MIT License
 *
 * Copyright (C) 2015-2016  Rafael Senties Martinelli. 
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
*/

/* Version 2016.06.01 */

"use strict";

/*
function color_lines(text) {
    
    // This stills experimental, there are some bugs like when using
    // comments of multiple lines
    var new_text = '';
    var lines = text.split('<br>');
    var lines_length = lines.length;
    
    for (var l = 0; l < lines_length; l++) {

        if (l % 2 == 0) {           
            line_class = 'CHodd'
        }else {
            line_class = 'CHeven'
        };           
        
        new_text += '<div class="'+line_class+'">'+lines[l]+'</div>'        
    };
    return new_text;
};*/


(function(){
    
    const special_chars = [
    	'!=', '&lt;', '&gt;', '-=', '+=', '==',
        '=',    ';',   '//',  '/',  '.',  '^',
        '**',    '*',    ':', '()',  '(',  ')',
        ',',   '[]',    '[',  ']', '{}',  '{',
        '}',    '+', '-',
    ];
    
    // https://docs.python.org/3/library/functions.html
    const built_in_functions=[
        'abs',         'dict',         'help',         'min',       'setattr',
        'all',         'dir',          'hex',          'next',      'slice',
        'any',         'divmod',       'id',           'object',    'sorted',
        'ascii',       'enumerate',    'input',        'oct',       'staticmethod',
        'bin',         'eval',         'int',          'open',      'str',
        'bool',        'exec',         'isinstance',   'ord',       'sum',
        'breakpoint',
        'bytearray',   'filter',       'issubclass',   'pow',       'super',
        'bytes',       'float',        'iter',         'print',     'tuple',
        'callable',    'format',       'len',          'property',  'type',
        'chr',         'frozenset',    'list',         'range',     'vars',
        'classmethod', 'getattr',      'locals',       'repr',      'zip',
        'compile',     'globals',      'map',          'reversed',  '__import__',
        'complex',     'hasattr',      'max',          'round',    
        'delattr',     'hash',         'memoryview',   'set',
    ];

    // https://docs.python.org/3/reference/simple_stmts.html
    const simple_statements=['assert','pass','del','return','yield','raise','break','continue','import','global','nonlocal'];
 
    // https://docs.python.org/3/reference/compound_stmts.html
    const compound_statements=['if','while','for','try','with','async','else','elif'];

    // https://www.programiz.com/python-programming/keywords-identifier
    var keywords=['False','None','True','and','as','class','def','except', 'finally', 'from', 'in', 'is', 'lambda', 'not', 'or', 'as','self','exit'];
 
    const special_words = built_in_functions.concat(simple_statements).concat(compound_statements).concat(keywords);
	
	const special_chars_length = special_chars.length;
	const special_words_length = special_words.length;       
    
    const pre_zones = document.getElementsByClassName('CHpython');
    
     for (var p = 0; p < pre_zones.length; p++) {
        
        const pre = pre_zones[p];
        const codes = pre.getElementsByTagName('code');
        
        if (codes.length > 0) {     
            var text = codes[0].innerHTML
        }else{
            var text = pre.innerHTML
        };

        var lines = text.split(/\r?\n/);
        var lines_length = lines.length;     
        var new_text = "";
        var append_line = '';
                
        
        for (var l = 0; l < lines_length; l++) {
            
                
            var line = lines[l];

            var words = line.split(/(\s+|\"\"\"|\'\'\'|\"\"|\'\'|\=\=|\=|\\t|'|"|\.|,|\:|\!\=|\-\=|\^|\+\=|\+|\-|\/|\(\)|\(|\)|\[]|\[|\]|\{}|\{|\}|\*)/);
            var new_line = '';
            var appended_word = '';
            var definition = false;
            
            words_loop: for (var w = 0; w < words.length; w++) {
                var word = words[w];
                if (word.trim() == "") {
                    new_line += word;
                    continue words_loop;
                    
                } else if (append_line != '') {
                    if (word == append_line) {
                        append_line = '';
                        new_line += word + '</span>';
                    } else {
                        new_line += word
                    };

                } else {

                    if (word == '"""' && append_line == '') {
                        new_line += '<span class="CHlcomment1">' + word;
                        append_line = word;
                        
                    } else if (word == "'''" && append_line == '') {
                        
                        new_line += '<span class="CHlcomment2">' + word;
                        append_line = word;
                        
                    } else if (appended_word != '') {
                        if (word == appended_word) {
                            new_line += word + '</span>';
                            appended_word = '';
                        } else {
                            new_line += word
                        };
                    } else if (append_line == 0) {
                        
                        if (word.charAt(0) == '#') {
                            new_line += '<span class="CHdcomment">';
                            for (var k = w; k < words.length; k++) {
                                new_line += words[k];
                            };
                            new_line += '</span>';
                            break;
                            
                        } else if (word == '""'){ 
                            new_line += '<span class="CHscomment2">' + word;
                            
                        } else if (word == '"') {
                            new_line += '<span class="CHscomment2">' + word;
                            appended_word = word;
                            
                        } else if (word == "'") {
                            new_line += '<span class="CHscomment1">' + word;
                            appended_word = word;
                            
                        } else if (word == 'def') {
                            new_line += '<span class="CHwords">' + word + '</span><span class="CHmwords">';
                            definition = true;
                            
                        } else if (word == 'class') {
                            new_line += '<span class="CHwords">' + word + '</span><span class="CHcwords">';
                            definition = true;
                            
                        } else {
                            if (word == "(" && definition == 1) {
                                definition = false;
                                new_line += '</span><span class="CHchars">(</span>';
                                continue words_loop;
                                
                            } else if (isNaN(word) == false) {
                                new_line += '<span class="CHnumb">' + word + '</span>';
                                continue words_loop;
                            };
                            
                            for (var i = 0; i < special_chars_length; i++) {
                                                                
                                if (word == special_chars[i]) {
                                    new_line += '<span class="CHchars">' + word + '</span>';
                                    continue words_loop;
                                }
                            };
                            
                            for (var i = 0; i < special_words_length; i++) {
                                                                
                                if (word == special_words[i]) {
                                    new_line += '<span class="CHwords">' + word + '</span>';
                                    continue words_loop;
                                }
                            };
                            new_line += word;
                        };
                    };
                };
            };
                        
                                    
            
            if (new_line == '') {
                // this is for valid html. There should not be empty divs
                new_line += '&nbsp;'
            };       

            if (appended_word != '' || definition == true) {
                new_line += '</span>'
            };

            new_text += new_line +'<br>'
            
        };
        pre.innerHTML = '<code>'+new_text+'</code>'
    };
})();
