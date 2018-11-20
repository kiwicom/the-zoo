<template>
  <div class="ui segments auditgrid-wrapper">
    <div :class="['ui', 'paddingless', 'segment', 'auditgrid', nselected > 0 ? 'results': '']">
      <div :class="{'compact': compactMode, 'auditgrid-header': true}">
        <div class="auditgrid-column">
          <div class="auditgrid-cell">
            <button v-on:click="toggleCompactClass" class="ui compact fluid icon button" style="display: none; pointer-events: none;">
              <i class="bars icon"></i>
            </button>
          </div>
        </div>
        <div class="auditgrid-header-services">
          <div v-for="s in services" :key="`service-${s.id}`" class="auditgrid-cell">
              <matrix-service-header :service="s"></matrix-service-header>
          </div>
        </div>
      </div>
      <div :class="[compactMode ? 'compact' : '', 'auditgrid-body']">
        <div class="auditgrid-column">
          <template v-for="[severity, issue_list] in groupedIssues">
            <div :class="['auditgrid-cell', 'auditgrid-severity', `severity-${severity}`]">
              {{ formatSeverityText(severity) }}
            </div>
            <div class="auditgrid-cell" v-for="[key, instance] in issue_list" :key="`issue-${key}`">
              <matrix-issue-header :issue="instance" :name="key"></matrix-issue-header>
            </div>
          </template>
        </div>
        <div class="auditgrid-matrix">
          <template v-for="[severity, issue_list] in groupedIssues">
            <div class="auditgrid-row auditgrid-severity">
              <div v-for="i in services.length" :class="['auditgrid-cell', 'auditgrid-severity', `severity-${severity}`]"></div>
            </div>
            <div class="auditgrid-row" v-for="[key, instance] in issue_list">
              <div class="auditgrid-cell" v-for="s in services" :key="`issue-${instance.id}-service-${s.id}`" >
                <matrix-cell :services="instance.services" :current="s"></matrix-cell>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>
    <div v-if="nselected > 0" class="ui yellow inverted segment table-actions">
      <div class="flex-horizontal selected-info">
        <h5 class="ui tiny header">{{ nselected }} selected</h5>
        <div class="ui compact tiny red circular icon button" v-if="nselected > 0" v-on:click="clearSelected">
          <i class="cancel circle icon"></i>
        </div>
      </div>
      <div class="ui compact brown vertical animated button" v-on:click="openIssues">
        <div class="hidden content">
          <i class="gitlab icon"></i>
        </div>
        <div class="visible content">
          Create issues
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import MatrixCell from './MatrixCell'
  import MatrixIssueHeader from './MatrixIssueHeader'
  import MatrixServiceHeader from './MatrixServiceHeader'
  import * as R from 'ramda'

  const issueModal = $('.ui.basic.modal')
  const issueModalText = issueModal.find('#issue-modal-text')
  var tSingleColumnBody = null
  var tHead = null
  var tBodyScroll = null

  var bodyScrollValues = {
    left: 0,
    top: 0
  }

  var scheduledAnimationFrame = false

  String.prototype.format = function() {
    return [...arguments].reduce((p,c) => p.replace(/%s/,c), this)
  };

  window.applyScroll = function () {
    tHead.scrollLeft = bodyScrollValues.left
    tSingleColumnBody.scrollTop = bodyScrollValues.top
    scheduledAnimationFrame = false
  }

  window.tableBodyOnScroll = function () {
    bodyScrollValues.top = tBodyScroll.scrollTop
    bodyScrollValues.left = tBodyScroll.scrollLeft

    if(scheduledAnimationFrame)
      return

    window.requestAnimationFrame(applyScroll)
  }

  const bySeverity = R.groupBy(
    (issue) => {
      const data = issue[1]
      return data.severity
    }
  )

  const severityOrder = R.sortBy(
    (category) => {
      const key = category[0]
      switch (key) {
        case 'critical':
          return 0
        case 'warning':
          return 1
        case 'advice':
          return 2
      }

      return -1
    }
  )

  export default {
    props: ['services', 'issues'],
    mounted () {
      tSingleColumnBody = this.$el.querySelector('.auditgrid-body>.auditgrid-column')
      tHead = this.$el.querySelector(".auditgrid-header-services")
      tBodyScroll = this.$el.querySelector(".auditgrid-matrix")
      tBodyScroll.addEventListener('scroll', window.tableBodyOnScroll)
      tSingleColumnBody.style.paddingBottom = tBodyScroll.offsetHeight - tBodyScroll.clientHeight + 'px'
      tHead.style.marginRight = tBodyScroll.offsetWidth - tBodyScroll.clientWidth + 'px'
    },
    data () {
      return {
        compactMode: true,
        groupedIssues: severityOrder(
          Object.entries(
            bySeverity(Object.entries(this.issues))
          )
        )
      }
    },
    computed: {
      nselected () {
        return this.$store.getters.selectedCount
      }
    },
    methods: {
      toggleCompactClass () {
        this.compactMode = !this.compactMode
      },
      clearSelected () {
        this.$store.commit('clearSelectedIssues')
      },
      formatSeverityText (originalText) {
        return `${originalText.charAt(0).toUpperCase()}${originalText.slice(1)} issues`
      },
      openIssues () {
        const nselected = this.nselected
        const store = this.$store

        issueModal.modal({
          transition: 'fade up',
          onShow() {
            issueModalText.html(issueModalText.html().format(nselected))
          },
          onApprove () {
            const request = new XMLHttpRequest()

            request.onreadystatechange = function () {
              if(request.readyState === XMLHttpRequest.DONE) {
                if (request.status === 200) {
                  const responseData = request.response
                  store.commit('clearSelectedIssues')
                  store.commit('setAppData', responseData)
                  store.commit('initFilters')
                  showSnackbar('Issues created succesfully')
                } else {
                  showSnackbar('Error creating issues. Please reload')
                }
              }
            }

            request.open("POST", auditOverviewEndpoint)
            request.setRequestHeader("X-CSRFToken", auditOverviewCsrfToken)
            request.responseType = 'json'

            const requestData = JSON.stringify({
              pk_list: R.uniq(store.state.selectedIssues),
              filters: store.state.data.filters
            })
            request.send(requestData)
          }
        }).modal('show')
      }
    },
    components: {
      MatrixCell,
      MatrixIssueHeader,
      MatrixServiceHeader
    }
  }

</script>
