// process.on('message', function (data) {
//     return process.send(JSON.stringify({msg:"计算成功", "th_proccess":data.th_proccess}))
// })

const { parentPort } = require('worker_threads')

parentPort.onmessage = function (event) {
    const startTime = new Date().getTime()
    let th_thread = event.data.th_thread
    parentPort.postMessage([true, th_thread])
}