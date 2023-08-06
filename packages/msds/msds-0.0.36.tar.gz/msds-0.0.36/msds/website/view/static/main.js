// 工具函数
function toTop() {
    window.scrollTo(0, 0)
}
function transformTime(timestamp = +new Date()) {
    if (timestamp) {
        var time = new Date(timestamp);
        var y = time.getFullYear(); //getFullYear方法以四位数字返回年份
        var M = time.getMonth() + 1; // getMonth方法从 Date 对象返回月份 (0 ~ 11)，返回结果需要手动加一
        var d = time.getDate(); // getDate方法从 Date 对象返回一个月中的某一天 (1 ~ 31)
        var h = time.getHours(); // getHours方法返回 Date 对象的小时 (0 ~ 23)
        var m = time.getMinutes(); // getMinutes方法返回 Date 对象的分钟 (0 ~ 59)
        var s = time.getSeconds(); // getSeconds方法返回 Date 对象的秒数 (0 ~ 59)
        return y + '-' + M + '-' + d + ' ' + h + ':' + m + ':' + s;
    } else {
        return '';
    }
}
function generateJSON(target) {
    try {
        var jsonValue = target.parentNode.nextElementSibling.value
        if (jsonValue[0] === '{' || jsonValue[0] === '[') {
            var jsonStr = JSON.stringify(eval(`(${jsonValue})`))
        } else if (jsonValue.indexOf(':') > -1) {
            jsonValue = `{${jsonValue}}`
            var jsonStr = JSON.stringify(eval(`(${jsonValue})`))
        } else {
            jsonValue = `[${jsonValue}]`
            var jsonStr = JSON.stringify(eval(`(${jsonValue})`))
        }
        copy(jsonStr)
    } catch (e) {
        alert('你这个数据是不是写的有点离谱?')
    }
}
function copyToStrategyBody(info, preventOtherInputChange) {
    var strategyBody = document.getElementsByClassName('strategy_body')[0]
    strategyBody.value = info
    savePageCurrentInfo(strategyBody)
    if (preventOtherInputChange) {
        return false
    }
    // 参数自动填充
    var forceParams = info.match(
        /<<strategy_params>>(.*)<<strategy_params>>/
    )
    var strategyParamsInput =
        document.getElementsByClassName('strategy_params')[0]
    if (forceParams) {
        strategyParamsInput.value = forceParams[1]
    } else {
        strategyParamsInput.value = ''
    }
    savePageCurrentInfo(strategyParamsInput)

    // 辅助线自动填充
    var forceAuxLine = info.match(
        /<<strategy_auxiliary_line>>(.*)<<strategy_auxiliary_line>>/
    )
    var strategyAuxiliaryLineInput = document.getElementsByClassName(
        'strategy_auxiliary_line'
    )[0]
    if (forceAuxLine) {
        strategyAuxiliaryLineInput.value = forceAuxLine[1]
    } else {
        strategyAuxiliaryLineInput.value = ''
    }
    savePageCurrentInfo(strategyAuxiliaryLineInput)

    // 辅助数据自动填充
    var forceAuxVolume = info.match(
        /<<strategy_auxiliary_volume>>(.*)<<strategy_auxiliary_volume>>/
    )
    var strategyAuxiliaryVolumeInput = document.getElementsByClassName(
        'strategy_auxiliary_volume'
    )[0]
    if (forceAuxVolume) {
        strategyAuxiliaryVolumeInput.value = forceAuxVolume[1]
    } else {
        strategyAuxiliaryVolumeInput.value = ''
    }
    savePageCurrentInfo(strategyAuxiliaryVolumeInput)

    // 辅助曲线自动填充
    var forceAuxCurve = info.match(
        /<<strategy_auxiliary_curve>>(.*)<<strategy_auxiliary_curve>>/
    )
    var strategyAuxiliaryCurveInput = document.getElementsByClassName(
        'strategy_auxiliary_curve'
    )[0]
    if (forceAuxCurve) {
        strategyAuxiliaryCurveInput.value = forceAuxCurve[1]
    } else {
        strategyAuxiliaryCurveInput.value = ''
    }
    savePageCurrentInfo(strategyAuxiliaryCurveInput)
}
function copy(info) {
    if (typeof info !== 'string') {
        info = info.innerText
    }
    const input = document.createElement('textarea')
    input.value = info
    document.body.appendChild(input)
    input.select()
    if (document.execCommand('Copy')) {
        document.execCommand('Copy')
    } else {
        alert('复制失败')
    }
    input.style.display = 'none'
    document.body.removeChild(input)
}
function getRandomLongString() {
    return (
        Math.random().toString(36).slice(2) +
        Math.random().toString(36).slice(2) +
        Math.random().toString(36).slice(2)
    )
}
function calcXPath(element) {
    if (element.id !== '') {
        //判断id属性，如果这个元素有id，则显 示//*[@id="xPath"]  形式内容
        return '//*[@id="' + element.id + '"]'
    }
    //这里需要需要主要字符串转译问题，可参考js 动态生成html时字符串和变量转译（注意引号的作用）
    if (element == document.body) {
        //递归到body处，结束递归
        return '/html/' + element.tagName.toLowerCase()
    }
    var ix = 1, //在nodelist中的位置，且每次点击初始化
        siblings = element.parentNode.childNodes //同级的子元素

    for (var i = 0, l = siblings.length; i < l; i++) {
        var sibling = siblings[i]
        //如果这个元素是siblings数组中的元素，则执行递归操作
        if (sibling == element) {
            return (
                arguments.callee(element.parentNode) +
                '/' +
                element.tagName.toLowerCase() +
                '[' +
                ix +
                ']'
            )
            //如果不符合，判断是否是element元素，并且是否是相同元素，如果是相同的就开始累加
        } else if (
            sibling.nodeType == 1 &&
            sibling.tagName == element.tagName
        ) {
            ix++
        }
    }
}
function findElementByXPath(xpath) {
    return document.evaluate(xpath, document).iterateNext()
}
function triggerChange(dom) {
    var event = document.createEvent('HTMLEvents')
    event.initEvent('change', true, true)
    dom.dispatchEvent(event)
}
function Loading(msg, isClose) {
    if (isClose) {
        if (!window.GLOBAL_LOADING_STATU) {
            return false
        }
        document.body.removeChild(window.GLOBAL_LOADING_WRAP)
        window.GLOBAL_LOADING_STATU = false
    } else {
        if (window.GLOBAL_LOADING_STATU) {
            return false
        }
        window.GLOBAL_LOADING_WRAP = document.createElement('div')
        window.GLOBAL_LOADING_WRAP.setAttribute('class', 'loading-wrap')
        window.GLOBAL_LOADING_WRAP.innerHTML = `
            <div class="loading-toast">
             ${msg}
            </div>`
        document.body.appendChild(window.GLOBAL_LOADING_WRAP)
        window.GLOBAL_LOADING_STATU = true
    }
}
function Selector(target, options, forceValue) {
    return new Promise((resolve) => {
        if (forceValue === undefined) {
            var oldSelector =
                document.body.getElementsByClassName('selector-wrap')[0]
            if (oldSelector) {
                document.body.removeChild(oldSelector)
            }
            var targetStyle = target.getBoundingClientRect()
            var selectorWrap = document.createElement('div')
            selectorWrap.setAttribute('class', 'selector-wrap')
            selectorWrap.onclick = () => {
                clearInterval(selectorStyleInterval)
                document.body.removeChild(selectorWrap)
            }
            selectorWrap.innerHTML = `
      <div
        class="selector-option-container"
        style="
          top:${targetStyle.top + 45}px;
          left:${targetStyle.left}px;
          width:${targetStyle.right - targetStyle.left}px;
        "
      >
        ${options
                    .map((option) => {
                        return `<div class="selector-option" onclick="window.GLOBAL_SELECTOR_HANDLER('${option.value}','${option.label}')">${option.label}</div>`
                    })
                    .join('')}
      </div>
    `

            window.GLOBAL_SELECTOR_HANDLER = (value, label) => {
                clearInterval(selectorStyleInterval)
                target.value = value
                savePageCurrentInfo(target)
                resolve({ label, value })
            }
            document.body.appendChild(selectorWrap)
            // 补一个样式跟随
            var selectorContainer = document.getElementsByClassName(
                'selector-option-container'
            )[0]
            var selectorStyleInterval = setInterval(() => {
                var newTargetStyle = target.getBoundingClientRect()
                selectorContainer.style.top = newTargetStyle.top + 45 + 'px'
                selectorContainer.style.left = newTargetStyle.left + 'px'
            }, 1000)
        } else {
            target.value = forceValue
            savePageCurrentInfo(target)
            var targetOption = options.find(
                (option) => option.value === forceValue
            )
            resolve({
                label: targetOption ? targetOption.value : '',
                value: forceValue,
            })
        }
    })
}
function Cover(callback) {
    var coverWrap = document.createElement('div')
    coverWrap.setAttribute('class', 'cover-wrap')
    coverWrap.innerHTML = `
        <div class="close-button" onclick="document.body.removeChild(this.parentNode)">关闭</div>
        <div class="cover-container"></div>
      `
    document.body.appendChild(coverWrap)
    callback &&
        callback(coverWrap.getElementsByClassName('cover-container')[0])
}
function Modal(
    title,
    info,
    logic,
    cancelLogic,
    afterRenderLogic,
    config = {}
) {
    return new Promise((resolve, reject) => {
        var modalWrap = document.createElement('div')
        modalWrap.setAttribute('class', 'modal-wrap')
        modalWrap.innerHTML = `
          <div class="modal-dialog-wrap${config.theme ? ' ' + config.theme : ''
            }">
            <div class="title">${title}</div>
            <div class="close-button" onclick="window.GLOBAL_MODAL_CLOSE(this.previousElementSibling)">${config.cancelBtnText ? config.cancelBtnText : '关闭'
            }</div>
            <div class="content"></div>
            <div class="confirm" onclick="window.GLOBAL_MODAL_CONFIRM(this.previousElementSibling)">${config.confirmBtnText ? config.confirmBtnText : '确认'
            }</div>
          </div>`
        window.GLOBAL_MODAL_CLOSE = function (content) {
            cancelLogic
                ? cancelLogic(() => {
                    document.body.removeChild(modalWrap)
                }, content)
                : document.body.removeChild(modalWrap)
        }
        window.GLOBAL_MODAL_CONFIRM = function (content) {
            logic
                ? logic(() => {
                    document.body.removeChild(modalWrap)
                }, content)
                : document.body.removeChild(modalWrap)
        }

        if (typeof info === 'string') {
            modalWrap.getElementsByClassName('content')[0].innerHTML = info
        } else {
            modalWrap.getElementsByClassName('content')[0].appendChild(info)
        }

        document.body.appendChild(modalWrap)
        afterRenderLogic && afterRenderLogic(modalWrap)
    })
}
function showEditor(target) {
    if (window.GLOBAL_STRATEGY_BODY_EDITOR) {
        return false
    }
    window.GLOBAL_STRATEGY_BODY_EDITOR = true
    var strategyBodyEditor
    Modal(
        `策略编辑器`,
        `<div class="code-mirror-wrap"></div>`,
        (closeModal, content) => {
            var editStrategyBody = strategyBodyEditor.getValue()
            target.value = editStrategyBody
            savePageCurrentInfo(target)
            closeModal()
            window.GLOBAL_STRATEGY_BODY_EDITOR = false
        },
        (closeModal, content) => {
            window.GLOBAL_STRATEGY_BODY_EDITOR = false
            closeModal()
        },
        (content) => {
            target.blur()
            strategyBodyEditor = CodeMirror(
                document.body.getElementsByClassName('code-mirror-wrap')[0],
                {
                    value: target.value,
                    mode: 'python',
                    theme: 'darcula',
                    lineNumbers: true,
                    scrollbarStyle: 'overlay',
                }
            )
        },
        {
            theme: 'darcula',
            confirmBtnText: '保存编辑内容',
            cancelBtnText: '取消编辑',
        }
    )
}
function addCircleCondition(target) {
    var keyInput = window.prompt(
        '请输入需要循环的参数名(无则增加,重复则删除)'
    )
    if (!keyInput) {
        return false
    }
    var finalCircleMap
    try {
        finalCircleMap = JSON.parse(target.value)
    } catch (e) {
        finalCircleMap = {}
    }
    if (finalCircleMap[keyInput]) {
        delete finalCircleMap[keyInput]
    } else {
        var valueInput = window.prompt('请输入:起始,结束,步长(如:1,100,10)')
        var valueArr = valueInput.split(',').map((value) => +value)
        if (valueArr.length === 3) {
            finalCircleMap[keyInput] = valueArr
        } else {
            return alert('循环条件格式错误')
        }
    }
    target.value = JSON.stringify(finalCircleMap)
    savePageCurrentInfo(target)
}
function addValueIntoObject(target) {
    var inputKey = window.prompt('请输入名称(无则增加,重复则删除)')
    if (!inputKey) {
        return false
    }
    var finalObject
    try {
        finalObject = JSON.parse(target.value)
    } catch (e) {
        finalObject = {}
    }
    var inputValue = window.prompt('请输入该参数的值')
    if (!inputValue) {
        delete finalObject[inputKey]
    } else {
        if (!isNaN(+inputValue)) {
            inputValue = +inputValue
        }
        finalObject[inputKey] = inputValue
    }
    target.value = JSON.stringify(finalObject)
    savePageCurrentInfo(target)
}
function addValueIntoArray(target) {
    var inputValue = window.prompt('请输入名称(无则增加,重复则删除)')
    if (!inputValue) {
        return false
    }
    var finalArray
    try {
        finalArray = JSON.parse(target.value)
    } catch (e) {
        finalArray = []
    }
    if (finalArray.indexOf(inputValue) > -1) {
        finalArray.splice(finalArray.indexOf(inputValue), 1)
    } else {
        finalArray.push(inputValue)
    }
    target.value = JSON.stringify(finalArray)
    savePageCurrentInfo(target)
}
function useDefaultStrategy(name) {
    copyToStrategyBody(window.GLOBAL_DEFAULT_STRATEGY_INFO[name])

    var useDefaultInput = document.getElementsByClassName(
        'default_strategy_name'
    )[0]
    useDefaultInput.value = name
    savePageCurrentInfo(useDefaultInput)
}
function showDataSelector(target, shouldUpdateFaceValue) {
    Selector(target, [
        { label: 'BTC-USDT > 5m', value: 'BTC-USDT_5m.h5' },
        { label: 'SHIB-USDT > 5m', value: 'SHIB-USDT_5m.h5' },
        { label: 'SHIB-USDT > 1m', value: 'SHIB-USDT_1m.h5' },
        { label: 'FIL-USDT > 5m', value: 'FIL-USDT_5m.h5' },
        { label: 'NEAR-USDT > 5m', value: 'NEAR-USDT_5m.h5' },
    ]).then((select) => {
        if (shouldUpdateFaceValue) {
            var dataName = select.value.split('_')[0]
            showFaceValueSelector(target.nextElementSibling, dataName)
        }
    })
}
function showResampleSelector(target) {
    Selector(target, [
        { label: '1T', value: '1T' },
        { label: '5T', value: '5T' },
        { label: '15T', value: '15T' },
        { label: '30T', value: '30T' },
        { label: '60T', value: '60T' },
    ])
}
function showFaceValueSelector(target, dataOfFaceValueName) {
    var faceValueOptions = [
        { label: 'SHIB-USDT >> 1000000', value: 1000000 },
        { label: 'BTC-USDT >> 0.01', value: 0.01 },
        { label: 'NEAR-USDT >> 10', value: 10 },
        { label: 'FIL-USDT >> 0.1', value: 0.1 },
    ]
    var targetOption =
        faceValueOptions.find((option) => {
            return option.label.indexOf(dataOfFaceValueName) > -1
        }) || null
    Selector(
        target,
        faceValueOptions,
        targetOption ? targetOption.value : undefined
    )
}
// 业务类
function addInfoGroup(element, callback) {
    var targetGroup = element.children[1]
    var container = element
    var copyGroup = document.createElement('div')
    copyGroup.className = targetGroup.className
    copyGroup.innerHTML = targetGroup.innerHTML
    container.appendChild(copyGroup)
    callback && callback(copyGroup)
    savePageCurrentInfo()
}
function calcAllParams() {
    var params = {}
    params.fallback_name =
        document.getElementsByClassName('fallback_name')[0].value ||
        getRandomLongString()
    // 同步一下dom
    var fallbackNameInput =
        document.getElementsByClassName('fallback_name')[0]
    fallbackNameInput.value = params.fallback_name
    triggerChange(fallbackNameInput)
    var divisions = document.getElementsByClassName('division-group')
    Array.prototype.forEach.call(divisions, (division) => {
        var divisionParamName = division.classList[1]
            .slice(0, -7)
            .replace(/\-/gi, '_')
        var groups = document.getElementsByClassName(
            division.classList[1].slice(0, -1)
        )
        var groupValueList = []
        Array.prototype.forEach.call(groups, (group) => {
            var groupValue = {}
            Array.prototype.forEach.call(group.children, (formItem) => {
                if (formItem.value) {
                    try {
                        groupValue[formItem.className] = JSON.parse(formItem.value)
                    } catch (e) {
                        groupValue[formItem.className] = formItem.value
                    }
                }
            })
            if (Object.keys(groupValue).length) {
                groupValueList.push(groupValue)
            }
        })
        params[divisionParamName] = groupValueList
    })
    return params
}
function clearPageSaveInfo() {
    localStorage.clear()
    location.reload()
}
function deleteCurrentFallback() {
    axios.get(
        `/api/delete_fallback?fallback_name=${document.getElementsByClassName('fallback_name')[0].value
        }`
    )
}
function traverseArraysObject(obj) {
    var traverseResult = []
    Object.keys(obj).forEach((objKey) => {
        // 本层开始之前的原始参数体
        var copyCurrentResult = JSON.parse(JSON.stringify(traverseResult))
        var finalCurrentResult = []
        if (typeof obj[objKey] === 'string') {
            if (copyCurrentResult.length) {
                finalCurrentResult = copyCurrentResult.map((resultItem) => {
                    resultItem[objKey] = obj[objKey]
                    return resultItem
                })
            } else {
                finalCurrentResult.push({ [objKey]: obj[objKey] })
            }
        } else {
            if (copyCurrentResult.length) {
                obj[objKey].forEach((currentValue, valueIndex) => {
                    copyCurrentResult.forEach((originItem) => {
                        finalCurrentResult.push(
                            Object.assign({}, originItem, {
                                [objKey]: obj[objKey][valueIndex],
                            })
                        )
                    })
                })
            } else {
                obj[objKey].forEach((currentValue, valueIndex) => {
                    finalCurrentResult.push({ [objKey]: obj[objKey][valueIndex] })
                })
            }
        }
        traverseResult = finalCurrentResult
    })
    return traverseResult
}
function resetInfoGroup(target) {
    deleteFormCacheValue(target)
}
function deleteFormCacheValue(target) {
    // todo:清除所有缓存数据
}
function savePageCurrentInfo(target, preventHTMLSave) {
    if (!preventHTMLSave) {
        var currentHTML =
            document.getElementsByClassName('body-container')[0].innerHTML
        localStorage.setItem('fallbackPageInfo', currentHTML)
    }
    if (target) {
        var currentXPath = calcXPath(target)
        var currentValue = target.value
        var valueSaved = localStorage.getItem('valueXPathMap')
        if (!valueSaved) {
            valueSaved = {}
        } else {
            valueSaved = JSON.parse(valueSaved)
        }
        valueSaved[currentXPath] = currentValue
        localStorage.setItem('valueXPathMap', JSON.stringify(valueSaved))
    }
}
function formatTime (ms) {
    var time = new Date(parseInt(ms));
    var YYYY = time.getFullYear();
    var M, D, h, m, s;
    var MM = ((M = time.getMonth() + 1) < 10) ? ("0" + M) : M;
    var DD = ((D = time.getDate()) < 10) ? ("0" + D) : D;
    var hh = ((h = time.getHours()) < 10) ? ("0" + h) : h;
    var mm = (m = time.getMinutes()) < 10 ? ('0' + m) : m;
    var ss = (s = time.getSeconds()) < 10 ? ('0' + s) : s;

    var timeStr = YYYY + "-" + MM + "-" + DD + " " + hh + ":" + mm + ":" + ss;
    return timeStr;
}
function generateNewEchart(missionNumber) {
    var fallbackInfo = window.GLOBAL_FALLBACK_INFO
    Loading('生成图表中,请稍后...')
    axios
        .get(
            `/data`
        )
        .then((res) => {
            Cover((content) => {
                window.GLOBAL_ECHART = echarts.init(content)
                var originData = res.data
                var chartInfo = {
                    time: [],
                    candle: originData.candle,
                    volume: [],
                    equity_curve: [],
                    signal: [],
                }
                originData.time.forEach(item => {
                    chartInfo.time.push(formatTime(item))
                })
                originData.volume.forEach(item => {
                    chartInfo.volume.push([
                        formatTime(item[0]),
                        item[1]
                    ])
                })
                originData.equity_curve.forEach(item => {
                    chartInfo.equity_curve.push([
                        formatTime(item[0]),
                        item[1]
                    ])
                })
                originData.signal.forEach(item => {
                    item[0] = formatTime(item[0])
                    chartInfo.signal.push(item)
                })
                var option = {
                    xAxis: {
                        data: chartInfo.time,
                    },
                    yAxis: [
                        {
                            scale: true,
                            name: '价格',
                            position: 'left',
                            splitArea: {
                                show: true,
                            },
                        },
                        {
                            name: '成交量',
                            position: 'right',
                            splitLine: {
                                show: false,
                            },
                        },
                        {
                            name: '资金曲线',
                            positoin: 'right',
                            offset: -80,
                            splitLine: {
                                show: false,
                            },
                        }
                    ],
                    series: [
                        {
                            name: '价格',
                            type: 'candlestick',
                            data: chartInfo.candle,
                            yAxisIndex: 0,
                            markPoint: {
                                label: {
                                    formatter: function (param) {
                                        switch (Number(param.value)) {
                                            case 0:
                                                return '平'
                                            case 1:
                                                return '多'
                                            case -1:
                                                return '空'
                                        }
                                    },
                                },
                                data: chartInfo.signal.map((eachSignal) => {
                                    eachSignal[1] = Number(eachSignal[1])
                                    eachSignal[2] = Number(eachSignal[2])
                                    return {
                                        name: (() => {
                                            switch (eachSignal[2]) {
                                                case 0:
                                                    return '平仓'
                                                case 1:
                                                    return '做多'
                                                case -1:
                                                    return '做空'
                                            }
                                        })(),
                                        coord: (() => {
                                            switch (eachSignal[2]) {
                                                case 0:
                                                    return [eachSignal[0], eachSignal[1]]
                                                case 1:
                                                    return [eachSignal[0], eachSignal[1]]
                                                case -1:
                                                    return [eachSignal[0], eachSignal[1]]
                                            }
                                        })(),
                                        value: (() => {
                                            switch (eachSignal[2]) {
                                                case 0:
                                                    return 0
                                                case 1:
                                                    return 1
                                                case -1:
                                                    return -1
                                            }
                                        })(),
                                        itemStyle: (() => {
                                            switch (eachSignal[2]) {
                                                case 0:
                                                    return { color: 'rgb(50,50,255)' }
                                                case 1:
                                                    return { color: 'rgb(255,50,50)' }
                                                case -1:
                                                    return { color: 'rgb(50,255,50)' }
                                            }
                                        })(),
                                    }
                                }),
                                tooltip: {
                                    formatter: function (param) {
                                        return (
                                            param.name + '<br>' + (param.data.coord || '')
                                        )
                                    },
                                },
                            },
                        },
                        {
                            name: '成交量',
                            type: 'bar',
                            yAxisIndex: 1,
                            data: chartInfo.volume,
                            itemStyle: {
                                color: function (param) {
                                    return 'rgba(0,0,0,0.08)'
                                },
                            },
                        },
                        {
                            name: '资金曲线',
                            type: 'line',
                            yAxisIndex: 2,
                            symbol: 'none',
                            areaStyle: {
                                color: 'rgba(164,222,137,0.1)',
                            },
                            data: chartInfo.equity_curve.map((item) => item[1]),
                            lineStyle: {
                                width: 0.8,
                            },
                        },
                    ],
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'cross',
                        },
                    },
                    grid: {
                        left: '10%',
                        right: '10%',
                        bottom: '15%',
                    },
                    dataZoom: [
                        {
                            type: 'inside',
                            start: 0,
                            end: 5,
                        },
                        {
                            show: true,
                            type: 'slider',
                            top: '90%',
                            start: 0,
                            end: 5,
                        },
                    ],
                    legend: {
                        data: ['价格', '成交量'],
                    },
                }
                window.GLOBAL_ECHART.setOption(option)
                Loading('', true)
            })
        })
}
function backToMainFallbackMission() {
    if (localStorage.getItem('isInSubMission') !== 'true') {
        return alert('当前并非循环子任务')
    }
    var fallbackNameInput =
        document.getElementsByClassName('fallback_name')[0]
    var circleConditionInput = document.getElementsByClassName(
        'strategy_circle_condition'
    )[0]
    var strategyParamsInput =
        document.getElementsByClassName('strategy_params')[0]

    fallbackNameInput.value = localStorage.getItem('mainMissionName')
    savePageCurrentInfo(fallbackNameInput)

    circleConditionInput.value = localStorage.getItem(
        'mainMissionCircleCondition'
    )
    savePageCurrentInfo(circleConditionInput)

    strategyParamsInput.value = localStorage.getItem('mainMissionParams')
    savePageCurrentInfo(strategyParamsInput)

    localStorage.setItem('isInSubMission', 'false')
    localStorage.setItem('needFirstEnterAnotherMissionRun', 'true')
    location.reload()
}
function generateAndRunNewFallbackMission(mission, missionIndex) {
    // todo:目前仅支持了策略体的保存,后续变为全参数可保存
    var fallbackNameInput =
        document.getElementsByClassName('fallback_name')[0]
    var circleConditionInput = document.getElementsByClassName(
        'strategy_circle_condition'
    )[0]
    var strategyParamsInput =
        document.getElementsByClassName('strategy_params')[0]

    // 这里可以理解为每一次都只拿sourcename
    localStorage.setItem('mainMissionName', fallbackNameInput.value)
    fallbackNameInput.value = ''
    savePageCurrentInfo(fallbackNameInput)

    localStorage.setItem(
        'mainMissionCircleCondition',
        circleConditionInput.value
    )
    circleConditionInput.value = ''
    savePageCurrentInfo(circleConditionInput)

    localStorage.setItem('mainMissionParams', strategyParamsInput.value)
    strategyParamsInput.value = JSON.stringify(
        mission.strategy.strategy_params
    )
    savePageCurrentInfo(strategyParamsInput)

    localStorage.setItem('isInSubMission', 'true')
    localStorage.setItem('needFirstEnterAnotherMissionRun', 'true')
    location.reload()
}
function openFallbackDetail() {
    searchFallback().then((res) => {
        if (
            Object.keys(window.GLOBAL_FALLBACK_INFO.fallback_missions)
                .length === 1
        ) {
            generateNewEchart(0)
        } else {
            var maxDetailNumber = 100
            Loading('处理详情中...')
            Modal(
                `查看任务详细信息(按照资金曲线排序)`,
                `${`<div style="margin-bottom:12px;">出于性能原因,暂时仅展示资金曲线最高的${maxDetailNumber}条</div>` +
                Object.keys(window.GLOBAL_FALLBACK_INFO.fallback_missions)
                    .sort((current, next) => {
                        return (
                            window.GLOBAL_FALLBACK_INFO.fallback_missions[next]
                                .final_result -
                            window.GLOBAL_FALLBACK_INFO.fallback_missions[current]
                                .final_result
                        )
                    })
                    .slice(0, maxDetailNumber)
                    .map((missionIndex) => {
                        mission =
                            window.GLOBAL_FALLBACK_INFO.fallback_missions[
                            missionIndex
                            ]
                        return `<div class="mission-item" onclick="${Object.keys(window.GLOBAL_FALLBACK_INFO.fallback_missions)
                                .length === 1
                                ? `generateNewEchart(${missionIndex})`
                                : `generateAndRunNewFallbackMission(
                    window.GLOBAL_FALLBACK_INFO.fallback_missions[${missionIndex}],
                    ${missionIndex}
                  )`
                            }"><pre>
${Object.keys(window.GLOBAL_FALLBACK_INFO.fallback_missions).length === 1
                                ? '[点击查看任务细节]'
                                : '[点击单独执行该任务]'
                            }
任务编号:${missionIndex}
收益:${mission.final_result}
策略参数:${JSON.stringify((() => mission.strategy.strategy_params)(), null, 4)}
</pre></div>`
                    })
                    .join('')
                }`,
                (closeModal, content) => {
                    closeModal()
                }
            )
            Loading('', true)
        }
    })
}

// 请求类
function cancelFallback() {
    var fallbackName =
        document.getElementsByClassName('fallback_name')[0].value
    return axios
        .get(`/api/cancel_fallback?fallback_name=${fallbackName}`)
        .then((res) => {
            if (res.data.result === 1) {
                window.GLOBAL_FALLBACK_INFO = res.data.data
                document.getElementsByClassName(
                    'fallback-result'
                )[0].innerHTML = `<pre>回测任务当前进度:
${res.data.data.fallback_process}</pre>`
                savePageCurrentInfo()
            } else {
                alert(res.data.error_msg)
            }
            // 取消循环查询
            clearInterval(window.GLOBAL_SEARCH_FALLBACK_INTERVAL)
        })
}
function searchFallback(useAutoProcess, dropFallbackMissions) {
    if (window.GLOBAL_SEARCH_FALLBACK_API_LOADING === true) {
        return false
    }
    window.GLOBAL_SEARCH_FALLBACK_API_LOADING = true
    var fallbackName =
        document.getElementsByClassName('fallback_name')[0].value
    return axios
        .get(
            `/api/search_fallback?fallback_name=${fallbackName}&drop_fallback_missions=${dropFallbackMissions ? '1' : '0'
            }`
        )
        .then((res) => {
            if (res.data.result === 1 && res.data.data) {
                window.GLOBAL_FALLBACK_INFO = res.data.data
                document.getElementsByClassName(
                    'fallback-result'
                )[0].innerHTML = `<pre>回测任务当前进度:
${res.data.data.fallback_process}</pre>`
                savePageCurrentInfo()
                window.GLOBAL_SEARCH_FALLBACK_API_LOADING = false
                if (useAutoProcess) {
                    if (res.data.data.fallback_statu !== 'running') {
                        clearInterval(window.GLOBAL_SEARCH_FALLBACK_INTERVAL)
                    }
                    if (res.data.data.fallback_statu === 'finished') {
                        openFallbackDetail()
                    }
                }
            } else if (res.data.result === -1) {
                window.GLOBAL_SEARCH_FALLBACK_API_LOADING = false
            } else {
                alert(res.data.error_msg)
                window.GLOBAL_SEARCH_FALLBACK_API_LOADING = false
            }
        })
}
function runFallback() {
    var params = calcAllParams()
    return axios.post('/api/run_fallback', params).then((res) => {
        if (res.data.result === 1) {
            window.GLOBAL_FALLBACK_INFO = res.data.data
            document.getElementsByClassName(
                'fallback-result'
            )[0].innerHTML = `<pre>回测任务当前进度:
${res.data.data.fallback_process}</pre>`
            savePageCurrentInfo()
            clearInterval(window.GLOBAL_SEARCH_FALLBACK_INTERVAL)
            window.GLOBAL_SEARCH_FALLBACK_INTERVAL = setInterval(() => {
                searchFallback(true, true)
            }, 1000)
        } else {
            alert(res.data.error_msg)
        }
    })
}

// 初始化行为类
; (() => {
    axios.get('/api/search_default_strategy').then((res) => {
        if (res.data.result === 1) {
            if (res.data.data.length) {
                var defaultStrategyContainer = document.getElementsByClassName(
                    'default-strategy-list'
                )[0]
                defaultStrategyContainer.innerHTML = ''
                window.GLOBAL_DEFAULT_STRATEGY_INFO = {}
                res.data.data.forEach((strategyInfo) => {
                    window.GLOBAL_DEFAULT_STRATEGY_INFO[
                        strategyInfo.strategy_name
                    ] = strategyInfo.strategy_info
                    var strategyInfoItem = document.createElement('div')
                    strategyInfoItem.setAttribute('class', 'default-strategy-item')
                    var strategyNameStr = strategyInfo.strategy_name.replace(
                        '.py',
                        ''
                    )
                    strategyInfoItem.innerHTML = `
          <div class="strategy-item">
            <label for="${strategyNameStr}" class="label-source">${strategyNameStr}</label>
            <button onclick="copyToStrategyBody(window.GLOBAL_DEFAULT_STRATEGY_INFO['${strategyInfo.strategy_name}'])">编辑器加载策略相关内容</button>
            <button onclick="copy(window.GLOBAL_DEFAULT_STRATEGY_INFO['${strategyInfo.strategy_name}'])">复制内容</button>
            <button onclick="useDefaultStrategy('${strategyInfo.strategy_name}')">设为默认加载</button>
            <input id="${strategyNameStr}" type="checkbox" class="label-target">
            <pre>${strategyInfo.strategy_info}</pre>
            </div>
        `
                    defaultStrategyContainer.appendChild(strategyInfoItem)
                })
                var defaultUseStrategy = document.getElementsByClassName(
                    'default_strategy_name'
                )[0].value
                // 这里有个子任务的问题,如果当前是子任务就不要覆盖其他参数了
                if (
                    defaultUseStrategy &&
                    localStorage.getItem('isInSubMission') !== 'true'
                ) {
                    copyToStrategyBody(
                        window.GLOBAL_DEFAULT_STRATEGY_INFO[defaultUseStrategy]
                    )
                }
            }
        } else {
            alert(res.data.error_msg)
        }
    })
})()
    // 做一个表单信息的存储功能
; (() => {
    var valueSaved = localStorage.getItem('valueXPathMap')
    var htmlSaved = localStorage.getItem('fallbackPageInfo')
    if (htmlSaved) {
        document.getElementsByClassName('body-container')[0].innerHTML =
            htmlSaved
    }
    if (valueSaved) {
        valueSaved = JSON.parse(valueSaved)
        for (var key in valueSaved) {
            var element = findElementByXPath(key)
            if (element) {
                element.value = valueSaved[key]
            }
        }
    }

    if (
        localStorage.getItem('needFirstEnterAnotherMissionRun') === 'true'
    ) {
        runFallback()
        localStorage.setItem('needFirstEnterAnotherMissionRun', 'false')
    }

    document.body.addEventListener(
        'change',
        (e) => {
            savePageCurrentInfo(e.target)
        },
        true
    )
    var globalKeyActive = false
    document.addEventListener('keyup', (e) => {
        switch (e.code) {
            case 'ControlLeft':
                globalKeyActive = false
                break
        }
    })
    document.body.addEventListener('keydown', (e) => {
        switch (e.code) {
            case 'ControlLeft':
                globalKeyActive = true
                break
            case 'Enter':
                globalKeyActive && runFallback()
                break
            case 'Slash':
                globalKeyActive && searchFallback()
                break
            case 'Digit0':
                globalKeyActive && cancelFallback()
                break
            case 'Period':
                globalKeyActive && openFallbackDetail()
                break
        }
    })
})()

; (() => {
    generateNewEchart()
})()