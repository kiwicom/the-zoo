<template>
  <div class="issue-header-wrapper flex-horizontal">
    <button v-on:click="selectRelated" class="ui compact fluid transparent button" :data-title="name"
      :data-html="description + '<br>' + effort + severity"
      data-position="right center">
      {{ name }}
    </button>
  </div>
</template>

<script>
  import * as R from 'ramda'
  import snarkdown from 'snarkdown'

  export default {
    props: ['issue', 'name'],
    data () {
      return {
        cells: [],
        description: snarkdown(this.issue.description),
        effort: "<br>effort: <b>" + this.issue.effort + '</b>',
        severity: "<br>severity: <b>" + this.issue.severity + '</b>',
      }
    },
    computed: {
      nSelected () {
        return R.filter(R.prop('selected'), this.cells).length
      }
    },
    methods: {
      loadCells () {
        this.cells = R.filter(R.prop('selectable'), this.$store.getters.issuesFromHeader('row', this.name))
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
