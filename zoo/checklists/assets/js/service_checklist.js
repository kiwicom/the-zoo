import '../style/service_checklist.less'

function updateSegmentStatus(segment, color) {
    const button = segment.find('.button')
    const buttonContainer = button.closest('.segment')

    button.attr('class', `ui fluid ${color} button`)
    buttonContainer.attr('class', `ui fluid ${color} segment`)

    if(color !== 'yellow')
        button.html(color === 'green' ? 'Done' : 'Not done')
    else
        button.addClass('loading')
}

$(document).on('click', '.checklist-action-wrapper', (event) => {
    const clickedWrapper = $(event.target).closest('.checklist-action-wrapper')
    const wasChecked = clickedWrapper.data('checked') === 'True'
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val()

    updateSegmentStatus(clickedWrapper, 'yellow')

    $.post({
        url: clickedWrapper.data('url'),
        data: {
            checked: !wasChecked,
            csrfmiddlewaretoken: csrfToken
        }
    }).done(() => {
        updateSegmentStatus(clickedWrapper, wasChecked ? 'red' : 'green')
        clickedWrapper.data('checked', wasChecked ? 'False' : 'True')
    }).fail(() => {
        Snackbar.show({
            text: 'Oops, the server... failed',
            actionText: 'Ok',
            actionTextColor: '#FBC02D',
            backgroundColor: '#795548'
        })
        updateSegmentStatus(clickedWrapper, wasChecked ? 'green' : 'red')
    })
})