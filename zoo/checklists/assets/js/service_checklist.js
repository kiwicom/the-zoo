import '../style/service_checklist.less'

$(document).on('click', '.checklist-action-wrapper', (event) => {
    const clickedWrapper = $(event.target).closest('.checklist-action-wrapper')
    const wasChecked = clickedWrapper.data('checked') === 'True'
    const button = clickedWrapper.find('.button')
    const buttonContainer = button.closest('.segment')
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val()

    button.attr('class', 'ui loading fluid yellow button')
    buttonContainer.attr('class', 'ui fluid yellow segment')

    $.post({
        url: clickedWrapper.data('url'),
        data: {
            checked: !wasChecked,
            csrfmiddlewaretoken: csrfToken
        }
    }).done(() => {
        button.attr('class', `ui fluid ${wasChecked ? 'red' : 'green'} button`)
        button.html(wasChecked ? 'Not done' : 'Done')
        clickedWrapper.data('checked', wasChecked ? 'False' : 'True')
        buttonContainer.attr('class', `ui fluid ${wasChecked ? 'red' : 'green'} segment`)
    })
})