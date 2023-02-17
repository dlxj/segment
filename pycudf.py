
# https://docs.rapids.ai/api/cudf/stable/user_guide/10min.html 教程

# import cudf, requests
# from io import StringIO

# df = cudf.DataFrame(
#     {
#         "a": list(range(21)),
#         "b": list(reversed(range(20))),
#         "c": list(range(20)),
#     }
# )

# print(df)

import glob
import os
import re


# 所有连续 N 个字，和它出现的总次数
dic_NGrams = {}
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

def splitAt(xs, index):
    return [xs[0:index], xs[index]]

paths = glob.glob('./**/OPS/*.html', recursive=True)
paths = [ pth for pth in paths if os.stat(pth).st_size >= 1024 * 10 ]  # 小于 10k 不是正文，跳过

paths = paths[0:2]

curr = 0
for pth in paths:
    with open(pth, encoding='utf-8-sig') as f:
        data = f.read() #f.readlines()
        lines = re.compile(r'<p>(.+?)<\/p>').findall(data)
        lines = [ re.compile(r'[^\u3007\u4E00-\u9FFF]').sub(' ', line) for line in lines ]
        lines = [ re.compile(r'[\s]+').sub(' ', line) for line in lines ]
        sentences = [ line.split(' ') for line in lines ]
        for ar in sentences:
            for sent in ar:
               ng = NG(sent, NGram)
               for g in ng:
                    k = f'{len(g)}'
                    if not k in dic_NGrams:
                        dic_NGrams[k] = {}
                    if not g in dic_NGrams[k]:
                        dic_NGrams[k][g] = {}
                    if not 'n' in dic_NGrams[k][g]:
                        dic_NGrams[k][g]['n'] = 0  # 该词出现次数
                    
                    dic_NGrams[k][g]['n'] += 1
        curr += 1
        print(f'building dic_NGrams from html: {curr} / {len(paths)}')


# 算每个词或单个字真实出现概率（简称真实概率）、理论完全随机出现的概率（简称理论概率）

# 先算所有词的真实概率

for n in range(1, NGram+1):
    ng = dic_NGrams[f'{n}']
    total = len(list(ng.keys()))

    for k, v in ng.items():
        times = v['n']           # 出现次数
        real_p = times / total   # 真实概率
        v['real_p'] = round(real_p, 6)
        
    if n % 5 == 0:
        print(f'calc real_p {n} / {NGram}')

    
#  再算所有词的理论概率
for n in range(2, NGram+1):
    ng = dic_NGrams[f'{n}']

    total = len(list(ng.keys()))

    #所有词的真实概率是理论概率的多少倍
    curr = 0
    for k, v in ng.items():

        # 遍历 k 分成左右两部分的所有可能
        theory_ps = []  # 所有左右两部分的理论概率 # 应该以最小值为准，还是以最大值为准？可能是大的，因为要判断这个命题： “真实概率远远大于理论概率”
        for i in range(1, len(k)):
            kg = splitAt(k, i)
            left = kg[0]
            right = kg[1]

            left_p = dic_NGrams[f'{len(left)}'][left]['real_p']     # 左边出现的概率
            right_p = dic_NGrams[f'{len(right)}'][right]['real_p']  # 右边出现的概率

            theory_ps.append(left_p * right_p)  # 左右连在一起的概率
            
        max_theory_p = max(theory_ps)
        v['theory_p'] = round(max_theory_p, 6)
        if v['theory_p'] < 0.000001:
            v['theory_p'] = 0.000001
        
        v['real_p/theory_p'] = round(v['real_p'] / v['theory_p'], 6)  # 真实概率 是 理论概率的多少倍
        if v['real_p/theory_p'] < 0.000001:
            v['real_p/theory_p'] = 0.000001
        
        curr += 1
        print( f'calc all word theory p {n-1} / {NGram-1}  {curr} / {len(ng)}' )
a = 1


