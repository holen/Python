#-* coding:UTF-8 -*
#!/usr/bin/env python

import re

text = "There is 1 data 10/15/99 in here!"
print text

# match() 从字符串的起始匹配一个模式
m = re.match(".*(\d{2})/(\d{2})/(\d{2,4}).*", text)

# repr() 转化为供解释器读取的形式, 对Pyhon比较友好
if m: print repr("."), "=>", repr(m.group(1, 2, 3))

# search() 在字符串内查找模式匹配
n = re.search("(\d{1,2})/(\d{1,2})/(\d{2,4})", text)
print n.group(1), n.group(2), n.group(3)

# sub() 使用另一个字符串代替匹配模式
# To match a literal backslash, one might have to write '\\\\' as the pattern string 
print re.sub("/", "-", text)

#findall() matches all occurrences of a pattern, not just the first one as search() does. 
text = "He was carefully disguised but captured quickly by police."
print re.findall(r"\w+ly", text)
# return ['carefully', 'quickly']


