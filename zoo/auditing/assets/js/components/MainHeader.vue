<template>
  <div class="main-header" v-on:click="enterWritingMode">
    <search-input :filtersCount="filtersCount" :filters="filters"></search-input>
  </div>
</template>

<script>
  import SearchInput from './SearchInput'
  import * as R from 'ramda'
  const URI = require('urijs')

  export default {
    computed: {
      filters () {
        return this.$store.state.data.filters.applied
      },
      filtersCount () {
        return this.filters.length
      }
    },
    mounted () {
      this.$store.commit('initFilters')
    },
    methods: {
      applyFilters () {
        const store = this.$store
        const newUrl = URI(auditOverviewUrl)

        newUrl.addSearch({
          owner: R.map(R.prop('name'), store.getters.appliedFiltersByType('owner'))
        })
        newUrl.addSearch({
          namespace: R.map(R.prop('name'), store.getters.appliedFiltersByType('namespace'))
        })
        newUrl.addSearch({
          status: R.map(R.prop('name'), store.getters.appliedFiltersByType('status'))
        })

        window.location = newUrl
      },
      enterWritingMode () {
        document.querySelector('#search-input').focus()
      }
    },
    components: {
      SearchInput
    },
    created () {
      this.$on('applyFilters', this.applyFilters)
    }
  }
</script>
