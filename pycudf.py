
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

        # for (let [k, v] of Object.entries(ng)) {
        #     let times = v[`n`]           // 出现次数
        #     let real_p = times / total   // 真实概率
        #     v[`real_p`] = real_p.toFixed(6)
        # }

        # console.log(`calc real_p ${n} / ${NGram}`)

    



a = 1


