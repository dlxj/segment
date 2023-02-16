
import glob
import os
import re

NGram = 5

def NG(strs, NGram):
    strs = re.compile(r'\s').sub(' ', strs)

    def ng(s, n):
        grs = []
        for i in range( len(s) ) :
            if i + n > len(s):
                break
            gr = s[i:i+n]
            grs.append( gr )
        return grs

    gss = []
    for i in range(1, NGram+1):
        gs = ng(strs, i)
        if len(gs) > 0:
            gss += gs
        else:
            break
    return gss

paths = glob.glob('./**/OPS/*.html', recursive=True)

for pth in paths:
    size = os.stat(pth).st_size
    if size < 1024 * 10:
        continue  # 小于 10k 不是正文，跳过
    
    with open(pth, encoding='utf-8-sig') as f:
        data = f.read() #f.readlines()
        lines = re.compile(r'<p>(.+?)<\/p>').findall(data)
        lines = [ re.compile(r'[^\u3007\u4E00-\u9FFF]').sub(' ', line) for line in lines ]
        lines = [ re.compile(r'[\s]+').sub(' ', line) for line in lines ]
        sentences = [ line.split(' ') for line in lines ]
        for ar in sentences:
            for sent in ar:
               ng = NG(sent, NGram)

        a = 1


