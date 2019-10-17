import '../style/project_detail.less'
import jQuery from 'jquery/src/jquery'
import 'fomantic-ui-css/semantic.min.js'
import Mustache from 'mustache'

$(document).ready(() => {
  const repoDetailsContainer = $('#repository-details-container')
  const pagerdutyDetailsContainer = $('#pagerduty-details-container')
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

  $.get(pagerdutyDetailsContainer.data('url'))
  .done((response) => {
    let template = $('#pagerduty-details').html()
    pagerdutyDetailsContainer.html(Mustache.render(template, response))
    pagerdutyDetailsContainer.removeClass('loading')
    $('.statistic').popup({
      transition: 'fade down',
      exclusive: true,
      position: 'top center'
    })
  })
  .fail(() => {
    showSnackbar('Failed fetching pagerduty details')
    pagerdutyDetailsContainer.remove()
  })

  $('.histogram .hitbox').popup({
    transition: 'fade down',
    position: 'top center',
    on: 'hover',
    exclusive: true,
    delay: {
      show: 250,
      hide: 0
    },
    className: {
      popup: 'ui histogram-popup popup'
    }
  })

  $('#issue-description').popup({
    transition: 'fade down',
    position: 'left center',
    on: 'click',
    exclusive: true,
    delay: {
      show: 250,
      hide: 0
    }
  })

  $('.ui.project-actions.dropdown').dropdown({
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
