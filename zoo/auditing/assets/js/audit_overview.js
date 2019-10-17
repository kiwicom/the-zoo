import '../style/audit_overview.less'
import * as R from 'ramda'
import Vue from 'vue'
import Vuex from 'vuex'
import IssueList from './components/IssueList'
import MainHeader from './components/MainHeader'
import 'fomantic-ui-css/semantic.min.js'

const propStartsWith = R.curry(function (propName, prefix, element) {
  return R.startsWith(prefix, R.prop(propName, element))
})

Vue.filter('pluralize', pluralize)

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    data: {
      issues: {},
      filters: {
        available: {},
        applied: {}
      },
    },
    selectedIssues: {},
    filteringTerm: '',
  },
  getters: {
    selectedPatches (state) {
      const issues = state.data.issues;
      const selected = state.selectedIssues;
      return R.filter(
        (name) => issues[name].patch !== null && selected.hasOwnProperty(name),
        Object.keys(issues),
      )
    },
    selectedKindsCount (state) {
      return Object.keys(state.selectedIssues).length
    },
    selectedIssuesCount (state) {
      return R.sum(
        R.map((repos) => repos.length, Object.values(state.selectedIssues))
      )
    },
    selectedPatchesCount (state, getters) {
      return R.sum(
        R.map(
          (repos) => repos.length,
          Object.values(R.pick(getters.selectedPatches, state.selectedIssues))
        )
      )
    },
    isSelectedIssue (state) {
      return (name) => {
        return state.selectedIssues.hasOwnProperty(name)
      }
    },
    isSelected (state) {
      return (issue_name, repo_id) => {
        return (
          state.selectedIssues.hasOwnProperty(issue_name) &&
          R.contains(repo_id, state.selectedIssues[issue_name])
        )
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
    setIssueData (state, issues) {
      state.data.issues = issues
    },
    setFilters (state, filters) {
      state.data.filters = filters
    },
    initFilters (state) {
      state.data.filters.available = R.differenceWith(
        R.whereEq,
        state.data.filters.available,
        state.data.filters.applied
      )
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
    setFilteringTerm (state, term) {
      state.filteringTerm = term
    },
    selectIssues (state, { name, repos_ids }) {
      var selected = repos_ids || R.uniq(
        R.map(
          (element) => element.repository.id,
          state.data.issues[name].projects
        )
      )
      selected.push(...state.selectedIssues[name] || [])
      Vue.set(state.selectedIssues, name, selected)
    },
    unselectIssues (state, { name, repos_ids }) {
      if (repos_ids !== undefined) {
        state.selectedIssues[name] = R.without(repos_ids, state.selectedIssues[name])
      }
      if (repos_ids === undefined || state.selectedIssues[name].length === 0) {
        Vue.delete(state.selectedIssues, name)
      }
    },
    clearSelectedIssues (state) {
      state.selectedIssues = {}
    },
  },
})

new Vue({
  el: '.app',
  data() {
    return this.$store.state.data
  },
  computed: {
    empty() {
      return this.$store.state.data.services.length === 0
    }
  },
  components: {
    MainHeader,
    IssueList,
  },
  mounted() {
    $.get(window.location.href).done((response) => {
      store.commit('setIssueData', response.issues)
      store.commit('setFilters', {
        available: response.filters,
        applied: response.applied_filters,
      })
      $('.issue-list').removeClass('loading ui segment')
    })
  },
  store: store
})
