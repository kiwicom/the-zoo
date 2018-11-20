<template>
  <button v-on:click="selectRelated" class="ui compact fluid transparent button">
    {{ service.name }}
  </button>
</template>

<script>
  import * as R from 'ramda'

  export default {
    props: ['service'],
    data () {
      return {
        cells: []
      }
    },
    computed: {
      nSelected () {
        return R.filter(R.prop('selected'), this.cells).length
      },
    },
    mounted () {
      this.loadCells()
    },
    methods: {
      loadCells () {
        this.cells = R.filter(R.prop('selectable'), this.$store.getters.issuesFromHeader('column', this.service.id))
      },
      selectRelated () {
        if(this.cells.length === 0) {
          this.loadCells()
        }
        const store = this.$store
        const nSelected = this.nSelected
        const action = nSelected === 0 ? 'selectIssue' : 'unselectIssue'

        R.forEach(function (c) {
          store.commit(action, c.issue.pk)
        }, this.cells)
      }
    }
  }
</script>
