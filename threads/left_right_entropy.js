const { parentPort } = require('worker_threads')
// const _ = require('lodash')

parentPort.onmessage = function (event) {
    let { thread_id, dic_NGrams, n, NGram } = event.data

    let ng = dic_NGrams[n]

    let total = Object.keys(ng).length


    // 计算所有词的左邻右邻字的丰富度（用信息熵衡量，越大越丰富），取它们中较小的那个作为丰富度
    let curr = 0
    for (let [k, v] of Object.entries(ng)) {

        if (curr++ % 100 == 0) {
            console.log(`start calc left_right_entropy thread ${thread_id - 1} curr/total: ${curr}/${total}`)
        }

        // 算这个词的左邻有多少个不同的字，右邻有多少个不同的字
        let lefts = {}
        let rights = {}
        for (let c of k) {
            let its = dic_NGrams[1][c][`c_words`]  // 所有含 c 这个字符的大于三的词
            if (!its) {
                continue
            }
            for (let it of its) {
                let t = it[0]
                if (t.length > k.length && t.indexOf(k) != -1  ) {
                    
                    let reg = String.raw`(.)${k}`
                    let ar = Array.from(t.matchAll(reg))
                    ar.forEach((w) => {
                        if (!lefts[w[1]]) {
                            lefts[w[1]] = true
                        }
                    })

                    let reg2 = String.raw`${k}(.)`
                    let ar2 = Array.from(t.matchAll(reg2))
                    ar2.forEach((w) => {
                        if (!rights[w[1]]) {
                            rights[w[1]] = true
                        }
                    })
                }
            }
        }

        // 算左邻右邻信息熵
        let left_entropy = 0
        let right_entropy = 0
        for (let w of Object.keys(lefts)) {
            let item = dic_NGrams[`1`][w]
            let real_p = item[`real_p`]
            left_entropy += -1 * real_p * Math.log(real_p)
        }
        for (let w of Object.keys(rights)) {
            let item = dic_NGrams[`1`][w]
            let real_p = item[`real_p`]
            right_entropy += -1 * real_p * Math.log(real_p)
        }

        let min_entropy = Math.min(left_entropy, right_entropy)
        if (min_entropy < 0.000001) {
            min_entropy = 0.000001
        }
        v[`min_entropy`] = min_entropy

    }

    //console.log(`thread ${thread_id} done.`)
    parentPort.postMessage([true, { thread_id, dic_NGrams, n }])
    process.exit()
}