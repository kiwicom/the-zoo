import '../style/audit_report.less'
import jQuery from 'jquery/src/jquery'
import 'semantic-ui-css/semantic.min.js'
import hljs from 'highlight.js/lib'

$('.ui.segment code').each(function (index, block) {
    hljs.highlightBlock(block)
})

const wontfixModal = $('.ui.basic.modal')
const wontfixModalForm = $('.resolve.issue.form')

wontfixModal.modal({
    transition: 'fade up',
    onDeny () {
        wontfixModalForm.submit()
        return false
    },
    onApprove () {
        Snackbar.show({
            text: 'We love you even more now',
            actionText: 'Yay!',
            actionTextColor: '#FBC02D',
            backgroundColor: '#795548'
        })
    },
    onHidden() {
        wontfixModalForm.find('.ui.label').transition('hide')
        wontfixModalForm.form('clear')
    }
})

wontfixModalForm.form({
    fields: {
        comment: 'empty'
    },
    onSuccess() {
        wontfixModal.modal('destroy')
    },
    onFailure() {
        wontfixModalForm.find('.ui.label').transition({
            animation: 'fade down',
            duration: '500ms'
        })
        return false
    }
})

$(document).on('click', '.wontfix.button', (el) => {
    const clickedButton = $(el.target).closest('.button')
    wontfixModalForm.attr('action', clickedButton.data('url'))
    wontfixModal.modal('show')
})
