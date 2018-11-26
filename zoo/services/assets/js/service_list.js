import '../style/service_list.less'
const URI = require('urijs')
const searchInput = $('.ui.search input')
const enterKeyCode = 13

const currentUrl = URI(window.location.href)
const currentQuery = URI.parseQuery(currentUrl.query()).q

searchInput.keypress((event) => {
    if(event.which === enterKeyCode) {
        let newUrl = URI(currentUrl.path())

        if(searchInput.val())
            newUrl.addSearch(URI.parseQuery('?q=' + searchInput.val()))

        window.location.href = newUrl.toString()
    }
})

if(currentQuery) {
    searchInput.val(currentQuery)
}

$('.service-filter .ui.basic.label').popup({
    transition: 'fade down',
    exclusive: true,
    hoverable: true,
    variation: 'inverted',
    position: 'left center'
})

$('.actions-wrapper a').popup({
    transition: 'fade down',
    variation: 'inverted',
    position: 'left center'
})
