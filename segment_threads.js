
(async () => {

    let NGram = 5 // 词的长度是 NGram - 1 ，长度为 NGram 
    let dir = '金庸全集（精制插图版，连载初回本）/OPS'
    // 所有连续 N 个字，和它出现的总次数
    let dic_NGrams = []

    // NGram
    function NG(strs, NGram) {

        strs = strs.replace(/\s/g, '')

        function ng(s, n) {

            var grs = []

            for (let i = 0; i < s.length; i++) {

                if (i + n > s.length) {
                    break
                }

                var gr = s.substring(i, i + n)

                grs.push(gr)


            }

            return grs

        }

        var gss = []
        for (let i = 1; i <= NGram; i++) {

            let gs = ng(strs, i)

            if (gs.length > 0) {

                gss = gss.concat(gs)

            } else {

                break

            }

        }

        return gss

    }

    // 多线程计算
    test_threads: {
        const { Worker, workerData, parentPort } = require('worker_threads')
        let re = await new Promise(function (resolve, reject) {
            const wk1 = new Worker(require('path').resolve(__dirname, './calc.js'))
            wk1.ref()
            wk1.postMessage({ "th_thread": 1 })
            wk1.on('message', async (re) => {
                resolve('ok')
            })
        })
    }

    // 构造 NGram 字典
    build_dic_NGrams: {

        for (let i = 0; i <= NGram; i++) {
            dic_NGrams.push({}) // 每个线程负责一个数据块的计算
        }

        let path = require('path')
        let rd = require('rd')
        let fs = require('fs')
        let _ = require('lodash')
        let paths = []

        // 目录下的所有文件名
        rd.eachFileFilterSync(dir, /\.html$/, function (fullpath, stats) {

            if (stats.size < 1024 * 10) {
                // 小于 10k 不是正文，跳过
                return
            }

            paths.push(fullpath)
        })

        let curr = 0
        paths = paths.slice(0, 3)
        for (let pth of paths) {

            let text = fs.readFileSync(pth, { encoding: 'utf8', flag: 'r' })

            let arr = Array.from(text.matchAll(/<p>(.+?)<\/p>/g))

            let str = ''
            for (let ar of arr) {
                let line = ar[1]
                str += line
            }
            str = str.replace(/[^\u3007\u4E00-\u9FFF]/g, ' ').replace(/[\s]+/g, ' ')  // 只要汉字，除掉其他所有符号
            let ar = str.split(' ')
            for (let r of ar) {
                let ng = NG(r, NGram)
                for (let g of ng) {
                    let k = g.length
                    if (k > NGram) {
                        throw `something wrong`
                    }
                    if (!dic_NGrams[k][g]) {
                        dic_NGrams[k][g] = {}
                    }
                    if (!dic_NGrams[k][g][`n`]) {
                        dic_NGrams[k][g][`n`] = 0  // 该词出现次数
                    }
                    dic_NGrams[k][g][`n`] += 1
                }
            }

            curr += 1
            console.log(`building dic_NGrams ${curr} / ${paths.length}`)
        }

        for (let i = 3; i < NGram; i++) {
            for (let it of Object.entries(dic_NGrams[i])) {
                // 遍历所有字符
                for (let c of it[0]) {
                    let item = dic_NGrams[1][c]
                    if (!item[`c_words`]) {
                        item[`c_words`] = []  // 存所有含这个字的长度大于等于3 的词的引用
                            // 因为目的是用来算左右邻信息熵，词至少两个字，再加上左右的字，至少三个。小于三的不存了，节省内存
                    }
                    item[`c_words`].push(it)
                }

            }
        }

    }



    //
    // 算每个词或单个字真实出现概率（简称真实概率）、理论完全随机出现的概率（简称理论概率）
    //

    // 所有词的真实概率
    calc_real_p: {
        for (let n = 1; n <= NGram; n++) {
            let ng = dic_NGrams[n]
            let total = Object.keys(ng).length
            for (let [k, v] of Object.entries(ng)) {
                let times = v[`n`]           // 出现次数
                let real_p = times / total   // 真实概率
                v[`real_p`] = real_p.toFixed(6)
            }
            console.log(`calc real_p curr/NGram: ${n} / ${NGram}`)
        }
    }

    // 计算所有词的真实概率，再算它是最大理论概率的多少倍，最后存入全局字典
    calc_theory_p: {
        // 开多线程，计算真实概率 是 理论概率的多少倍
        let re = await new Promise(async (resolve, reject) => {
            let start = 2
            let numThread = NGram - start + 1
            let threadDone = 0
            for (let n = start; n <= NGram; n++) {
                const { Worker, workerData, parentPort } = require('worker_threads')
                const wk1 = new Worker(require('path').resolve(__dirname, './threads/theory_p.js'))
                wk1.ref()
                wk1.postMessage({ "thread_id": n, dic_NGrams, n })
                wk1.on('message', async (re) => {
                    threadDone++
                    let nn = re[1]['n']
                    let ddic_NGrams = re[1]['dic_NGrams']
                    dic_NGrams[nn] = ddic_NGrams[nn]
                    console.log(`threadDone theory_p curr/numThread: ${threadDone} / ${numThread}`)
                    if (threadDone >= numThread) {
                        resolve('ok')
                    }
                })
                wk1.on('error', (e) => {
                    throw `thread err. ${e}`
                })
            }
        })
    }

    // 计算所有词的左邻右邻字的丰富度（用信息熵衡量，越大越丰富），取它们中较小的那个作为丰富度
    calc_left_right_entropy: {
        // 开多线程，计算左邻右邻最小信息熵
        let re = await new Promise(async (resolve, reject) => {
            let start = 2
            let numThread = NGram - start
            let threadDone = 0
            for (let n = start; n < NGram; n++) {
                const { Worker, workerData, parentPort } = require('worker_threads')
                const wk1 = new Worker(require('path').resolve(__dirname, './threads/left_right_entropy.js'))
                wk1.ref()
                wk1.postMessage({ "thread_id": n, dic_NGrams, n, NGram })
                wk1.on('message', async (re) => {
                    threadDone++
                    let nn = re[1]['n']
                    let ddic_NGrams = re[1]['dic_NGrams']
                    dic_NGrams[nn] = ddic_NGrams[nn]
                    console.log(`threadDone left_right_entropy curr/numThread: ${threadDone} / ${numThread}`)
                    if (threadDone >= numThread) {
                        resolve('ok')
                    }
                })
                wk1.on('error', (e) => {
                    throw `thread err. ${e}`
                })
            }
        })
    }

    // 保存分词结果
    save_result:{
        for (let i = 2; i < NGram; i++) {
            let word2 = dic_NGrams[i]
            let result = require('lodash').pickBy(word2, function (v, k) { return v[`real_p/theory_p`] >= 1.0 && v[`min_entropy`] >= 0.85 })
            let tmp = Object.keys(result).join('\n')
            require('fs').writeFileSync(`result${i}.txt`, tmp, { encoding: 'utf8', flag: 'w' })
        }
    }
})()



