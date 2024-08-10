# Pure JavaScript Python-Highlighter

Unsatisfied by the quality of the pure JavaScript python highlighters I decided to create one. The code is pretty simple and easy to customize. Enjoy it!

## How to use it?

1) Customize the CSS:

```
.CHpython {background: #d9d9d9}
.CHnumb {color: #9C0000}
.CHwords{color: #008504}
.CHchars {color: #9B26A4}
.CHcwords {color: #6D0D61}
.CHmwords {color: #0016A8}
.CHdcomment {color: #686565}
.CHlcomment1 {color: #7F7A7A}
.CHscomment1 {color: #844D01}
.CHscomment2 {color: #D0C018}
```    	            

2) Create a `<pre>` tag with the python code inside:

```<pre class="CHpython"><code> your code.. </code></pre>```

3) Import python-highlighter.js at the end of the HTML:

`<script src="/static/js/python-highlighter.js"></script>`

4) The python code will be highlighted!

Remarks:

+ The highlighter works in single line/words codes

+ When inserting code it should be valid HTML. The highlighter will work if the HTML is not escaped, but the HTML of the website may fail. At least escape basic characters like ">" or "<".
