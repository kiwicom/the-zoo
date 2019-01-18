import '../style/audit_report.less'
import jQuery from 'jquery/src/jquery'
import 'semantic-ui-css/semantic.min.js'
import hljs from 'highlight.js/lib'

$('.ui.segment code').each(function (index, block) {
    hljs.highlightBlock(block)
})

const wontfixModal = $('.ui.basic.modal.wontfix')
const wontfixModalForm = $('.resolve.issue.form.wontfix')

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

const patchModal = $('.ui.patch.modal')
const patchModalForm = $('.resolve.issue.form.patch')
const patchModalSegment = patchModal.find('.main.segment')

patchModalForm.form({
    onSuccess() {
        patchModal.modal('destroy')
    }
})

$(document).on('click', '.patch.button', (el) => {
    const clickedButton = $(el.target).closest('.button')
    patchModalForm.attr('action', clickedButton.data('url'))
    patchModal.modal({
        transition: 'fade up',
        onShow () {
            var $modal = $(this);
            var $content = $modal.find('.form-content');
            $.get(clickedButton.data('url'), (data) => {
                $content.html(data);
                $content.find('pre code').each(function (index, block) {
                    hljs.highlightBlock(block);
                });
                // enable approve button only if there are patches to be applied
                if ($content.find('code.diff')[0]) {
                    $modal.find('.ui.green.approve.button').removeClass('disabled');
                }
                patchModalSegment.removeClass('loading')
            });
        },
        onApprove () {
            patchModalForm.submit()
        },
        onHidden() {
            patchModalSegment.addClass('loading')
            patchModal.modal('destroy')
            patchModalForm.form('clear')
        }
    }).modal('show')
})
