import '../style/audit_overview.less'
import * as R from 'ramda'
import Vue from 'vue'
import Vuex from 'vuex'
import MainHeader from './components/MainHeader'
import Matrix from './components/Matrix'
import 'semantic-ui-css/semantic.min.js'
import hljs from 'highlight.js/lib'

const isSelected = function (el) {
  return el.selected
}
const propStartsWith = R.curry(function (propName, prefix, element) {
  return R.startsWith(prefix, R.prop(propName, element))
})
const currentOrEmptyList = function (key, obj) {
  return R.propOr([], key, obj)
}

Vue.use(Vuex)

$.get(window.location.href).done((response) => {
  const store = new Vuex.Store({
    state: {
      data: {
        services: response.services,
        issues: response.issues,
        filters: {
          available: response.filters,
          applied: response.applied_filters
        }
      },
      filteringTerm: '',
      selectedIssues: [],
      cells: [],
      issuesByNamespace: {},
      issuesByService: {}
    },
    getters: {
      selectedCount (state) {
        return state.selectedIssues.length
      },
      issuesFromHeader (state) {
        return function (kind, id) {
          const headerList = (kind === 'row' ? state.issuesByNamespace : state.issuesByService)
          return currentOrEmptyList(id, headerList)
        }
      },
      filteredFilters (state) {
        return R.filter(propStartsWith('name', state.filteringTerm), state.data.filters.available)
      },
      appliedFiltersByType (state) {
        return function (type) {
          return R.filter(R.propEq('type', type), state.data.filters.applied)
        }
      }
    },
    mutations: {
      setAppData (state, obj) {
        Object.assign(state.data, obj)
      },
      setFilteringTerm (state, term) {
        state.filteringTerm = term
      },
      addAppliedFilter (state, filter) {
        const filterObj = R.find(R.whereEq(filter), state.data.filters.available)

        if (filterObj) {
          state.data.filters.available = R.difference(state.data.filters.available, [filterObj])
          state.data.filters.applied.push(filterObj)
        }
      },
      removeAppliedFilter (state, filter) {
        const filterObj = R.find(R.whereEq(filter), state.data.filters.applied)

        if (filterObj) {
          state.data.filters.applied = R.difference(state.data.filters.applied, [filterObj])
          state.data.filters.available.push(filterObj)
        }
      },
      initFilters (state) {
        state.data.filters.available = R.differenceWith(
          R.whereEq,
          state.data.filters.available,
          state.data.filters.applied
        )
      },
      registerCell (state, payload) {
        const cell = payload.cell
        const rel = payload.rel

        state.cells.push(cell)

        state.issuesByNamespace[rel.rowId] = R.insert(0, cell, currentOrEmptyList(rel.rowId, state.issuesByNamespace))
        state.issuesByService[rel.columnId] = R.insert(0, cell, currentOrEmptyList(rel.columnId, state.issuesByService))
      },
      selectIssue (state, id) {
        state.selectedIssues.push(id)
      },
      unselectIssue (state, id) {
        state.selectedIssues = R.reject(R.equals(id), state.selectedIssues)
      },
      clearSelectedIssues (state) {
        state.selectedIssues = []
      }
    }
  })

  new Vue({
    el: '.app',
    data () {
      return this.$store.state.data
    },
    computed: {
      empty () {
        return this.$store.state.data.services.length === 0
      }
    },
    components: {
      MainHeader,
      Matrix
    },
    mounted () {
      $('.app').removeClass('loading')
    },
    store: store
  })

  $('.auditgrid-column .ui.fluid.button').popup({
    transition: 'fade down',
    hoverable: true,
    variation: 'inverted',
    duration: 100,
    delay: {
      show: 300,
      hide: 0
    },
    onShow () {
      $('.ui.popup code, .ui.popup pre').each(function (index, block) {
        hljs.highlightBlock(block)
      })
    }
  })
})
