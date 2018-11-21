import '../style/service_detail.less'
import jQuery from 'jquery/src/jquery'
import 'semantic-ui-css/semantic.min.js'
import Mustache from 'mustache'

$(document).ready(() => {
  const repoDetailsContainer = $('#repository-details-container')
  const serviceDeleteForm = $('#service-delete-form')
  const confirmationModal = $('.ui.basic.modal')
  let serviceDeleteFormProcessed = false

  $.get(repoDetailsContainer.data('url'))
  .done((response) => {
    let template = $('#repository-details').html()
    repoDetailsContainer.html(Mustache.render(template, response))
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

  $('.ui.service-actions.dropdown').dropdown({
    action: 'hide',
    position: 'right',
    transition: 'fade up'
  })

  serviceDeleteForm.submit((event) => {
    if(!serviceDeleteFormProcessed) {event.preventDefault()}

    confirmationModal.modal({
      transition: 'fade up',
      onApprove () {
        serviceDeleteFormProcessed = true
        serviceDeleteForm.submit()
      }
    }).modal('show')
  })
})
