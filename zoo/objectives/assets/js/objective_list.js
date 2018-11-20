import Clipboard from 'clipboard'

$(document).ready(() => {
    new Clipboard('.copy-to-clipboard', {
        text (trigger) {
            showSnackbar('Copied to clipboard')
            return $(trigger).prev('input').val()
        }
    })
})
