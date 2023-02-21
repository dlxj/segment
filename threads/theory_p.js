const { parentPort } = require('worker_threads')

parentPort.onmessage = function (event) {
    let { thread_id, dic_NGrams, n } = event.data

    let ng = dic_NGrams[n]

    let total = Object.keys(ng).length

    let splitAt = (xs, index) => [xs.slice(0, index), xs.slice(index)]

    // 所有词的真实概率是理论概率的多少倍
    let curr = 0
    for (let [k, v] of Object.entries(ng)) {
        
        if (curr++ % 100 == 0) {
            console.log(`start calc theory_p thread ${thread_id} curr/total: ${curr}/${total}`)
        }

        // 遍历 k 分成左右两部分的所有可能
        let theory_ps = []  // 所有左右两部分的理论概率 // 应该以最小值为准，还是以最大值为准？可能是大的，因为要判断这个命题： “真实概率远远大于理论概率”
        for (let i = 1; i < k.length; i++) {

            let kg = splitAt(k, i)
            let left = kg[0]
            let right = kg[1]

            let left_p = dic_NGrams[left.length][left]['real_p']     // 左边出现的概率
            let right_p = dic_NGrams[right.length][right]['real_p']  // 右边出现的概率

            theory_ps.push(left_p * right_p)  // 左右连在一起的概率
        }

        let max_theory_p = Math.max(...theory_ps)
        v[`theory_p`] = max_theory_p.toFixed(6)
        if (v[`theory_p`] < 0.000001) {
            v[`theory_p`] = 0.000001
        }
        v[`real_p/theory_p`] = (v[`real_p`] / v[`theory_p`]).toFixed(6)  // 真实概率 是 理论概率的多少倍
        if (v[`real_p/theory_p`] < 0.000001) {
            v[`real_p/theory_p`] = 0.000001
        }


    }
    
    console.log(`thread ${thread_id} done.`)
    parentPort.postMessage([true, { thread_id, dic_NGrams, n }])
    process.exit()
}