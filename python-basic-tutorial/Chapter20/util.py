#-* coding:UTF-8 -*                                                                                                 
#!/usr/bin/env python

def lines(file):
    '''在文件尾部加一行空行'''
    for line in file: yield line
    yield '\n'

def blocks(file):
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []
