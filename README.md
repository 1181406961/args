<p>Python实现clean code中的Command-Line Argument Parser练习。(需要python3.8及以上版本)<p>
<p>自己实现命令行参数解析，简单来说就是解析一个字符串数组。<p>
<p>例如:  -l -p 8080 -d /usr/logs　</p>
<p>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp“l”（日志）没有相关的值，它是一个布尔标志，如果存在则为 true，不存在则为 false。</p>
<p>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp“p”（端口）有一个整数值，“d”（目录）有一个字符串值。</p>
<p>标志后面如果存在多个值，则该标志表示一个列表，例如：　-g this is a list -d 1 2 -3 5</p>
<p>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp"g"表示一个字符串列表[“this”, “is”, “a”, “list”]，“d"标志表示一个整数列表[1, 2, -3, 5]</p>
<p>如果参数中没有指定某个标志，那么解析器应该指定一个默认值。例如，false 代表布尔值，0 代表数字，”"代表字符串，[]代表列表。如果给出的参数与模式不匹配，重要的是给出一个好的错误信息，准确地解释什么是错误的。　确保你的代码是可扩展的，即如何增加新的数值类型是直接和明显的。</p>
   
    
