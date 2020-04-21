import * as R from 'ramda'
import jQuery from 'jquery/src/jquery'
import 'fomantic-ui-css/semantic.min.js'
import Vue from 'vue'
import Vuex from 'vuex'
import SearchInput from './components/SearchInput'


Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    results: [],
    inputValue: '',
    enteredText: ''
  },
  getters: {
    getFilteredSuggestions (state) {
      return R.filter(R.where({
        reference: R.contains(state.enteredText)
      }), state.results)
    },
    getRepoId (state) {
      return (repoName) => {
        return R.filter(
          R.propSatisfies(
            ref => ref.split(' - ')[1] === repoName,
            'reference'
          ), state.results
        )
      }
    },
    getRepoReference (state) {
      return (repoId) => {
        return R.find(R.propEq('id', repoId), state.results).reference
      }
    }
  },
  mutations: {
    setEnteredText (state, term) {
      state.enteredText = term
    },
    selectSuggestion (state, id) {
      state.inputValue = id
    },
    refreshEnteredText (state) {
      const matchedValue = R.find(R.propEq('id', state.inputValue), state.results)
      state.enteredText = matchedValue ? matchedValue.reference : ''
    },
    clearInputs (state) {
      state.enteredText = ''
      state.inputValue = ''
    }
  }
})

const searchInputApp = new Vue({
  el: '#search-input',
  store: store,
  components: {
    SearchInput
  },
})

console.log('Whatever')
