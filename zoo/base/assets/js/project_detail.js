import '../style/project_detail.less'
import jQuery from 'jquery/src/jquery'
import 'fomantic-ui-css/semantic.min.js'
import Mustache from 'mustache'


$(document).ready(() => {
  const repoDetailsContainer = $('#repository-details-container')
  const projectDeleteForm = $('#project-delete-form')
  const confirmationModal = $('.ui.basic.modal')
  let projectDeleteFormProcessed = false

  $.get(repoDetailsContainer.data('url'))
  .done((response) => {
    let template = $('#repository-details').html()
    repoDetailsContainer.html(Mustache.render(template, response))
    repoDetailsContainer.removeClass('loading')
    $('.statistic').popup({
      transition: 'fade down',
      exclusive: true,
      position: 'top center'
    })
  })
  .fail(() => {
    showSnackbar('Failed fetching repository')
    repoDetailsContainer.remove()
  })

  $('.ui.fade.dropdown').dropdown({
    action: 'hide',
    position: 'right',
    transition: 'fade up'
  })

  projectDeleteForm.submit((event) => {
    if(!projectDeleteFormProcessed) {event.preventDefault()}

    confirmationModal.modal({
      transition: 'fade up',
      onApprove () {
        projectDeleteFormProcessed = true
        projectDeleteForm.submit()
      }
    }).modal('show')
  })

  $('.ui.progress').progress()
})
