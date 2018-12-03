import * as R from 'ramda'
import jQuery from 'jquery/src/jquery'
import 'semantic-ui-css/semantic.min.js'
import Vue from 'vue'
import Vuex from 'vuex'
import RepoInput from './components/RepoInput'
import TagInput from './components/TagInput'
import '../style/service_form.less'

$('select').dropdown({
  transition: 'fade down'
})

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    repoList: repoList,
    inputValue: '',
    enteredText: ''
  },
  getters: {
    getFilteredSuggestions (state) {
      return R.filter(R.where({
        reference: R.contains(state.enteredText)
      }), state.repoList)
    },
    getRepoId (state) {
      return (repoName) => {
        return R.filter(
          R.propSatisfies(
            ref => ref.split(' - ')[1] === repoName,
            'reference'
          ), state.repoList
        )
      }
    },
    getRepoReference (state) {
      return (repoId) => {
        return R.find(R.propEq('id', repoId), state.repoList).reference
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
      const matchedValue = R.find(R.propEq('id', state.inputValue), state.repoList)
      state.enteredText = matchedValue ? matchedValue.reference : ''
    },
    clearInputs (state) {
      state.enteredText = ''
      state.inputValue = ''
    }
  }
})

const repoInputApp = new Vue({
  el: '#repo-input',
  store: store,
  components: {
    RepoInput,
    TagInput
  },
})

const tagInputApp = new Vue({
  el: '#tag-input',
  store: store,
  components: {
    RepoInput,
    TagInput
  },
})
