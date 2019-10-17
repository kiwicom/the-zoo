import 'fomantic-ui-css/semantic.min.js'
import 'jquery-tablesort/jquery.tablesort.min.js'
import '../style/analytics_overview.less'
import 'chart.js'

const URI = require('urijs')
const searchInput = $('.ui.search input')

const enterKeyCode = 13
let queryParams = {}


$(document).ready(() => {
    const currentUrl = URI(window.location.href)
    queryParams = URI.parseQuery(currentUrl.query())

    if(queryParams.hasOwnProperty('q'))
        searchInput.val(queryParams.q)

    if(queryParams.hasOwnProperty('type')) {
        typeDropdown.dropdown('set selected', queryParams.type)
    }

    $('.version-chart').each((index, element) => {
        const chartElement = $(element)
        new Chart(
            document.getElementById($(element).attr('id')).getContext('2d'),
            {
                type: 'horizontalBar',
                data: {
                    labels: ["Versions"],
                    datasets: $(element).data("chart")
                },
                options: {
                    animation: {
                        duration: 0,
                    },
                    responsive: false,
                    devicePixelRatio: 3,
                    legend: {
                        display: false,
                    },
                    scales: {
                        xAxes: [{
                            display: false,
                            stacked: true,
                        }],
                        yAxes: [{
                            display: false,
                            stacked: true,
                        }]
                    },
                    layout: {
                        padding: 7.5
                    },
                    tooltips: {
                        enabled: false,
                        custom (hook) {
                            chartElement.popup({
                                transition: 'fade down',
                                position: 'left center',
                                on: 'manual',
                                exclusive: true,
                                html () {
                                    let lines = [
                                        `<b>${hook.title}</b><br>`,
                                    ]
                                    for(const version of hook.body) {
                                        let line = version.lines[0].split(':')
                                        const value = line.pop() * 100
                                        lines.push(
                                            `<div class="flex-horizontal--space-between">
                                                <span><b>${line.join(':')}</b>:&nbsp;</span>
                                                <span>${value.toFixed(2)}%</span>
                                            </div>`
                                        )
                                    }
                                    return lines
                                },
                                delay: {
                                  show: 250,
                                  hide: 0
                                },
                                className: {
                                  popup: 'ui histogram-popup popup'
                                }
                            })
                            chartElement.popup(hook.opacity === 0 ? 'hide': 'show')
                        }
                    }
                }
            }
        )
    })

    $('.usage-chart').each((index, element) => {
        const chartElement = $(element)
        new Chart(
            document.getElementById($(element).attr('id')).getContext('2d'),
            {
                type: 'line',
                data: {
                    labels: $(element).data("chart").labels,
                    datasets: [
                        {
                            label: 'Usages',
                            data: $(element).data("chart").series,
                            fill: false,
                            borderWidth: 3.5
                        }
                    ]
                },
                options: {
                    animation: {
                        duration: 0,
                    },
                    responsive: false,
                    devicePixelRatio: 3,
                    legend: {
                        display: false,
                    },
                    scales: {
                        xAxes: [{
                            display: false,
                        }],
                        yAxes: [{
                            display: false,
                        }]
                    },
                    elements: {
                        point: {
                            radius: .75
                        }
                    },
                    layout: {
                        padding: 7.5
                    },
                    tooltips: {
                        enabled: false,
                        custom (hook) {
                            chartElement.popup({
                                transition: 'fade down',
                                position: 'left center',
                                on: 'manual',
                                exclusive: true,
                                html: `<b>${hook.title}</b><br>${hook.body ? hook.body[0].lines[0] : ''}`,
                                delay: {
                                  show: 250,
                                  hide: 0
                                },
                                className: {
                                  popup: 'ui histogram-popup popup'
                                }
                            })
                            chartElement.popup(hook.opacity === 0 ? 'hide': 'show')
                        }
                    }
                }
            }
        )
    })
})

function applySearch() {
    const currentUrl = URI(window.location.href)
    let newUrl = URI(currentUrl.path())
    delete queryParams.page
    newUrl.setSearch(queryParams)
    window.location.href = newUrl.toString()
}

searchInput.keypress((event) => {
    if(event.which === enterKeyCode) {
        if(searchInput.val())
            queryParams.q = searchInput.val()
        else
            delete queryParams.q

        applySearch()
    }
})

$('.ui.table').tablesort()
