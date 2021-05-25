import '../style/project_list.less'

$('.project-filter .ui.basic.label').popup({
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
