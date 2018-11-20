<template>
  <button v-if="(exists && issue.status !='fixed')" class="matrix-cell-button" v-on:click="selectCell">
    <i class="material-icons" :data-selectable="selectable" v-if="url === null">{{ icon }}</i>
    <a :href="url" target="_blank" v-if="url !== null" style="text-decoration: none;">
      <i class="material-icons" :data-selectable="selectable">{{ icon }}</i>
    </a>
  </button>
  <i v-else class="material-icons" style="color: #4CAF50;">check</i>
</template>

<script>
  import * as R from 'ramda'

  export default {
    props: ['current', 'services'],
    methods: {
      selectCell () {
        if (this.exists && this.selectable) {
          this.$store.commit((!this.selected ? 'selectIssue' : 'unselectIssue'), this.issue.pk)
        }
      }
    },
    data () {
      const exists = R.contains(this.current.id, R.map(R.prop('id'), this.services))
      const issue = exists ? R.find(R.propEq('id', this.current.id), this.services) : null
      const issueUrl = exists && issue.remote_id ? issue.url : null
      const selectable = exists && issue.status === 'new' && issue.remote_id === null
      return {
        exists: exists,
        url: issueUrl,
        issue: issue,
        selectable: selectable
      }
    },
    mounted () {
      if (this.issue !== null) {
        this.$store.commit('registerCell', {
          cell: this,
          rel: {
            rowId: this.issue.kind_key,
            columnId: this.current.id
          }
        })
      }
    },
    computed: {
      selected () {
        return R.contains(this.issue.pk, this.$store.state.selectedIssues)
      },
      icon () {
        if (this.exists) {
          switch(this.issue.status) {
            case 'new':
              if (this.issue.remote_id === null) {
                return (this.selected ? 'check_box' : 'check_box_outline_blank')
              } else {
                return 'code'
              }
            case 'wontfix': return 'close'
            case 'fixed': return 'done'
          }
        }
        return 'done'
      }
    }
  }
</script>
